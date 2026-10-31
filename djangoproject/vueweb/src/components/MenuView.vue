<template>
  <template v-for="(item) in filteredMenuList" :key="item.path">
    <!-- 一级菜单项没有子路由 -->
    <el-menu-item
      v-if="!item.children || item.children.length === 0"
      :index="item.path"
    >
      <el-icon v-if="item.meta?.icon">
        <component :is="item.meta.icon"></component>
      </el-icon>
      <template #title>
        <span>{{ item.meta?.title }}</span>
      </template>
    </el-menu-item>

    <!-- layout 单独处理 -->
    <template v-if="isLayout(item)">
      <el-menu-item
        v-if="hasPermission(item.children[0])"
        :index="item.children[0].path"
      >
        <el-icon>
          <component :is="item.children[0].meta.icon"></component>
        </el-icon>
        <template #title>
          <span>{{ item.children[0].meta.title }}</span>
        </template>
      </el-menu-item>
    </template>

    <!-- 有子路由且大于一个，不是首页 layout -->
    <el-sub-menu v-else-if="hasChildren(item)" :index="item.path">
      <template #title>
        <el-icon v-if="item.meta?.icon">
          <component :is="item.meta.icon"></component>
        </el-icon>
        <span>{{ item.meta?.title }}</span>
      </template>
      <template v-for="(child, index) in item.children" :key="`${item.path}-${index}`">
        <!-- 递归处理子菜单 -->
        <el-menu-item 
          v-if="!child.meta?.hidden && hasPermission(child) && (!child.children || child.children.length === 0)"
          :index="child.path"
        >
          <el-icon v-if="child.meta?.icon">
            <component :is="child.meta.icon"></component>
          </el-icon>
          <span>{{ child.meta.title }}</span>
        </el-menu-item>
        <!-- 如果子菜单还有子路由，继续嵌套 sub-menu -->
        <el-sub-menu 
          v-else-if="!child.meta?.hidden && hasPermission(child) && child.children && child.children.length > 0"
          :index="child.path"
          :key="`${item.path}-${index}-submenu`"
        >
          <template #title>
            <el-icon v-if="child.meta?.icon">
              <component :is="child.meta.icon"></component>
            </el-icon>
            <span>{{ child.meta.title }}</span>
          </template>
          <template v-for="(grandChild, gcIndex) in child.children" :key="`${child.path}-${gcIndex}`">
            <el-menu-item 
              v-if="!grandChild.meta?.hidden && hasPermission(grandChild)"
              :index="grandChild.path"
            >
              <el-icon v-if="grandChild.meta?.icon">
                <component :is="grandChild.meta.icon"></component>
              </el-icon>
              <span>{{ grandChild.meta.title }}</span>
            </el-menu-item>
          </template>
        </el-sub-menu>
      </template>
    </el-sub-menu>
  </template>
</template>

<script setup name="Menu">
import { defineProps, computed ,watch } from 'vue';
import useUserStore from '@/store/modules/user';

const userStore = useUserStore();

const props = defineProps({
  menuList: {
    type: Array,
    required: true,
    default: () => []
  }
});


// 添加watch来监控roleMenus的变化
watch(() => userStore.roleMenus, (newVal) => {
  console.log('roleMenus updated:', newVal);
}, { immediate: true });

// 判断是否有权限
const hasPermission = (menuItem) => {
  console.log('Checking permission for menu item:', menuItem.name, 'roleMenus:', userStore.roleMenus);
  
  // 特殊处理：图表分析的子菜单继承父级权限
  const chartAnalysisChildren = ['dataAnalysisArea', 'dataAnalysisQuantity', 'dataAnalysisHouse', 'dataAnalysisPrice'];
  if (chartAnalysisChildren.includes(menuItem.name)) {
    // 如果父级菜单 dataAnalysis 有权限，则子菜单也有权限
    return userStore.roleMenus.includes('dataAnalysis');
  }
  
  // 其他菜单正常检查
  return userStore.roleMenus.includes(menuItem.name);
};

// 判断是否是 layout 类型的菜单
const isLayout = (item) => item.children && item.path === '/' && item.meta.title === 'layout';

// 判断是否有子菜单并且不是 layout
const hasChildren = (item) => item.children && item.children.length >= 1 && item.path !== '/' && item.meta.title !== 'layout';

// 过滤掉 hidden 为 true 的菜单项
const filteredMenuList = computed(() => {
  const result = props.menuList.filter(item => !item.meta?.hidden && hasPermission(item));
  console.log('Filtered menu list:', result); // 调试信息
  return result;
});

</script>

<style scoped>
.el-sub-menu .el-menu-item {
  display: block;
  visibility: visible;
}
</style>