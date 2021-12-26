<template>
  <div class='login_con'>
    <div class='login_box'>
      <div class='logo'>
        <img src="../assets/logo.png">
      </div>
      <el-form class='form_style' :model="UserForm" :rules="UserRules" ref="userRef">
        <el-form-item prop="name">
          <el-input prefix-icon="el-icon-user" v-model='UserForm.name' placeholder="用户名"></el-input>
        </el-form-item>
        <el-form-item prop="pwd">
          <el-input prefix-icon="el-icon-unlock" v-model='UserForm.pwd' show-password placeholder="密码"></el-input>
        </el-form-item>
        <el-form-item  class='btns'>
          <el-button type="primary" @click="login">登录</el-button>
          <el-button @click="restFrom">重置</el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script>
export default {
  data () {
    return {
      UserForm: {
        name: '',
        pwd: ''
      },
      UserRules: {
        name: [
          { required: true, message: '请输入用户名', trigger: 'blur' },
          { min: 2, max: 6, message: '长度在 2 到 6 个字符', trigger: 'blur' }
        ],
        pwd: [
          { required: true, message: '请输入密码', trigger: 'blur' }
        ]
      }
    }
  },
  methods: {
    restFrom () {
      // console.log(this)
      this.$refs.userRef.resetFields()
    },
    login () {
      this.$refs.userRef.validate(async valid => {
        if (!valid) return
        //  登录操作
        const { data: res } = await this.$axios.post('/user/login', this.$qs.stringify(this.UserForm))
        // console.log(res)
        if (res.status === 200) {
          window.sessionStorage.setItem('token', res.data.token)
          this.$msg.success(res.msg)
          this.$router.push('/home')
        } else {
          this.$msg.error(res.msg)
        }
      })
    }
  }
}
</script>
<style lang='less' scoped>
  .login_con{
    background-color: rgb(161, 154, 250);
    height: 100%;
  }
  .login_box{
    height: 300px;
    width: 400px;
    border-radius: 40px;
    background-color: cornsilk;
    position: absolute;
    left: 40%;
    top: 40%;
    transform: translate(-30%, -30%);
  }
  .logo{
    height: 80px;
    width: 200px;
    border: 1px solid #eee;
    padding: 10px;
    box-shadow: 0 0 20px #eee;
    border-radius: 10%;
    position: absolute;
    left: 50%;
    transform: translate(-50%,-50%);
    img{
      height: 100%;
      width: 100%;
    }
  }
  .form_style{
    position: absolute;
    bottom: 0;
    width: 100%;
    padding: 10% 10%;
    box-sizing: border-box;
  }
  .btns{
    display: flex;
    justify-content: flex-end;
  }
</style>
