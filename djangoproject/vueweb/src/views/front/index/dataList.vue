<template>
  <div style="margin-top: 80px;">
    <el-breadcrumb separator=">">
    <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
    <el-breadcrumb-item>
      <a to="{ path: '/travel/list' }">景区景点</a>
    </el-breadcrumb-item>
    <el-breadcrumb-item>景点列表</el-breadcrumb-item>
  </el-breadcrumb>
  </div>
<hr>
    <el-card class="box-card">
      <!-- 添加按钮和搜索框 -->
      <div class="header-actions">
        <div class="input_box">
          <el-input placeholder="请输入内容" v-model="searchParams.keyWord" class="input-with-select">
            <template #append>
              <el-button @click="fetchData"><el-icon>
                  <Search />
                </el-icon></el-button>
            </template>
          </el-input>
        </div>
      </div>
  
       <!-- 表格组件 -->
    <el-table :data="dataList" style="width: 100%; margin-top: 20px;" border>
      <el-table-column label="景点图片" align="center" width="100">
        <template #default="scope">
          <img :src="scope.row.image_url" alt="景点图片" class="avatar1">
        </template>
      </el-table-column>
      <el-table-column prop="cn_tit" label="景点名称" width="180" />
      <el-table-column prop="desbox" label="景点介绍" width="350" />
      <el-table-column prop="city" label="城市" width="60" />
      <el-table-column prop="cur_score" label="评分" width="60" align="center" />
      <el-table-column prop="memo2" label="旅游时节" width="550" />
      <el-table-column prop="memo1" label="建议游览时间" width="120" />
      <el-table-column label="详情" align="center">
        <template #default="scope">
          <el-button type="primary" size="small" icon="Edit" @click="editRow(scope.row)">详情</el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 分页 -->
    <el-pagination background layout="prev, pager, next, sizes, ->,jumper, total" :page-size="searchParams.pagesize"
      v-model:current-page="searchParams.pagenum" :page-sizes="[10, 15, 20, 25, 30]" :total="total"
      @size-change="handleSizeChange" @current-change="fetchData" style="margin-top: 20px;" />
  </el-card>
  </template>
  
  <script setup>
  import { reactive, ref, onMounted } from 'vue';
  import { traveltList } from '@/api/data/index.js';

  
  // 定义响应式数据
  const searchParams = reactive({
    keyWord: '',
    pagenum: 1,
    pagesize: 15,
  });
  
  const dataList = ref([]);
  const total = ref(0);
  
  // 获取数据的方法
  const fetchData = () => {
    traveltList(searchParams).then((res) => {
      if (res.code === 200) {
        dataList.value = res.data.results || [];
        total.value = res.data.count || 0;
      }
    }).catch((error) => {
      console.error('Failed to fetch data:', error);
    });
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
  .box-card{
    margin-top: 10px;
  }
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