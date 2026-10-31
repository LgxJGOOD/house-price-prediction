<template>
            <!-- 左侧面包屑 -->
            <el-breadcrumb :separator-icon="ArrowRight">
                <el-breadcrumb-item v-for ="(item,index) in filteredRoutes" :key="index">
                    <span>{{  item.meta.title }}</span>
                </el-breadcrumb-item>
            </el-breadcrumb>  
</template>

<script setup>
import { useRoute } from 'vue-router'
import { computed } from 'vue';
import { ArrowRight } from '@element-plus/icons-vue'; 
const route = useRoute()



// 过滤掉 meta.title 为 'layout' 的项，并且确保只显示首页
const filteredRoutes = computed(() => {
  const matchedRoutes = route.matched.filter(item => item.meta?.title !== 'layout');
  
  // 如果只剩下一个项且其标题是 '首页'，则返回该项
  if (matchedRoutes.length === 1 && matchedRoutes[0].meta?.title === '首页') {
    return matchedRoutes;
  }

  // 否则返回所有非 'layout' 的项
  return matchedRoutes;
});

</script>

<style scoped lang="scss">

</style>