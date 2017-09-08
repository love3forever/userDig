<template>
    <div id="login_page">
      <el-row>
        <el-col :span="24"><div class="grid-content bg-purple-dark"></div></el-col>
      </el-row>
      <el-row>
        <el-col :span="6" :offset="9">
          <el-card class="box-card">
              <el-form label-width="30px" label-position="top" class="demo-ruleForm">
                <el-form-item label="用户名" prop="username">
                  <el-input type="username" v-model="username" auto-complete="off"></el-input>
                </el-form-item>
                <el-form-item label="密码" prop="password">
                  <el-input type="password" v-model="password" auto-complete="off"></el-input>
                </el-form-item>
                <el-form-item>
                  <el-button id="submit_btn" type="primary" @click="submitForm()">提交</el-button>
                </el-form-item>
                <a href="da" style="">忘记密码</a>
                <router-link to="/register">用户注册</router-link>
              </el-form>      
          </el-card>
        </el-col>
      </el-row>   
      
    </div>
</template>

<script>
export default {
  name: "Login",
  data: function () {
    return {
      username:'',
      password:''
    }
  },
  methods:{
    submitForm() {
      if (this.username && this.password){
        this.$http.post('/api/v1/auth', JSON.stringify({username: this.username,password:this.password})).then(response=>{
          console.log(response) 
          localStorage.setItem('id_token',response.data['access_token'])
          this.$message('登陆成功');
          this.$router.push('/');
        })
      }
      console.log('try login')
    }
  },
  mounted: function (){
    let jwt_token = localStorage.getItem('id_token')
    if (jwt_token) {
      this.$message('请先登出当前用户')
      this.$router.push('/')
    }
  }
};
</script>

<style lang="css" scoped>
.grid-content {
  border-radius: 4px;
  min-height: 36px;
}

#submit_btn {
  width: 100%;
}

</style>