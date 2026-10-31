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
      <el-table-column prop="name" label="城市名称" width="100" />
      <el-table-column prop="pinyin" label="城市名称拼音" width="200" />
      <el-table-column prop="desc" label="城市介绍" width="550" />
      <el-table-column prop="province" label="所属省份" width="120" />
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
      <el-form-item prop="name" label="城市名称:">
        <el-input v-model="formData.name" placeholder="请输入城市名称" />
      </el-form-item>
      <el-form-item prop="pinyin" label="名称拼音:">
        <el-input v-model="formData.pinyin" placeholder="请输入城市名称拼音" />
      </el-form-item>
      <el-form-item prop="desc" label="城市介绍:">
        <el-input v-model="formData.desc" placeholder="请输入城市介绍" />
      </el-form-item>
      <el-form-item prop="province" label="所属省份:">
        <el-input v-model="formData.province" placeholder="请输入城市所在省份" />
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
import { cityList,cityAdd, cityEdit, cityDel } from '@/api/data/index.js';
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


const formData = reactive({
  id: undefined,
  name: '',
  pinyin: '',
  desc: '',
  province:''
});

const dataFormRef = ref(null);


const rules = reactive({
  name: [{ required: true, message: '请输入城市名称', trigger: 'change' }],
  pinyin: [{ required: true, message: '请输入城市名称拼音', trigger: 'blur' }]
});


// 打开添加对话框
const openAddDialog = () => {
    // resetFormData();
    formData.id = undefined;
    formData.name = '';
    formData.pinyin = '';
    formData.desc = '';
    formData.province='';

    isEditMode.value = false;
    dialogFormVisible.value = true;
};

// 打开修改对话框
const editRow = (row) => {
  // Object.assign(formData, row);
  formData.id = row.id;
    formData.name = row.name;
    formData.pinyin = row.pinyin;
    formData.desc = row.desc;
    formData.province=row.province;

    isEditMode.value = true; // 设置为编辑模式
    dialogFormVisible.value = true;
};


// 获取数据的方法
const fetchData = () => {
  cityList(searchParams).then((res) => {
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
            response = await cityEdit(formData);
        } else {
            response = await cityAdd(formData);
        }
        if (response.code === 200) {
            ElMessage.success(isEditMode.value ? '城市信息修改成功 ' : '城市信息新增成功');
            resetFormData();
            fetchData(); // 刷新列表
            closeDialog();
            //刷新网页

        } else {
            ElMessage.error(isEditMode.value ? '城市修改失败，请稍后再试' : '城市添加失败，' + response.message);
        }
    } catch (error) {
        ElMessage.error(isEditMode.value ? '城市修改失败，请检查输入信息' : '城市添加失败，请检查输入信息');
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
    const res = await cityDel(row.id);

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
    id: undefined,
    name: '',
    pinyin: '',
    desc: '',
    province:''
  });
  dataFormRef.value?.resetFields(); // 清除验证信息
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

