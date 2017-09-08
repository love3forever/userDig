<template>
  <div id="userdetail-container">
    <el-row>
      <el-col :span="20" :offset="2">
        <el-row>
          <el-col :span="5">
            <el-card :body-style="{ padding: '0px' }" id="user-card">
              <img :src="userDetail.img" class="image" id="detail-avatar">
              <div style="padding: 14px;">
                <span>{{userDetail.name}}</span>
                <div class="bottom clearfix">
                  <el-button type="text" class="button">操作按钮</el-button>
                </div>
              </div>
            </el-card>
          </el-col>
          <el-col :span="18" :offset="1">
             <el-row>
               <el-col :span="6" v-for="playlist in userDetail.playlist" :key="playlist.playlistId">
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
          </el-col>
        </el-row>
      </el-col>
    </el-row>
  </div>
</template>

<script>
export default {

  name: 'user_detail',

  data () {
    return {
      userDetail:'',
    };
  },
  methods:{
    getUserDetail(){
      this.$http.get('/api/v1/user/userdetail',{'headers':{'Authorization':'JWT '+localStorage.getItem('id_token')}}).then(response=>{
        console.log(response)
        this.userDetail = response.body
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
#userdetail-container {
  margin-top: 30px;
}

#user-card {
  width: 220px;
}

#detail-avatar {
  height: 220px;
  width: 220px;
  border-radius: 10px;
}
</style>