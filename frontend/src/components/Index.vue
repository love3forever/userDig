<template>
  <div>
    <el-menu theme="dark" class="el-menu-demo" mode="horizontal">
      <el-menu-item index="1">用户详情</el-menu-item>
      <el-menu-item index="2">用户歌单</el-menu-item>
      <el-menu-item index="3">歌曲分析</el-menu-item>
      <el-dropdown @command="handleCommand" id="user-detail">
        <span class="el-dropdown-link">
          <img src="http://p1.music.126.net/AX0idymyJI121iG4JK38ew==/3329321209374150.jpg?param=30y30" alt="">
        </span>
        <el-dropdown-menu slot="dropdown">
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

    };
  },
  methods:{
    logout() {
      localStorage.removeItem('id_token')

      this.$router.push('/login')
    },
    handleCommand(command) {
      if (command=="logout") {
        localStorage.removeItem('id_token')
        this.$message('完成登出')
        this.$router.push('/login')
      }
    }
  },
  mounted: function(){
    let jwt_token = localStorage.getItem('id_token')
    if (!jwt_token) {
      this.$message('请先完成登陆')
      this.$router.push('/login')
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
</style>