<template>
  <div>
    <el-row>
      <el-col :span="6" v-for="playlist in currentUser.playlist" :key="playlist.playlistId">
        <el-card class="playlist-card" :body-style="{ padding: '0px' }">
          <img :src="playlist.coverImgUrl" class="image" style="height:300px;width:300px;">
          <div style="padding: 5px;height:60px">
            <span>{{playlist.name}}</span>
            <div class="bottom clearfix">
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
export default {
  name: 'playlist_detail',

  data () {
    return {
      currentUser:'',
    };
  },
  methods:{
    getUserDetail(){
      this.$http.get('/api/v1/user/userdetail',{'headers':{'Authorization':'JWT '+localStorage.getItem('id_token')}}).then(response=>{
        console.log(response)
        this.currentUser = response.body
      }, response=>{
        this.$message('请用和网易云音乐相同的用户名')
      })
    }
  },
  mounted: function(){
    let jwt_token = localStorage.getItem('id_token')
    if (!jwt_token) {
      this.$message('请先完成登陆')
      this.$router.push('/login')
    }
    else{
      this.getUserDetail()
    }
  }
};
</script>

<style lang="css" scoped>
#user-detail {
  float: right;
  margin-right: 25px;
  margin-top: 17px;
}

#user-avatar {
  height: 30px;
  width: 30px;
}

.playlist-card {
  max-width: 300px;
  max-height: 385px;
  margin-left: 5px;
  margin-right: 5px;
  margin-top: 5px;
}
</style>