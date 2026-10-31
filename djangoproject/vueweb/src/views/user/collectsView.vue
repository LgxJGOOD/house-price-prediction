<template>
    <el-card class="box-card">
      <!-- 添加按钮和搜索框 -->
      <div class="header-actions">
  
        <div class="input_box">
       <h2>景点收藏和评分</h2>
        </div>
     
      </div>
  
      <!-- 表格组件 -->
      <el-table :data="dataList" style="width: 100%; margin-top: 20px;" border>
        <el-table-column prop="districtName" label="景点城市" width="150" />
        <el-table-column prop="poiName" label="景点名称" width="150" />
        <el-table-column prop="rating" label="我的评分" width="150" />
        <el-table-column prop="collectText" label="我的收藏" width="150" />
        <el-table-column prop="nickname" label="用户昵称" width="150" />
        <el-table-column prop="create_date" label="创建时间" width="200" />
      </el-table>
  
      <!-- 分页 -->
      <el-pagination background layout="prev, pager, next, sizes, ->,jumper, total" :page-size="searchParams.pagesize"
        v-model:current-page="searchParams.page" :page-sizes="[10, 15, 20, 25, 30]" :total="total"
        @size-change="handleSizeChange" @current-change="fetchData" style="margin-top: 20px;" />
    </el-card>
  
  </template>
  
  <script setup>
  import { reactive, ref, onMounted } from 'vue';
  import { favoriteList } from '@/api/data/index.js';
  import useUserStore from '@/store/modules/user';
  const userStore = useUserStore();

  // 定义响应式数据
  const searchParams = reactive({
    user_id: 0,
    page: 1,
    pagesize: 10,
  });
  
  const dataList = ref([]);
  const total = ref(0);


  const formatDate = (isoString) => {
    const date = new Date(isoString);
    return new Intl.DateTimeFormat('zh-CN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
        hour12: false, // 使用24小时制
    }).format(date);
};

  const fetchData = async () => {
    if (userStore.id) {
    searchParams.user_id = userStore.id;
  }
    try {
        const res = await favoriteList(searchParams);
        if (res.code === 200) {
            total.value = res.data.count || 0;
            dataList.value = res.data.results.map(comment => {
              const collectText = comment.is_collect ? '已收藏' : '未收藏';
                return {
                    ...comment,
                    create_date: formatDate(comment.create_date),
                    collectText:collectText
                };
            }
           
        );

        }
    } catch (error) {
        console.error('Failed to fetch comments:', error);
    }
};


  // 处理分页大小变化
  const handleSizeChange = (newSize) => {
    searchParams.pagesize = newSize;
    fetchData();
  };
  
  

  
  // 组件挂载时获取数据
  onMounted(() => {
    fetchData();
  });
  </script>
  
  <style scoped>
  /* 使用 Flexbox 布局 */
  .header-actions {
    display: flex;
    align-items: center;
    /* justify-content: space-between; */
    margin-bottom: 20px;
  }
  
  .input_box {
    width: 200px;
    margin-right: 20px;
  }
  
  /* 设置头像样式 */
  .avatar1 {
    width: 60px;
    height: 60px;
    /* border-radius: 50%; */
    object-fit: cover;
  }
  

  
  /* 美化表格 */
  .el-table {
    border: 1px solid #ebeef5;
    border-radius: 4px;
    overflow: hidden;
  }
  
  /* 美化分页 */
  .el-pagination {
    text-align: right;
  }
  </style>
  
