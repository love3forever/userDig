#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-05-22 20:56:56
# @Author  : eclipse (eclipse_sv@163.com)
# @Link    : https://eclipsesv.com
# @Version : $Id$
import json
import requests
from bs4 import BeautifulSoup
from params_dicts import get_user_follows_param, get_user_fans_param, \
    get_playlist_comments_param, get_user_playlist_param, \
    get_user_playrecord_week, get_user_playrecord_all, album_comments,\
    follow_and_fans_data
from encrypter import encrypted_request
from proxy_hunter import gen_proxy, test_proxy, gen_myproxy


host_url = 'https://music.163.com{}'
indexURL = 'https://music.163.com/discover'
playlist_URL = 'https://music.163.com/playlist?id={}'
user_index_URL = 'http://music.163.com/user/home?id={}'
user_follows_URL = 'http://music.163.com/weapi/user/getfollows/{}?csrf_token='
user_fans_URL = 'http://music.163.com/weapi/user/getfolloweds?csrf_token='
user_playlist_URL = 'http://music.163.com/weapi/user/playlist?csrf_token='
user_playrecord_URL = 'http://music.163.com/weapi/v1/play/record?csrf_token='
playlist_comments_URL = 'http://music.163.com/weapi/v1/resource/comments/A_PL_0_{}?csrf_token='
playlist_detail_URL = 'http://music.163.com/api/playlist/detail?id={}'
song_comments_URL = 'http://music.163.com/api/v1/resource/comments/R_SO_4_{}/?rid=R_SO_4_{}&offset={}&total=true&limit=20'
song_detail_URL = 'http://music.163.com/api/song/detail?ids=[{}]'
song_lyric_URL = 'http://music.163.com/api/song/lyric?id={}&lv=-1&tv=-1'
artist_index_URL = 'http://music.163.com/artist?id={}'
artist_album_URL = 'http://music.163.com/artist/album?id={}&limit=200'
album_detail_URL = 'http://music.163.com/album?id={}'
album_comments_URL = 'http://music.163.com/weapi/v1/resource/comments/R_AL_3_{}'
djradio_comments_URL = 'http://music.163.com/weapi/v1/resource/comments/A_DJ_1_{}?csrf_token='
djradio_detail_URL = 'http://music.163.com/dj?id={}'

# proxy_pool = gen_proxy()
proxy_pool = gen_myproxy()
# proxy_pool = gen_kuaidaili()
proxies = {
    "http": "",
    "https": "",
}

host = 'music.163.com'
origin = 'http://music.163.com'
pragma = 'no-cache'
referer = 'http://music.163.com/'
agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36'

headers = {
    'User-Agent': agent,
    'Host': host,
    'Origin': origin,
    'Referer': referer,
    'Pragma': pragma,
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en,zh-CN;q=0.8,zh;q=0.6,zh-TW;q=0.4',
    'Cache-Control': 'no-cache'
}

session = requests.Session()
http_adapter = requests.adapters.HTTPAdapter(max_retries=3)
session.mount('http://', http_adapter)


def get_data_from_web(url):
    # 根据url获取原始数据
    # time.sleep(1)
    if url:
        try:
            origin_data = session.get(
                url, timeout=10, headers=headers, proxies=proxies)
            if origin_data.status_code == 200:
                print('current url:{}'.format(url))
                return origin_data
            else:
                gen_new_request()
                get_data_from_web(url)
        except Exception:
            gen_new_request()
            get_data_from_web(url)
    else:
        return None


def post_data_to_web(url, params):
    try:
        result_data = session.post(
            url, data=params, timeout=10, headers=headers, proxies=proxies)
        if result_data.status_code == 200:
            print('current url:{}'.format(url))
            return json.loads(result_data.text)
        else:
            gen_new_request()
            post_data_to_web(url, params)
    except Exception:
        gen_new_request()
        post_data_to_web(url, params)


def gen_new_request():
    try:
        while True:
            proxy_pair = next(proxy_pool)
            if test_proxy(proxy_pair):
                proxies['http'] = "http://{}:{}".format(*proxy_pair)
                proxies['https'] = "http://{}:{}".format(*proxy_pair)
                break
    except Exception:
        pass


def get_playlist_data(playlist_id):
    playlist_url = playlist_URL.format(playlist_id)
    playlist_origin_data = get_data_from_web(playlist_url)
    if playlist_origin_data:
        playlist_soup = BeautifulSoup(playlist_origin_data.content, 'lxml')
        # 获取歌单基本信息
        cntc = playlist_soup.select('.cntc')[0]
        cntc = parse_playlist_cntc(cntc)
        return cntc or None
    else:
        return None


def parse_playlist_cntc(data):
    if data:
        cntc_title = data.select('.f-ff2')[0].string
        tags = data.find_all('a', class_='u-tag')
        cntc_tags = []
        for tag in tags:
            tag_url = tag['href']
            tag_name = tag.select('i')[0].string
            cntc_tags.append({
                'tagURL': tag_url,
                'tagName': tag_name
            })
        cntc_creator_soup = data.find_all('div', class_='user f-cb')[0]
        creator_img = cntc_creator_soup.select('img')[0]['src']
        creator_url = cntc_creator_soup.select('span > a')[0]['href']
        creator_name = cntc_creator_soup.select('span > a')[0].string
        created_time = cntc_creator_soup.select('.time')[0].string
        cntc = {
            'cntcTitle': cntc_title,
            'cntcCreator': {
                'name': creator_name,
                'url': creator_url,
                'img': creator_img
            },
            'cntcCreatedTime': created_time,
        }
        return cntc
    else:
        return None


def data_poster(uid, postURL, keyword, getparamFunc):
    ##########################################
    # uid: 唯一标识符，可以为用户id，歌单id等
    # postURL: 发送post请求的目标url
    # keyword: 返回值目标数据的key
    # getparamFunc: 获取不同请求类型的请求参数的方法
    ##########################################
    if hasattr(getparamFunc, '__call__'):
        post_param = getparamFunc(uid)
        data_flag = True
        data_times = 0
        while data_flag:
            post_param['offset'] = int(data_times * 100)
            encrtyed_param = encrypted_request(post_param)
            response_data = post_data_to_web(postURL, encrtyed_param)
            if not response_data:
                break
            if keyword not in response_data.keys():
                break
            if response_data[keyword]:
                yield response_data[keyword]
            data_times += 1
            try:
                data_flag = response_data['more']
            except Exception:
                data_flag = False
    else:
        print('{} should be callable'.format(str(getparamFunc)))


def data_poster_withoffset(post_url, post_content):
    encrtyed_param = encrypted_request(post_content)
    response_data = post_data_to_web(post_url, encrtyed_param)
    return response_data

##########################################
# 获取用户相关内容 #########################
##########################################


def get_user_follows(userid):
    # 根据用户id获取关注列表
    return data_poster(userid, user_follows_URL.format(userid),
                       'follow', get_user_follows_param)


def get_user_follows_withoffset(userId, page):
    # 根据用户id和和offset获取关注列表
    follows_url = user_follows_URL.format(userId)
    post_data = follow_and_fans_data
    post_data['userId'] = userId
    post_data['limit'] = 100
    post_data['offset'] = (page - 1) * post_data['limit']
    result = data_poster_withoffset(follows_url, post_data)
    if result:
        return result.setdefault('follow', [])
    else:
        return None


def get_user_fans(userid):
    # 根据用户id获取粉丝列表
    return data_poster(userid, user_fans_URL, 'followeds', get_user_fans_param)


def get_user_fans_withoffset(userId, page):
    # 根据用户id和和offset获取关注列表
    fans_url = user_fans_URL.format(userId)
    post_data = follow_and_fans_data
    post_data['userId'] = userId
    post_data['limit'] = 100
    post_data['offset'] = (page - 1) * post_data['limit']
    result = data_poster_withoffset(fans_url, post_data)
    if result:
        return result.setdefault('follow', [])
    else:
        return None


def get_user_playlist(userid):
    # 根据用户id获取用户歌单
    user_data = data_poster(userid, user_playlist_URL,
                            'playlist', get_user_playlist_param)
    if user_data:
        user_playlist_result = {
            'own': [],
            'other': []
        }
        creator = None
        for data in user_data:
            for playlist in data:
                convert_data = {
                    'name': playlist['name'],
                    'playCount': playlist['playCount'],
                    'playlistId': playlist['id'],
                    'coverImgUrl': playlist['coverImgUrl']
                }
                if str(playlist['userId']) == str(userid):
                    user_playlist_result['own'].append(convert_data)
                    if not creator:
                        creator = playlist['creator']['nickname']
                else:
                    user_playlist_result['other'].append(convert_data)
        return user_playlist_result, creator
    else:
        return None


def get_user_playrecord(userid, kind):
    # 根据用户id获取用户播放记录
    if kind:
        getFunc = get_user_playrecord_all
    else:
        getFunc = get_user_playrecord_week
    return data_poster(userid, user_playrecord_URL, 'allData', getFunc)


def get_user_index(userid):
    # 根据用户id获取基本信息
    index_url = user_index_URL.format(userid)
    index_data = get_data_from_web(index_url)
    if index_data:
        index_content = index_data.content
        index_soup = BeautifulSoup(index_content, 'lxml')
        if not index_soup.select('#head-box'):
            return None
        index_box = index_soup.select('#head-box')[0]
        index_data = {}
        img_tag = index_box.select('#ava > img')
        if len(img_tag):
            index_data.setdefault(
                'img', img_tag[0]['src'])
        wrapper_tag = index_box.select('#j-name-wrap')
        if len(wrapper_tag):
            index_name_wrapper = wrapper_tag[0]
            index_name = index_name_wrapper.select('.tit')[0].string
            index_data.setdefault('name', index_name)
            index_level = index_name_wrapper.select('.lev')[0].next
            index_data.setdefault('level', index_level)
            genders = {
                "u-icn-00": "unknown",
                "u-icn-01": "male",
                "u-icn-02": "female"
            }
            index_gender = ''
            for item in genders.keys():
                if len(index_name_wrapper.select('.{}'.format(item))):
                    index_gender = genders[item]
                    break
            index_data.setdefault('gender', index_gender)
        events_tag = index_box.select('#event_count')
        if len(events_tag):
            index_events = events_tag[0].string
            index_data.setdefault('events', index_events)
        follow_tag = index_box.select('#follow_count')
        if len(follow_tag):
            index_follows = follow_tag[0].string
            index_data.setdefault('follows', index_follows)
        fans_tag = index_box.select('#fan_count')
        if len(fans_tag):
            index_fans = index_box.select('#fan_count')[0].string
            index_data.setdefault('fans', index_fans)
        age_tag = index_box.select('#age')
        if len(age_tag):
            index_location = age_tag[0]
            location_tag = index_location.find_previous_siblings("span")
            if len(location_tag):
                index_location_detail = location_tag[0].string
                index_data.setdefault('location', index_location_detail)
        networks_tag = index_box.select('.u-logo')
        if len(networks_tag):
            index_networks = networks_tag[0]
            index_social_networks = {}
            for item in index_networks.select('li > a'):
                index_social_networks.setdefault(item['title'], item['href'])
            index_data.setdefault('social_networks', index_social_networks)
        return index_data
    else:
        return None


##########################################
# 获取歌单相关内容 #########################
##########################################


def get_playlist_comments(playlistId):
    # 根据歌单id获取评论
    return data_poster(playlistId, playlist_comments_URL.format(
        playlistId), 'comments', get_playlist_comments_param)


def get_playlist_detail(playlistId):
    # 根据歌单id获取歌单详情
    detail_url = playlist_detail_URL.format(playlistId)
    detail_origin_data = get_data_from_web(detail_url)
    if detail_origin_data:
        detail_result = json.loads(detail_origin_data.content)
        return detail_result
    else:
        return None


def get_song_detail(songId):
    # 根据歌曲Id获取详情
    detail_url = song_detail_URL.format(songId)
    detail_data = get_data_from_web(detail_url)
    if detail_data.status_code == 200:
        detail_result = json.loads(detail_data.content)
        return detail_result
    else:
        return None


def get_song_comments(songId):
    # 根据歌曲ID获取全部评论
    data_list = []
    data_flag = True
    data_times = 0
    while data_flag:
        comments_url = song_comments_URL.format(
            songId, songId, 100 * data_times)
        response_data = get_data_from_web(comments_url)
        if response_data:
            response_data = json.loads(response_data.content)
            if response_data['comments']:
                data_list.extend(response_data['comments'])
            data_times += 1
            data_flag = response_data['more']
        else:
            return None
    return data_list


def get_playlist_comments_withoffset(playlistid, page):
    # 根据歌单id和page获取歌单评论
    postURL = playlist_comments_URL.format(playlistid)
    post_param = get_playlist_comments_param(playlistid)
    post_param['offset'] = str((page - 1) * 20)
    post_param['limit'] = str(20)
    return data_poster_withoffset(postURL, post_param)


def get_song_comments_withoffset(songId, page):
    # 根据歌曲id和page获取评论
    comments_url = song_comments_URL.format(
        songId, songId, 20 * (page - 1))
    response_data = get_data_from_web(comments_url)
    return json.loads(response_data.content)


def get_lyric(songId):
    lyricURL = song_lyric_URL.format(songId)
    response_data = get_data_from_web(lyricURL)
    lyric_data = json.loads(response_data.content)
    if lyric_data:
        # 修改歌词和翻译歌词
        try:
            lyric = lyric_data['lrc']['lyric']
        except Exception as e:
            print(str(e))
        else:
            lyric_str = convert_lyric(lyric)
            lyric_data['lrc']['lyric'] = lyric_str

        try:
            tlyric = lyric_data['tlyric']['lyric']
        except Exception as e:
            print(str(e))
        else:
            tlyric_str = convert_lyric(tlyric)
            lyric_data['tlyric']['lyric'] = tlyric_str
        return lyric_data
    else:
        return None


def convert_lyric(lyric):
    if lyric:
        lyric_data = lyric.split('\n')
        lyric_pure = [x[10:] for x in lyric_data[1:]]
        lyric_result = '\n'.join(lyric_pure)
        return lyric_result
    else:
        return None


##########################################
# 获取歌手相关内容 #########################
##########################################

def get_artist_index_page(artistId):
    index_url = artist_index_URL.format(artistId)
    index_data = get_data_from_web(index_url)
    index_info = {}
    if index_data:
        index_info.setdefault('artistId', artistId)
        index_soup = BeautifulSoup(index_data.content, 'lxml')
        top_50_songs = index_soup.select('#song-list-pre-cache > textarea')
        if len(top_50_songs):
            songs = top_50_songs[0].string
            try:
                index_info.setdefault('top50', json.loads(songs))
            except Exception as e:
                print(str(e))
        pic_info = index_soup.select('.n-artist > img')
        if len(pic_info) and pic_info[0] is not None:
            index_info.setdefault('img', pic_info[0]['src'])
        try:
            artist_name = index_soup.select('#artist-name')[0].string
            artist_alias = index_soup.select('#artist-alias')[0].string
        except Exception as e:
            print(str(e))
        else:
            index_info.setdefault('artist_name', artist_name)
            index_info.setdefault('artist_alias', artist_alias)
        return index_info
    else:
        return None


def get_artist_album(artistId):
    album_url = artist_album_URL.format(artistId)
    album_data = get_data_from_web(album_url)
    if album_data:
        album_soup = BeautifulSoup(album_data.content, 'lxml')
        album_list = album_soup.select('ul[id="m-song-module"] > li')
        album_result = []
        for album in album_list:
            img = album.select('img')[0]
            img_url = img['src']
            title = album.select('.s-fc0')[0].string
            time = album.select('.s-fc3')[0].string
            album_id = album.select('.s-fc0')[0]['href'][10:]
            album_info = {
                'img': img_url,
                'name': title,
                'time': time,
                'id': album_id
            }
            album_result.append(album_info)
        return album_result
    else:
        return None


##########################################
# 获取专辑相关内容 #########################
##########################################

def get_album_detail(albumId):
    album_url = album_detail_URL.format(albumId)
    album_data = get_data_from_web(album_url)
    if album_data:
        album_soup = BeautifulSoup(album_data.content, 'lxml')
        song_list = album_soup.select('#song-list-pre-cache > textarea')
        song_desc_all = album_soup.select('#album-desc-more > .f-brk')
        if len(song_desc_all) == 0:
            song_desc_all = album_soup.select('.n-albdesc > .f-brk')
        album_desc = ' '.join([x.string for x in song_desc_all])
        album_blk = album_soup.select('.topblk > .intr')
        album_singer = album_blk[0].select('a')[0]
        album_singer_name = album_singer.string
        album_singer_id = album_singer['href'][11:]
        album_publish_time = album_blk[1].select('b')[0].next_sibling
        album_publish_company = album_blk[2].select('b')[0].next_sibling
        if song_list:
            detail_data = json.loads(song_list[0].string)
            result_data = detail_data[0]['album']
            result_data.setdefault('alias', detail_data[0]['alias'])
            for item in detail_data:
                del item['album']
                del item['alias']
            result_data.setdefault('songs', detail_data)
            result_data.setdefault('singer', album_singer_name)
            result_data.setdefault('singer_id', album_singer_id)
            result_data.setdefault('publish_time', album_publish_time)
            result_data.setdefault('publish_company', album_publish_company)
            result_data.setdefault('desc', album_desc)
            return result_data
        else:
            return None
    else:
        return None


def get_album_comments_withoffset(albumId, page):
    comments_url = album_comments_URL.format(albumId)
    post_data = album_comments
    post_data['rid'] = post_data['rid'].format(albumId)
    post_data['offset'] = (page - 1) * post_data['limit']
    return data_poster_withoffset(comments_url, post_data)
