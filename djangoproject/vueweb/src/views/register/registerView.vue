<template>
  <div class="container">
    <div class="box">
      <h1>{{title}}</h1>
      <div class="title">欢迎注册</div>
      <el-form :model="RegisterForm" :rules="rules" ref="RegisterForms">
        <el-form-item prop="username">
          <el-input :prefix-icon="User" placeholder="请输入用户名" v-model="RegisterForm.username" size="large"></el-input>
        </el-form-item>
        <el-form-item prop="email">
          <el-input v-model="RegisterForm.email" placeholder="请输入邮箱" />
        </el-form-item>
        <el-form-item prop="nickname">
          <el-input v-model="RegisterForm.nickname" placeholder="请输入昵称" />
        </el-form-item>
        <el-form-item prop="password">
          <el-input :prefix-icon="Lock" placeholder="请输入密码" show-password v-model="RegisterForm.password"></el-input>
        </el-form-item>
        <el-form-item prop="password2">
          <el-input :prefix-icon="Lock" placeholder="请确认密码" show-password v-model="RegisterForm.password2"></el-input>
        </el-form-item>
        <el-form-item label="性别:" prop="gender">
          <el-radio-group v-model="RegisterForm.gender">
            <el-radio label="男" style="color: #150501;">男</el-radio>
            <el-radio label="女" style="color: #150501;">女</el-radio>
            <el-radio label="保密" style="color: #150501;">保密</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item>
          <el-button :loading='loading' type="primary" @click="Register">
            注册
          </el-button>
        </el-form-item>
        <el-form-item>
          已有账号？<router-link :to="{ path: '/login' }">立即登录</router-link>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script setup>
import { User, Lock } from '@element-plus/icons-vue'
import { reactive, ref } from 'vue'

import { useRouter, useRoute } from 'vue-router'
import { ElNotification } from 'element-plus'

import { getTime } from '@/utils/time'
import { register } from '@/api/user/index.js';

const router = useRouter()
const route = useRoute()
let loading = ref(false)
let RegisterForms = ref(null)

let RegisterForm = reactive({
  username: '',
  nickname: '',
  email: '',
  password: '',
  password2: '',
  role_id: '2',
  gender: ''
})

const title = ref(process.env.VUE_APP_LOGO_TITLE || '后台管理');
//自定义验证规则
const rules = reactive({
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  nickname: [{ required: true, message: '请输入昵称', trigger: 'blur' }],
  email: [{ type: 'email', required: true, message: '请输入有效的邮箱地址', trigger: 'blur' }],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, max: 16, message: '密码不少于6位且不多于16位', trigger: 'blur' }
  ],
  password2: [
    { required: true, message: '请确认密码', trigger: 'blur' },
    {
      validator: (rule, value, callback) => {
        if (value !== RegisterForm.password) {
          callback(new Error('两次输入的密码不一致'))
        } else {
          callback()
        }
      }, trigger: 'blur'
    }
  ],
  gender: [{ required: true, message: '请选择性别', trigger: 'change' }]
})


//注册
const Register = async () => {
  try {
    // 表单验证通过再发请求
    await RegisterForms.value.validate(async (valid) => {
      if (!valid) {
        console.log('验证未通过');
        return;
      }

      // 登录加载动画
      loading.value = true;
      const redirect = route.query.redirect;

      try {
        await register(RegisterForm);
        router.push({ path: redirect || '/login' });
        ElNotification.success({
          title: `Hi, ${getTime()}好~`,
          message: '注册成功',
        });
      } catch (err) {
        ElNotification.error({
          title: '注册失败',
          message: err.message || '未知错误',
        });
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
/* 设置整个页面的背景颜色和字体 */
body {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background-color: #f4f7fa;
  margin: 0;
  padding: 0;
}

.container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}

.box {
  width: 380px;
  /* 适当增加宽度 */
  background-color: #fff;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  border-radius: 12px;
  padding: 30px;
  /* 增加内边距 */
  animation: fadeIn 0.3s ease-in-out;
  /* 添加淡入动画 */
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}

h1 {
  font-size: 24px;
  font-weight: bold;
  text-align: center;
  color: #626aef;
  /* 与登录颜色匹配 */
  margin-bottom: 20px;
  /* 增加底部间距 */
}

.title {
  color: #626aef;
  font-size: 22px;
  font-weight: bold;
  text-align: center;
  margin-bottom: 20px;
}

.el-form {
  margin-top: 20px;
}

.el-form-item {
  margin-bottom: 20px;
}

.el-button {
  width: 100%;
  height: 40px;
  font-size: 16px;
}

/* 链接样式 */
.router-link {
  color: #626aef;
  text-decoration: none;
  transition: color 0.3s ease;

  &:hover {
    color: #4a52d1;
  }
}
</style>