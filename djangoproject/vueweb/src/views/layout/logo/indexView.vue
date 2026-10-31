<template>
  <div class="logo-container">
    <img :src="logoSrc" alt="Logo" class="logo" />
    <span v-if="showTitle">{{ title }}</span>
  </div>
</template>

<script setup>
/* eslint-disable no-unused-vars */
import {  defineProps , ref} from 'vue';
// 定义 props
const props = defineProps({
  logoSrc: {
    type: String,
    default: () => require('@/assets/logo.png'), // 使用 require 加载图片
  },
  showTitle: {
    type: Boolean,
    default: true,
  }
});

// 使用环境变量设置标题
const title = ref(process.env.VUE_APP_LOGO_TITLE || '后台管理');
</script>

<style scoped>
.logo-container {
  display: flex;
  align-items: center; /* 垂直居中 */
  justify-content: flex-start; /* 水平对齐到左侧 */
  /* margin-bottom: 20px; */
  color: #fff;
  height: 60px;
}

.logo {
  width: 40px;
  height: 40px;
  margin-right: 10px;
}
</style>