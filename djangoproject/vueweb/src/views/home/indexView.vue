<template>
  <el-card class="welcome-card">
    <div class="welcome-box">
      <!-- 头像 -->
      <div class="avatar-container">
        <img 
          v-if="!userStore.avatar" 
          src="https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png" 
          alt="default avatar"
          class="default-avatar"
        />
        <img 
          v-else 
          :src="userStore.avatar" 
          alt="user avatar" 
          class="user-avatar"
        />
      </div>

      <!-- 欢迎信息 -->
      <div class="greeting">
        <h1 v-if="!userStore.username" class="title not-logged-in">
          {{ getTime() }}好，
          <router-link to="/login" class="login-link">点击登录</router-link>
        </h1>
        <h1 v-else class="title logged-in">
          {{ getTime() }}好，{{ userStore.nickname }}
        </h1>
        <p class="subtitle">{{ currentTime  }}</p>
      </div>
    </div>
  </el-card>

  <el-card class="calendar-card" style="height: 400px;">
   <h1 class="system-title">{{title}}</h1>
  </el-card>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import useUserStore from '@/store/modules/user'
import { getTime } from '@/utils/time'


const userStore = useUserStore()
const title = ref(process.env.VUE_APP_LOGO_TITLE || '后台管理');

const currentTime = ref(new Date().toLocaleString());
// 方法：更新当前时间
const updateTime = () => {
  currentTime.value = new Date().toLocaleString();
};

// 组件挂载时开始更新时间
onMounted(() => {
  updateTime(); // 初始化时间
  const intervalId = setInterval(updateTime, 1000); // 每秒更新一次时间

  // 清理函数，在组件卸载或依赖项变化时清除定时器
  onBeforeUnmount(() => clearInterval(intervalId));
});
</script>

<style scoped>
/* 整体卡片样式 */
.welcome-card {
  margin: 10px;
  padding: 20px;
  text-align: center;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.calendar-card {
  margin: 10px;
  padding: 20px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

/* 欢迎信息盒子 */
.welcome-box {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
}

/* 头像容器 */
.avatar-container {
  margin-bottom: 20px;
}

.default-avatar, .user-avatar {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  object-fit: cover;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.user-avatar {
  border: 2px solid #409eff; /* 可选：为用户上传的头像添加边框 */
}

/* 欢迎标题 */
.title {
  font-size: 28px;
  font-weight: 600;
  margin-bottom: 10px;
}

.not-logged-in .login-link {
  color: #409eff;
  cursor: pointer;
  text-decoration: none;
  font-weight: bold;
}

.login-link:hover {
  text-decoration: underline;
}

.logged-in {
  color: #2c3e50;
}

/* 副标题 */
.subtitle {
  font-size: 18px;
  font-style: italic;
  color: slategray;
  margin-top: 20px;
}

.system-title {
  font-size: 36px; /* 字体大小可根据需求调整 */
  font-weight: bold;
  text-align: center;
}
</style>