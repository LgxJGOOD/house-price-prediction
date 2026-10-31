<template>
    <el-card class="box-card">
        <!-- 添加按钮 -->
        <div class="header-actions">
            <el-button disabled type="primary" size="default" icon="Plus" @click="handleAddRole">添加角色</el-button>
        </div>

        <!-- 表格组件 -->
        <el-table :data="dataList" style="width: 100%" border>
            <el-table-column type="selection" width="50" align="center" />
            <el-table-column prop="name" label="角色名称" width="180" align="center" />
            <el-table-column label="操作" align="center" width="300">
                <template #default="scope">
                    <el-button type="primary" size="small" icon="User" @click="openPermissionDrawer(scope.row)">分配菜单</el-button> 
                    <el-button type="primary" size="small" icon="Edit" @click="handleEdit(scope.row)">编辑</el-button>
                    <el-button disabled type="danger" size="small" icon="Delete" @click="handleDelete(scope.row)">删除</el-button>
                </template>
            </el-table-column>
        </el-table>
    </el-card>

    <!-- 修改角色名称 -->
    <el-dialog v-model="roleVisible" title="修改角色名称" style="width: 400px;">
        <el-form :model="role" :rules="roleRules" ref="roleFormRef" label-width="90px">
            <el-form-item label="角色名称:" prop="role_name">
                <el-input v-model="role.role_name"></el-input>
            </el-form-item>
        </el-form>
        <template #footer>
            <span class="dialog-footer">
                <el-button @click="roleVisible = false">取 消</el-button>
                <el-button type="primary" @click="saveRoleName">确 定</el-button>
            </span>
        </template>
    </el-dialog>

    <!-- 抽屉 -->
    <el-drawer v-model="permissionDrawerVisible" :show-close="false" title="分配菜单">
        <el-tree
            ref="menuTree"
            :data="formattedMenuData"
            show-checkbox
            node-key="id"
            default-expand-all
            :props="defaultProps"
            @check-change="handleCheckChange"
        />
        <template #footer>
            <span class="dialog-footer">
                <el-button @click="permissionDrawerVisible = false">取 消</el-button>
                <el-button type="primary" @click="savePermissions">保 存</el-button>
            </span>
        </template>
    </el-drawer>
  
</template>

<script setup>
import { ref, reactive, onMounted ,computed,nextTick} from 'vue';
import { ElMessage } from 'element-plus';
import { roleList, updateRole,menuList ,saveRoleMenu,getRoleMenu} from '@/api/user/index.js';

// 定义响应式数据
const dataList = ref([]);
const roleVisible = ref(false);
const roleFormRef = ref(null);
const role = reactive({
    id: null,
    role_name: '',
});
const permissionDrawerVisible = ref(false); // 抽屉可见性
const menuData = ref([]); // 菜单数据


const roleRules = {
    role_name: [{ required: true, message: '请输入角色名称', trigger: 'blur' }],
};

const defaultProps = {
    children: 'children',
    label: 'title'
};

const menuTree = ref(null);


// 格式化菜单数据，使其适用于 el-tree
const formattedMenuData = computed(() => {
    return menuData.value.map(item => ({
        id: item.id,
        title: item.title,
        children: item.children && item.children.length ? item.children : undefined
    }));
});
// 获取角色列表的方法
const fetchRoleList = async () => {
    try {
        const response = await roleList();
        if (response.code === 200) {
            dataList.value = response.data.roles.map(item => ({ ...item, name: item.name }));
        } else {
            ElMessage.error(response.message || '获取角色列表失败');
        }
    } catch (error) {
        ElMessage.error('网络错误，请稍后重试');
    }
};

// 页面加载时获取角色列表
onMounted(() => {
    fetchRoleList();
});

// 打开修改角色对话框
const handleEdit = (row) => {
    role.id = row.id;
    role.role_name = row.name;
    roleVisible.value = true;
};

// 保存角色名称
const saveRoleName = () => {
    roleFormRef.value.validate(async (valid) => {
        if (valid) {
            try {
                await updateRole(role.id, { name: role.role_name });
                ElMessage.success('更新成功');
                roleVisible.value = false;
                await fetchRoleList();
            } catch (error) {
                ElMessage.error('更新失败，请稍后重试');
            }
        }
    });
};


// 打开权限抽屉并加载菜单数据
const openPermissionDrawer = async (row) => {
  try {
    role.id = row.id;

    // 并发执行两个API请求
    const [menuResponse, roleMenuResponse] = await Promise.all([
      menuList(),
      getRoleMenu(row.id)
    ]);

    if (menuResponse.code === 200 && roleMenuResponse.code === 200) {
      menuData.value = menuResponse.data.menus;

      // 提取已分配菜单的ID列表
      const assignedMenuIds = roleMenuResponse.data.menus.map(item => item.menu_id);
      console.log('assignedMenuIds:', assignedMenuIds);

      // 设置权限抽屉为可见，并确保DOM更新后才设置默认选中的节点
      permissionDrawerVisible.value = true;
      
      // 使用 nextTick 确保 DOM 更新后再设置选中状态
      await nextTick();
      
      // 确保 menuTree 已经初始化
      if (menuTree.value) {
        menuTree.value.setCheckedKeys(assignedMenuIds);
      } else {
        console.error('menuTree is not initialized');
      }
    } else {
      ElMessage.error('获取菜单列表或角色已分配菜单失败');
    }
  } catch (error) {
    console.error('网络错误:', error);
    ElMessage.error('网络错误，请稍后重试');
  }
};

// 保存分配的权限
const savePermissions = async () => {
    if (!role.id) {
        ElMessage.error('未指定要分配权限的角色');
        return;
    }
    const checkedKeys = menuTree.value.getCheckedKeys(true); // true 表示包含半选状态的节点
    // const allCheckedKeys = getAncestorsAndSelf(menuData.value, checkedKeys);
    console.log('半选节点:', checkedKeys);
    // console.log('传递的值:', allCheckedKeys);
    try {
        await saveRoleMenu( {role_id:role.id, menu_ids: checkedKeys });
        ElMessage.success('权限分配成功');
        permissionDrawerVisible.value = false;
    } catch (error) {
        console.error('保存权限时出错:', error);
        ElMessage.error('权限分配失败，请稍后重试');
    }
};

// 删除角色
const handleDelete = (row) => {
   console.log('删除角色:', row);
};

// 添加角色
const handleAddRole = () => {
    // 实现添加角色逻辑
    console.log('添加角色');
};
</script>

<style scoped>
.header-actions {
    display: flex;
    align-items: center;
    margin-bottom: 20px;
}

.el-table {
    border: 1px solid #ebeef5;
    border-radius: 4px;
    overflow: hidden;
}
</style>