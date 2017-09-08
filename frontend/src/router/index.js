import Vue from 'vue'
import Router from 'vue-router'
import base from '@/components/base'
import Login from '@/components/user/login'
import register from '@/components/user/register'
import userdetail from '@/components/common/user_detail'
import playlistdetail from '@/components/common/playlist_detail'
import userrelation from '@/components/common/user_relation'
import songdetail from '@/components/common/song_detail'

Vue.use(Router)

export default new Router({
  mode:'history',
  routes: [
    {
      path: '/',
      component: base,
      children :[
        { path: '', component: userdetail },
        { path: 'home', component: userdetail },
        { path: 'playlist', component: playlistdetail },
        { path: 'social', component: userrelation },
      ]
    },
    {
      path: '/login',
      name: 'Login',
      component: Login
    },
    {
      path: '/register',
      name: 'Register',
      component: register
    }
  ]
})
