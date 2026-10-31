import axios from 'axios';
import { ElMessage } from 'element-plus';
import useUserStore from '@/store/modules/user';
import { useRouter } from 'vue-router'

const router = useRouter();
// 创建 Axios 实例
const request = axios.create({
  baseURL: process.env.VUE_APP_BASE_API,
  timeout: 10000,
});

// 请求拦截器
request.interceptors.request.use(
  (config) => {
    const userStore = useUserStore();
    const token = userStore.token;
    if (token) {
      // 在 Authorization 头中添加 Bearer 前缀
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    // 处理请求错误
    return Promise.reject(error);
  }
);

// 响应拦截器
request.interceptors.response.use(
  (response) => response.data,
  async (error) => {
    let status = error.response ? error.response.status : null;
    let message = '';

    switch (status) {
      case 401:
        message = 'Token失效,请刷新重新登录';
        await handleUnauthorizedError(); 
        break;
      case 403:
        message = '权限不足';
        break;
      case 404:
        message = '请求地址错误';
        break;
      case 500:
        message = '服务器发生错误';
        break;
      default:
        message = '网络异常';
        break;
    }

    // 使用 Element Plus 的消息提示组件显示错误信息
    ElMessage({
      type: 'error',
      message,
    });

    return Promise.reject(error);
  }
);

// 处理 401 错误的函数
async function handleUnauthorizedError() {
  // 清除用户信息
  localStorage.removeItem('token');
  localStorage.removeItem('refresh');
  localStorage.removeItem('id');
  localStorage.removeItem('username');
  localStorage.removeItem('email');
  localStorage.removeItem('nickname');
  localStorage.removeItem('gender');
  localStorage.removeItem('is_active');
  localStorage.removeItem('is_superuser');
  localStorage.removeItem('bio');
  localStorage.removeItem('avatar');
  localStorage.removeItem('role_id');
  localStorage.removeItem('role_name');
  localStorage.removeItem('last_login');
  localStorage.removeItem('roleMenus');
  if (router && typeof router.push === 'function') {
    await router.push('/login');
  }
}


export default request;