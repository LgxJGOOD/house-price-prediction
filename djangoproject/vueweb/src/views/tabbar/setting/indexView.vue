<template>
    <el-button size="small" icon="FullScreen" circle @click="fullScreen"></el-button>
    <template v-if="!userStore.nickname">
        <img src="https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png" alt=""
            style="width: 24px; height: 24px; margin: 0px 10px; border-radius: 50%;">
        <el-button type="primary" @click="goToLogin">登录</el-button>
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
                    <!-- <el-dropdown-item @click="goToFront">前台</el-dropdown-item> -->
                    <el-dropdown-item @click="changePassword">修改密码</el-dropdown-item>
                    <el-dropdown-item @click="logout">退出登录</el-dropdown-item>
                </el-dropdown-menu>
            </template>
        </el-dropdown>
    </template>
</template>

<script setup>
import useUserStore from '@/store/modules/user';
import { useRoute, useRouter } from 'vue-router'

const userStore = useUserStore();
const router = useRouter();
const route = useRoute()
const fullScreen = () => {
    if (document.fullscreenElement) {
        document.exitFullscreen();
    } else {
        document.documentElement.requestFullscreen();
    }
}

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
    router.push('/users/user');
}

const goToLogin = () => {
    router.push('/admin/login');
};

// 新增方法：跳转到前台页面
// const goToFront = () => {
//     router.push('/index');
// };
</script>

<style scoped lang="scss"></style>