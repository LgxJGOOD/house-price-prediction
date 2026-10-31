<template>
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
        <el-table-column prop="poiName" label="景点名称" width="150" />
        <el-table-column prop="review_content" label="评论内容" width="800" />
        <el-table-column prop="reviewer_name" label="评论者" width="150" />
        <el-table-column prop="create_date" label="评论时间" width="200" />
        <el-table-column label="操作" align="center">
          <template #default="scope">
            <el-button type="danger" size="small" icon="Delete" @click="deleteRow(scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
  
      <!-- 分页 -->
      <el-pagination background layout="prev, pager, next, sizes, ->,jumper, total" :page-size="searchParams.pagesize"
        v-model:current-page="searchParams.page" :page-sizes="[10, 15, 20, 25, 30]" :total="total"
        @size-change="handleSizeChange" @current-change="fetchData" style="margin-top: 20px;" />
    </el-card>
  
  </template>
  
  <script setup>
  import { reactive, ref, onMounted } from 'vue';
  import { travelCommentList,reviewsDel } from '@/api/data/index.js';
  import { ElMessage, ElMessageBox } from 'element-plus';
  import useUserStore from '@/store/modules/user';
  const userStore = useUserStore();

  // 定义响应式数据
  const searchParams = reactive({
    search: '',
    page: 1,
    pagesize: 10,
  });
  if (!userStore.is_superuser) {
  searchParams.reviewer_id = userStore.username;
}
  
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
    if (!userStore.is_superuser && !searchParams.reviewer_id) {
    searchParams.reviewer_id = userStore.username;
  }
    try {
        const res = await travelCommentList(searchParams);
        if (res.code === 200) {
            total.value = res.data.count || 0;
            dataList.value = res.data.results.map(comment => {
                return {
                    ...comment,
                    create_date: formatDate(comment.create_date),
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
  
  
  


  const showMessage = (type, message) => {
    const msg = message || {
      success: '删除成功',
      error: '删除失败',
      info: '已取消删除'
    }[type];
    ElMessage[type](msg);
  };
  
  const deleteRow = async (row) => {
    try {
      // 显示确认对话框
      await ElMessageBox.confirm('确定删除该数据吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      });
  
      // 执行删除操作
      const res = await reviewsDel(row.id);
  
      if (res.code === 200) {
        showMessage('success', res.message);
        fetchData();
      } else {
        showMessage('error', res.message);
      }
  
    } catch (error) {
      if (error instanceof Error) {
        console.error('Error during data deletion:', error);
        showMessage('error');
      }
    }
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
  
