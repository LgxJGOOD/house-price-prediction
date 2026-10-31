<template>
  <div class="common-layout">
    <el-container>
      <!-- 菜单栏 -->
      <el-aside :width="isCollapse ? '64px' : '180px'" class="sidebar-container">
        <Logo :showTitle="!isCollapse" :collapsed="isCollapse"></Logo>
        <el-menu
          router
          background-color="#383d42"
          text-color="#fff"
          :collapse="isCollapse"
          :collapse-transition="false"
          :default-active="$route.path"
        >
          <Menu :menuList="userStore.menuRoutes"></Menu>
        </el-menu>
      </el-aside>

      <!-- 右侧导航内容 -->
      <el-container>
        <el-header style="padding-left: 0px;">
          <div class="header-content">
            <el-button type="text" @click="toggleCollapse" class="collapse-btn">
              <el-icon v-if="!isCollapse"><Expand /></el-icon>
              <el-icon v-else><Fold /></el-icon>
            </el-button>
            <Tabbar></Tabbar>
          </div>
        </el-header>
        <!-- 右侧内容 -->
        <el-main>
          <router-view :key="$route.fullPath"></router-view>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script setup>
import { ref } from 'vue';
// import { Expand, Fold } from '@element-plus/icons-vue'; // 导入图标组件
import Logo from './logo/indexView.vue';
import Menu from '@/components/MenuView.vue'; 
import useUserStore from '@/store/modules/user';
import Tabbar from '@/views/tabbar/indexView.vue';

let userStore = useUserStore();
// 控制 logo 文字 显示与否的布尔值
const isCollapse = ref(false);

const toggleCollapse = () => {
  isCollapse.value = !isCollapse.value;
};
</script>

<style lang="scss" scoped>
.common-layout {
  height: 100vh;
  width: 100vw;
  display: flex;
  flex-direction: column;

  .sidebar-container {
    background-color: #383d42;
    color: #333;
    text-align: center;
    line-height: normal;

    .el-menu {
      border-right: none;
    }
  }

  .el-container {
    height: 100%;

    .el-header {
      background-color: #b3c0d1;
      color: #333;
      line-height: 60px;
      display: flex;
      justify-content: space-between;
      align-items: center;

      .header-content {
        display: flex;
        align-items: center;
        justify-content: space-between;
        width: 100%;

        .collapse-btn {
          margin-right: 20px;
        }
      }
    }

    .el-main {
      background-color: #e9eef3;
      color: #333;
      // text-align: center;
      // line-height: 160px;
    }
  }
}
</style>