<template>
  <div>
    <el-container>
      <el-header class="fixed-header">
        <div style="display: flex; justify-content: space-between; align-items: center;">
          <el-menu 
            :default-active="activeIndex" 
            class="el-menu-demo" 
            mode="horizontal" 
            @select="handleSelect"
            style="flex-grow: 1; display: flex; justify-content: center;"
          >
            <el-menu-item index="1" @click="goToHome">首页</el-menu-item>
            <el-menu-item index="2" @click="goToTravelList">景区景点</el-menu-item>
            <el-menu-item index="3" @click="goToDataEchart">图表分析</el-menu-item>
            <el-menu-item index="4" @click="goToDataMap">景点地图</el-menu-item>
          </el-menu>
          <template v-if="!userStore.nickname">
        <img src="https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png" alt=""
            style="width: 24px; height: 24px; margin: 0px 10px; border-radius: 50%;">
        <el-button type="primary"  @click="goToLogin" style="margin-left: 20px;">登录</el-button>
    </template>
    <template v-else>
        <img :src="userStore.avatar" alt="" style="width: 24px;height: 24px; margin: 0px 10px; border-radius: 50%;">
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
                    <el-dropdown-item @click="goToBack">后台</el-dropdown-item>
                    <el-dropdown-item @click="goToBack">个人中心</el-dropdown-item>
                    <el-dropdown-item @click="changePassword">修改密码</el-dropdown-item>
                    <el-dropdown-item @click="logout">退出登录</el-dropdown-item>
                </el-dropdown-menu>
            </template>
        </el-dropdown>
    </template>
        </div>
      </el-header>
      <el-main>
        <router-view></router-view>
      </el-main>
    </el-container>
  </div>
</template>

<script setup>
import { ref,watch } from 'vue';
// import { ref } from 'vue';
import useUserStore from '@/store/modules/user';
import { useRoute, useRouter } from 'vue-router'

const userStore = useUserStore();
const router = useRouter();
const route = useRoute()

const activeIndex = ref('1');

// 根据路由路径设置 activeIndex
const setActiveIndexByRoute = () => {
  const path = route.path;
  if (path.startsWith('/travel/list')|| path.startsWith('/travel/detail/')) {
    activeIndex.value = '2';
  }else if (path.startsWith('/travel/echarts')) {
    activeIndex.value = '3';
  } else if (path.startsWith('/data/visual/map')) {
    activeIndex.value = '4';
  } else {
    activeIndex.value = '1'; // 默认首页
  }
};

setActiveIndexByRoute(); // 初始化时设置一次

watch(route, () => {
  setActiveIndexByRoute();
});


const handleSelect = (key, keyPath) => {
  console.log(key, keyPath);
};

const goToHome = () => {
  router.push('/index');
};

const goToTravelList = () => {
  router.push('/travel/list');
};

const goToDataEchart = () => {
  router.push('/travel/echarts');
};
const goToDataMap = () => {
  router.push('/data/visual/map');
};

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
const changePassword = () => {
    router.push('/admin/users/user');
}

const goToLogin = () => {
    router.push('/login');
};

const goToBack = () => {
    router.push('/admin/home');
};

</script>

<style scoped lang="scss">
.fixed-header {
  position: fixed;
  top: 0;
  width: 100%;
  z-index: 1000;
  padding: 0 50px; // 根据需要调整padding值来控制左右边距
  box-sizing: border-box;
  background-color: #d0d3d6; 
}
.el-menu-demo {
  border-bottom: none; // 移除菜单底部边框以避免与header的重叠
  background-color: #d0d3d6; 
}
</style>