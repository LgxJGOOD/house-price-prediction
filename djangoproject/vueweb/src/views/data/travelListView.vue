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
        <el-button type="primary" size="default" icon="Plus" @click="openAddDialog">添加</el-button>
      </div>
  
      <!-- 表格组件 -->
      <el-table :data="dataList" style="width: 100%; margin-top: 20px;" border>
        <el-table-column prop="title" label="行程标题" width="200" />
        <el-table-column prop="journey_time" label="行程安排" width="260">
        <template #default="scope">
          <span>
            {{  '第'+scope.row.journey_time +'天'}} <br/>
            {{ scope.row.scheduling }}
          </span>
        </template>
      </el-table-column>
        <el-table-column prop="dine" label="用餐" width="260" />
        <el-table-column prop="Activities" label="景点/场地" width="260" />
        <el-table-column prop="hotel" label="酒店" width="120" />
        <el-table-column prop="city" label="所在城市" width="100" />
        <el-table-column label="操作" align="center">
          <template #default="scope">
            <el-button type="primary" size="small" icon="Edit" @click="editRow(scope.row)">编辑</el-button>
            <el-button type="danger" size="small" icon="Delete" @click="deleteRow(scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
  
      <!-- 分页 -->
      <el-pagination background layout="prev, pager, next, sizes, ->,jumper, total" :page-size="searchParams.pagesize"
        v-model:current-page="searchParams.pagenum" :page-sizes="[10, 15, 20, 25, 30]" :total="total"
        @size-change="handleSizeChange" @current-change="fetchData" style="margin-top: 20px;" />
    </el-card>
  
    <!-- 新增/修改 -->
    <el-dialog v-model="dialogFormVisible" :title="isEditMode ? '修改城市信息' : '新增城市信息'" width="30%" @closed="resetForm">
      <el-form ref="dataFormRef" :model="formData" :rules="rules" label-width="100px" label-position="left">
        <el-form-item prop="title" label="行程标题:">
          <el-input v-model="formData.title" placeholder="请输入行程标题" />
        </el-form-item>
        <el-form-item label="行程时间:" prop="journey_time">
        <el-input-number v-model="formData.journey_time" :precision="0" :step="1" :min="1" :max="20" />
      </el-form-item>
        <el-form-item prop="scheduling" label="行程安排:">
          <el-input v-model="formData.scheduling" placeholder="请输入行程安排" />
        </el-form-item>
        <el-form-item prop="dine" label="行程用餐:">
          <el-input v-model="formData.dine" placeholder="请输入行程用餐" />
        </el-form-item>
        <el-form-item prop="Activities" label="行程活动:">
          <el-input v-model="formData.Activities" placeholder="请输入行程活动" />
        </el-form-item>
        <el-form-item prop="hotel" label="行程酒店:">
          <el-input v-model="formData.hotel" placeholder="请输入行程酒店" />
        </el-form-item>
        <el-form-item prop="city" label="城市:">
        <el-select v-model="formData.city" placeholder="请选择城市" style="width: 100%;">
          <el-option v-for="city in cityDataList" :key="city.name" :label="city.name" :value="city.name">
          </el-option>
        </el-select>
      </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="closeDialog">取消</el-button>
        <el-button type="primary" :loading="loading" @click="handleCreateOrUpdate">确认</el-button>
      </template>
    </el-dialog>
  
  </template>
  
  <script setup>
  import { reactive, ref, onMounted } from 'vue';
  import { travelListApi,travelsAddApi, travelAddEditApi, travelAddDelApi,cityListApi} from '@/api/data/index.js';
  import { ElMessage, ElMessageBox } from 'element-plus';
  
  // 定义响应式数据
  const searchParams = reactive({
    keyWord: '',
    pagenum: 1,
    pagesize: 10,
  });
  
  const dataList = ref([]);
  const total = ref(0);
  const dialogFormVisible = ref(false);
  const isEditMode = ref(false); // 是否为编辑模式
  const loading = ref(false); // 表单提交加载状态
  const cityDataList = ref([]);
  
  const formData = reactive({
      'id': undefined,
      'title': '',
      'journey_time': '',
      'scheduling': 1,
      'city': '',
      'dine': '',
      'hotel':'',
      'Activities':''
             });
  
  const dataFormRef = ref(null);
  
  
  const rules = reactive({
    title: [{ required: true, message: '请输入线路标题', trigger: 'change' }],
    journey_time: [{ required: true, message: '请输入行程时间', trigger: 'blur' }],
    scheduling: [{ required: true, message: '请输入行程安排', trigger: 'blur' }],
  });
  
  


//获取城市信息数据
const fetchCityData = () => {
  cityListApi().then((res) => {
    if (res.code === 200) {
      cityDataList.value = res.data || [];
    }
  }).catch((error) => {
    console.error('Failed to fetch data:', error);
  });
};




  // 打开添加对话框
  const openAddDialog = () => {
      // resetFormData();
      formData.id = undefined;
      formData.title = '';
      formData.journey_time = '';
      formData.scheduling = '';
      formData.city = '';
      formData.dine = '';
      formData.hotel = '';
      formData.Activities = '';
  
      isEditMode.value = false;
      dialogFormVisible.value = true;
  };
  
  // 打开修改对话框
  const editRow = (row) => {
    // Object.assign(formData, row);
      formData.id = row.id;
      formData.title = row.title;
      formData.journey_time = row.journey_time;
      formData.scheduling = row.scheduling;
      formData.city =row.city;
      formData.dine = row.dine;
      formData.hotel = row.hotel;
      formData.Activities = row.Activities;
  
      isEditMode.value = true; // 设置为编辑模式
      dialogFormVisible.value = true;
  };
  
  
  // 获取数据的方法
  const fetchData = () => {
    travelListApi(searchParams).then((res) => {
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
  
  
  
  
  // 提交表单的方法
  const handleCreateOrUpdate = async () => {
      try {
          await dataFormRef.value.validate();
          loading.value = true; // 开始加载动画
  
          let response;
          if (isEditMode.value) {
              response = await travelAddEditApi(formData);
          } else {
              response = await travelsAddApi(formData);
          }
          if (response.code === 200) {
              ElMessage.success(isEditMode.value ? '行程信息修改成功 ' : '行程信息新增成功');
              resetFormData();
              fetchData(); // 刷新列表
              closeDialog();
              //刷新网页
  
          } else {
              ElMessage.error(isEditMode.value ? '行程修改失败，请稍后再试' : '行程添加失败，' + response.message);
          }
      } catch (error) {
          ElMessage.error(isEditMode.value ? '行程修改失败，请检查输入信息' : '行程添加失败，请检查输入信息');
          console.error('Failed to create or update user:', error);
      } finally {
          loading.value = false;
      }
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
      const res = await travelAddDelApi(row.id);
  
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
  
  // 关闭对话框并重置表单
  const closeDialog = () => {
    dialogFormVisible.value = false;
    resetFormData();
  };
  
  // 重置表单数据
  const resetFormData = () => {
    Object.assign(formData, {
      'id': undefined,
      'title': '',
      'journey_time': '',
      'scheduling': 1,
      'city': '',
      'dine': '',
      // 'hotel':'',
      'Activities':''
    });
    dataFormRef.value?.resetFields(); // 清除验证信息
  };
  
  
  // 组件挂载时获取数据
  onMounted(() => {
    fetchData();
    fetchCityData();
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
  
  
  .avatar-uploader .avatar {
      width: 178px;
      height: 178px;
      display: block;
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
  
