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
            <el-button type="primary" size="default" icon="Plus" @click="openAddUserDialog">添加用户</el-button>
        </div>

        <!-- 表格组件 -->
        <el-table :data="dataList" style="width: 100%" border>
            <el-table-column type="selection" width="50" align="center" />
            <el-table-column label="头像" width="80" align="center">
                <template #default="scope">
                    <img :src="scope.row.avatar" alt="Avatar" class="avatar1">
                </template>
            </el-table-column>
            <el-table-column prop="username" label="用户名" width="120" align="center" />
            <el-table-column prop="email" label="邮箱" width="180" />
            <el-table-column prop="nickname" label="昵称" width="120" />
            <el-table-column prop="role_name" label="角色" align="center" width="100" />
            <el-table-column prop="gender" label="性别" width="80" align="center" />
            <el-table-column prop="is_active" label="管理员权限" width="100" align="center">
                <template #default="scope">
                    <el-switch v-model="scope.row.is_superuser" @change="switchChange(scope.row)" />
                </template>
            </el-table-column>
            <el-table-column prop="last_login" label="最后登录时间" width="180" />
            <el-table-column label="操作" align="center">
                <template #default="scope">
                    <el-button type="primary" size="small" icon="Edit" @click="editRow(scope.row)">编辑</el-button>
                    <el-button type="danger" size="small" icon="Delete" @click="deleteRow(scope.row)">删除</el-button>
                    <el-button type="danger" size="small" icon="Key" @click="resetRow(scope.row)">重置密码</el-button>
                </template>
            </el-table-column>
        </el-table>

        <!-- 分页 -->
        <el-pagination background layout="prev, pager, next, sizes, ->,jumper, total" :page-size="searchParams.pagesize"
            v-model:current-page="searchParams.pagenum" :page-sizes="[10, 15, 20, 25, 30]" :total="total"
            @size-change="handleSizeChange" @current-change="fetchData" style="margin-top: 20px;" />
    </el-card>

    <!-- 新增/修改 -->
    <el-dialog v-model="dialogFormVisible" :title="isEditMode ? '修改用户' : '新增用户'" width="30%" @closed="resetForm">
        <el-form ref="userFormRef" :model="formData" :rules="rules" label-width="100px" label-position="left">
            <!-- 在 dialog 表单中添加头像上传 -->

            <el-form-item label="头像:">
                <el-upload class="avatar-uploader" action="http://127.0.0.1:8899/api/upload/images/"
                    :show-file-list="false" :on-success="handleAvatarSuccess" :before-upload="beforeAvatarUpload">
                    <img v-if="formData.avatar" :src="formData.avatar" class="avatar" />
                    <el-icon v-else class="avatar-uploader-icon">
                        <Plus />
                    </el-icon>
                </el-upload>
            </el-form-item>
            <el-form-item prop="username" label="用户名:">
                <el-input v-model="formData.username" placeholder="请输入用户名" :disabled="isEditMode" />
            </el-form-item>
            <el-form-item prop="email" label="邮箱:">
                <el-input v-model="formData.email" placeholder="请输入邮箱" />
            </el-form-item>
            <el-form-item prop="nickname" label="昵称:">
                <el-input v-model="formData.nickname" placeholder="请输入昵称" />
            </el-form-item>
            <el-form-item label="性别:" prop="gender">
                <el-radio-group v-model="formData.gender">
                    <el-radio label="男">男</el-radio>
                    <el-radio label="女">女</el-radio>
                    <el-radio label="保密">保密</el-radio>
                </el-radio-group>
            </el-form-item>
            <el-form-item label="角色:" prop="role_name">
                <el-radio-group v-model="formData.role_id">
                    <el-radio v-for="role in roles" :key="role.id" :label="role.id">{{ role.name }}</el-radio>
                </el-radio-group>
            </el-form-item>
        </el-form>
        <template #footer>
            <el-button @click="closeDialog">取消</el-button>
            <el-button type="primary" :loading="loading" @click="handleCreateOrUpdate">确认</el-button>
        </template>
    </el-dialog>
</template>

<script setup>
import { reactive, ref, onMounted, nextTick } from 'vue';
import { userList, userAdd, userEdit, userEditState, userDel, userResetpsd, roleList } from '@/api/user/index.js';
import { ElMessage, ElMessageBox } from 'element-plus';
import useUserStore from '@/store/modules/user';

const userStore = useUserStore();
import { useRouter } from 'vue-router'
const roles = ref([]); // 角色列表
const router = useRouter();
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
    username: '',
    email: '',
    nickname: '',
    avatar: '',
    gender: '',
    role:''
});

const userFormRef = ref(null);

const fetchRoles = () => {
  roleList().then((res) => {
    if (res.code === 200) {
      roles.value = res.data.roles;
    } else {
      console.error('Failed to fetch roles:', res.message);
    }
  }).catch(error => {
    console.error('Error fetching roles:', error);
  });
};

// 自定义验证规则
const validatorUsername = (rule, value, callback) => {
    if (value.length >= 1) {
        callback();
    } else {
        callback(new Error('请输入账号'));
    }
};

const validatorEmail = (rule, value, callback) => {
    if (!value) {
        return callback(new Error('请输入邮箱'));
    }

    const emailPattern = /^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$/;
    if (!emailPattern.test(value)) {
        return callback(new Error('请输入正确的邮箱格式'));
    }

    callback();
};

const validatorNickname = (rule, value, callback) => {
    if (!value) {
        return callback(new Error('请输入昵称'));
    }

    if (value.length < 1 || value.length > 30) {
        return callback(new Error('昵称长度必须在1到30个字符之间'));
    }

    callback();
};

const rules = reactive({
    username: [
        { trigger: 'blur', validator: validatorUsername },
    ],
    email: [
        { trigger: 'blur', validator: validatorEmail },
    ],
    nickname: [
        { trigger: 'blur', validator: validatorNickname },
    ],
    gender: [{ required: true, message: '请选择性别', trigger: 'change' }]
});

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
// 获取数据的方法
const fetchData = () => {
    userList(searchParams).then((res) => {
        if (res.code === 200) {
            const formattedResults = res.data.results.map(item => ({
                ...item,
                last_login: item.last_login ? formatDate(item.last_login) : null
            }));
            dataList.value = formattedResults || [];
            total.value = res.data.count || 0;
        }
    }).catch((error) => {
        console.error('Failed to fetch data:', error);
    });
};


const handleSizeChange = (newSize) => {
    searchParams.pagesize = newSize;
    fetchData();
};

// 打开添加用户对话框
const openAddUserDialog = () => {
    // resetFormData();
    formData.id = undefined;
    formData.username = '';
    formData.email = '';
    formData.nickname = '';
    formData.avatar = '';
    formData.gender = '';
    formData.role = '';
    isEditMode.value = false;
    dialogFormVisible.value = true;
};

// 编辑行
const editRow = (row) => {
    Object.assign(formData, row); // 填充表单数据
    isEditMode.value = true; // 设置为编辑模式
    dialogFormVisible.value = true;
};
//删除
const deleteRow = (row) => {
    ElMessageBox.confirm('确定删除该用户吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
    }).then(() => {
        // 用户点击了确认按钮
        userDel(row.id).then((res) => {
            if (res.code === 200) {
                ElMessage.success('用户删除成功');
                fetchData(); // 刷新列表
            } else {
                ElMessage.error('用户删除失败，请稍后再试');
            }
        }).catch(error => {
            console.error('Failed to delete user:', error);
            ElMessage.error('用户删除失败，请稍后再试');
        });
    }).catch(action => {
        // 用户点击了取消按钮或关闭了对话框
        if (action === 'cancel') {
            ElMessage.info('已取消删除');
        } else {
            console.error('Unexpected action:', action);
        }
    });
};

// 重置密码
const resetRow = async (row) => {
    // 确认对话框
    const confirm = await ElMessageBox.confirm(
        '确定要将该用户的密码重置为默认值吗？',
        '警告',
        {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
        }
    ).catch(action => action);

    if (confirm !== 'confirm') {
        ElMessage.info('已取消重置密码');
        return;
    }

    try {
        loading.value = true;

        const response = await userResetpsd({
            user_id: row.id,
            new_password1: '12345678',
            new_password2: '12345678'
        });

        if (response.code === 200) {
            ElMessage.success('密码重置成功，默认密码为：12345678');

            // 检查是否为当前登录用户重置了密码
            const currentUserId = localStorage.getItem('id');
            if (currentUserId && parseInt(currentUserId, 10) === row.id) {
                ElMessage.warning('你重置了当前登录用户的密码，请重新登录');
                // 调用登出逻辑
                await userStore.useLogout();
                // 导航到登录页面
                nextTick(() => { // 使用 nextTick 确保所有 DOM 更新完成后再进行路由跳转
                    router.push('/login');
                });
            }
        } else {
            ElMessage.error(`密码重置失败：${response.message || '未知错误'}`);
        }
    } catch (error) {
        console.error('Failed to reset password:', error);
        ElMessage.error('密码重置失败，请稍后再试');
    } finally {
        loading.value = false; // 结束加载动画
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
        username: '',
        email: '',
        nickname: '',
        avatar: '',
        gender: '',
        role:''
    });
    userFormRef.value?.resetFields(); // 清除验证信息
};

// 提交表单的方法
const handleCreateOrUpdate = async () => {
    try {
        await userFormRef.value.validate();
        loading.value = true; // 开始加载动画

        let response;
        if (isEditMode.value) {
            formData.role = formData.role_id;
            response = await userEdit(formData);
        } else {
            response = await userAdd(formData);
        }
        if (response.code === 200) {
            if (isEditMode.value && formData.id == localStorage.getItem('id')) {
                ElMessage.warning('你修改了当前登录用户的信息，请重新登录')

                // window.location.reload();
            }
            ElMessage.success(isEditMode.value ? '用户修改成功' : '用户添加成功');



            resetFormData();
            fetchData(); // 刷新列表
            closeDialog();
            //刷新网页

        } else {
            ElMessage.error(isEditMode.value ? '用户修改失败，请稍后再试' : '用户添加失败，' + response.message);
        }
    } catch (error) {
        ElMessage.error(isEditMode.value ? '用户修改失败，请检查输入信息' : '用户添加失败，请检查输入信息');
        console.error('Failed to create or update user:', error);
    } finally {
        loading.value = false;
    }
};

// 修改用户状态的函数
const switchChange = async (row) => {
    const originalState = row.is_superuser;

    try {

        await userEditState({ id: row.id, state: row.is_superuser });
        ElMessage.success('用户状态更新成功');
    } catch (error) {
        row.is_active = originalState;
        ElMessage.error('用户状态更新失败，请稍后再试');
        console.error('Failed to update user state:', error);
    }
};



const beforeAvatarUpload = (file) => {
    const allowedTypes = ['image/jpeg', 'image/png', 'image/gif']; // 支持的图片格式
    const maxSizeMB = 2; // 最大大小，单位为MB
    const isAllowedType = allowedTypes.includes(file.type);
    const isLtMaxSize = file.size / 1024 / 1024 < maxSizeMB;

    if (!isAllowedType) {
        ElMessage.error(`上传头像图片只能是 ${allowedTypes.join(', ')} 格式!`);
    }
    if (!isLtMaxSize) {
        ElMessage.error(`上传头像图片大小不能超过 ${maxSizeMB}MB!`);
    }

    return isAllowedType && isLtMaxSize;
};


// 处理上传成功后的回调
const handleAvatarSuccess = (response) => {
    formData.avatar = response.data;
};

// 组件挂载时获取数据
onMounted(() => {
    fetchData();
    fetchRoles();
});
</script>

<style scoped>
.header-actions {
    display: flex;
    align-items: center;
    margin-bottom: 20px;
}

.input_box {
    width: 200px;
    margin-right: 20px;
}

/* 美化表格 */
.el-table {
    border: 1px solid #ebeef5;
    border-radius: 4px;
    overflow: hidden;
}

/* 设置头像样式 */
.avatar1 {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    object-fit: cover;
}

.avatar-uploader .avatar {
    width: 178px;
    height: 178px;
    display: block;
}

.el-pagination {
    text-align: right;
}
</style>

<style>
.avatar-uploader .el-upload {
    border: 1px dashed var(--el-border-color);
    border-radius: 6px;
    cursor: pointer;
    position: relative;
    overflow: hidden;
    transition: var(--el-transition-duration-fast);
}

.avatar-uploader .el-upload:hover {
    border-color: var(--el-color-primary);
}

.el-icon.avatar-uploader-icon {
    font-size: 28px;
    color: #8c939d;
    width: 178px;
    height: 178px;
    text-align: center;
}
</style>