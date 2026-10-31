<template>
  <div class="error">
    <div class="error-svg">
      <!-- 使用 img 标签 -->
      <img :src="require('../images/403.svg')" alt="403" />
    </div>
    <router-link to="/admin/home">
      <el-button type="primary">
        回到首页
      </el-button>
    </router-link>
  </div>
</template>

<style lang="scss" scoped>
.error {
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;

  .error-svg img {
    width: 300px; // 根据需要调整宽度
    height: auto; // 保持宽高比
  }
}
</style>