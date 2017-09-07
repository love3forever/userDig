<template>
    <div id="register_page">
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
              </el-form>      
          </el-card>
        </el-col>
      </el-row>   
      
    </div>
</template>

<script>
export default {

  name: 'register',

  data: function () {
    return {
      username:'',
      password:''
    }
  },
  methods:{
    submitForm() {
      if (this.username && this.password){
        this.$http.post('/api/v1/user/register', JSON.stringify({username: this.username,password:this.password})).then(response=>{
          console.log(response) 
          this.$message('注册成功');
          this.$router.push('/login');
        })
      }
      console.log('try login')
    }
  }
};
</script>

<style lang="css" scoped>
</style>