<template>
  <div>
    <el-menu theme="dark" class="el-menu-demo" mode="horizontal" @select="navSelect">
      <el-menu-item index="home" id="menu-home">用户详情</el-menu-item>
      <el-menu-item index="playlist">用户歌单</el-menu-item>
      <el-menu-item index="social">歌曲分析</el-menu-item>
      <el-dropdown @command="handleCommand" id="user-detail">
        <span class="el-dropdown-link">
          <img id="user-avatar" :src="currentUser.img" alt="">
        </span>
        <el-dropdown-menu slot="dropdown">
          <el-dropdown-item disabled>当前用户:<br>{{currentUser.name}}</el-dropdown-item>
          <el-dropdown-item command="logout">登出</el-dropdown-item>
          <el-dropdown-item command="setting">设置</el-dropdown-item>
        </el-dropdown-menu>
      </el-dropdown>
    </el-menu>
  </div>
</template>

<script>
export default {

  name: 'Index',

  data () {
    return {
      currentUser:'',
    };
  },
  methods:{
    logout() {
      localStorage.removeItem('id_token')
      this.$router.push('/login')
    },
    navSelect(key, keyPath){
      console.log(key)
      this.$router.push('/'+key)
    },
    handleCommand(command) {
      if (command=="logout") {
        localStorage.removeItem('id_token')
        this.currentUser = ''
        this.$message('完成登出')
        this.$router.push('/login')
      }
    },
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
  },
  watch:{
    '$route' (to, from) {
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

#menu-home {
  margin-left: 20px;
}
</style>