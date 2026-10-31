<template>
  <div class="login-container">
    <el-row>
      <el-col :span="12" :xs="0"></el-col>
      <el-col :span="12" :xs="24">
        <el-card class="card-container">
          <div class="header">
            <span>{{title}}</span>
            <!-- <span style="font-size: 18px;margin-top: 5px;">欢迎登录</span> -->
          </div>
          <el-form :model="loginForm" :rules="rules" ref="loginForms">
            <el-form-item prop="username">
              <el-input :prefix-icon="User" placeholder="请输入用户名" v-model="loginForm.username" size="large"></el-input>
            </el-form-item>
            <el-form-item prop="password">
              <el-input :prefix-icon="Lock" placeholder="请输入密码" show-password v-model="loginForm.password"></el-input>
            </el-form-item>
            <el-form-item>
              <el-button :loading='loading' type="primary" @click="login">
                登录
              </el-button>
            </el-form-item>
            <el-form-item>
              没有账号？<router-link :to="{ path: '/register' }">立即注册</router-link>
            </el-form-item>
          </el-form>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { User, Lock } from '@element-plus/icons-vue'
import { reactive, ref } from 'vue'
import useUserStore from '@/store/modules/user'
import { useRouter, useRoute } from 'vue-router'
import { ElNotification } from 'element-plus'
import { getTime } from '@/utils/time'
const userStore = useUserStore()
const router = useRouter()
const route = useRoute()
let loading = ref(false)
let loginForms = ref(null)


let loginForm = reactive({
  username: '',
  password: '',
})
const title = ref(process.env.VUE_APP_LOGO_TITLE || '后台管理');

//自定义验证规则
const validatorUsername = (rule, value, callback) => {
  if (value.length >= 1) {
    callback()
  } else {
    callback(new Error('请输入账号'))
  }
}

const validatorPassword = (rule, value, callback) => {
  if (value.length === 0) {
    callback(new Error('请输入密码'))
  } else if (value.length < 3 || value.length > 16) {
    callback(new Error('密码不少于3位的任意组合'))
  } else {
    callback()
  }
}



const rules = reactive({
  username: [
    {
      trigger: 'blur',
      validator: validatorUsername
    },
  ],
  password: [
    {
      trigger: 'blur',
      validator: validatorPassword
    }
  ],
})

//登录
const login = async () => {
  try {
    // 表单验证通过再发请求
    await loginForms.value.validate(async (valid) => {
      if (!valid) {
        console.log('验证未通过');
        return;
      }

      // 登录加载动画
      loading.value = true;
      const redirect = route.query.redirect;

      try {
        await userStore.userLogin(loginForm);
        router.push({ path: redirect || '/admin/home' });
        ElNotification.success({
          title: `Hi, ${getTime()}好~`,
          message: '欢迎回来',
        });
      } catch (err) {
        ElNotification.error({
          title: '登录失败',
          message: err.message +err.response.data.message || '未知错误1',
        });
        console.log('err',err.response.data.message);
      } finally {
        loading.value = false;
      }
    });
  } catch (err) {
    console.error('表单验证或登录过程中发生错误:', err);
    ElNotification.error({
      title: '发生错误',
      message: err.message || '未知错误',
    });
    loading.value = false;
  }

}

</script>

<style lang="scss" scoped>
.login-container {
  width: 100vw;
  height: 100vh;
  background: url('@/assets/images/background.jpg') no-repeat;
  background-size: cover;

  .el-row {
    height: 100%;

    .el-col {
      display: flex;
      justify-content: center;
      align-items: center;

      .card-container {
        width: 62%;
        background: url('@/assets/images/login_form.png') no-repeat bottom;
        border: 0;
        box-shadow: none;
        border-radius: 3px;

        .header {
          color: #111;
          font-size: 28px;
          padding-bottom: 22px;
        }

        .el-button {
          width: 100%;
        }
      }
    }
  }
}
</style>
