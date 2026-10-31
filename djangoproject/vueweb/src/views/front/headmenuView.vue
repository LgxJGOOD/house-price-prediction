<template>
  <el-menu :default-active="activeIndex" class="el-menu-demo" mode="horizontal" @select="handleSelect">
    <!-- 左侧导航 -->
    <div class="left-nav">
      <el-menu-item index="1">首页</el-menu-item>
      <el-menu-item index="2">数据可视化</el-menu-item>
      <el-menu-item index="3">大屏</el-menu-item>
    </div>

    <!-- 右侧用户信息 -->
    <div class="right-user-info">
      <template v-if="!userStore.nickname">
        <img src="https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png" alt=""
          style="width: 24px; height: 24px; margin-right: 10px; border-radius: 50%;">
        <el-button type="primary" @click="goToLogin">登录</el-button>
      </template>
      <template v-else>
        <img :src="userStore.avatar" alt="" style="width: 24px;height: 24px; margin-right: 10px; border-radius: 50%;">
        <!-- 下拉菜单 -->
        <el-dropdown>
          <span class="el-dropdown-link">
            {{ userStore.nickname }}
            <el-icon class="el-icon--right">
              <arrow-down></arrow-down>
            </el-icon>
          </span>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item @click="houtai">后台</el-dropdown-item>
              <el-dropdown-item @click="logout">退出登录</el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </template>
    </div>
  </el-menu>
</template>

<script setup>
import { ref } from 'vue'
import useUserStore from '@/store/modules/user';
import { useRoute, useRouter } from 'vue-router'


const userStore = useUserStore();
const router = useRouter();
const route = useRoute()

const logout = async () => {
    try {
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
        await userStore.useLogout();
        router.push({ path: '/login', query: { redirect: route.path } });
    } catch (error) {
        console.error('Logout failed:', error);
    }
}


const houtai = () => {
    router.push('/home');
}

const goToLogin = () => {
    router.push('/login');
};

const activeIndex = ref('1')
const handleSelect = (key, keyPath) => {
  console.log(key, keyPath);
}
</script>


<style scoped>
.el-menu-demo {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.left-nav {
  display: flex;
  align-items: center;
}

.right-user-info {
  display: flex;
  align-items: center;
}
</style>