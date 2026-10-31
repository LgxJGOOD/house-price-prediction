import request from '@/utils/request'

// 用户注册接口
export const register = (data) => {
  return request.post('/register/', data);
};

// 用户登录接口
export const login = (data) => {
  return request.post('/login/', data);
};

// 获取用户信息接口
export const getUserInfo = () => {
  return request.get('/profile/');
};

// 用户注销接口
export const logout = () => {
  return request.post('/logout/');
};


//用户列表
export const userList = (params) => {
  return request.get('/users/list/', {
    params: {
      query: params.keyWord || '',
      pagesize: params.pagesize,
      pagenum: params.pagenum,
    },
  });
};


//添加用户
export const userAdd = (data) => {
  return request.post('/users/create/', data);
};

//修改用户
export const userEdit = (data) => {
  return request.put(`users/${data.id}/update/`, data);
};
//删除用户
export const userDel = (id) => {
  return request.delete(`users/${id}/delete/`);
};
//修改用户状态
export const userEditState = ({ id, state }) => {
  return request.put(`users/${id}/state/${state}/`);
};

//重置密码12345678
export const userResetpsd = (data) => {
  return request.post('change/psd/',data);
};


//获取角色列表
export const roleList = () => {
  return request.get('/roles/');
};

//更新角色名称 
export const updateRole= (id ,data) => {
  return request.put(`/roles/${id}/`,data);
};

//获取菜单列表

export const menuList = () => {
  return request.get('/menus/');
};
//保存权限配置

export const saveRoleMenu = (data) => {
  return request.post('menus/assign-menus-to-role/', data);
};
//根据角色获取菜单
export const getRoleMenu = (id) => {
  return request.get(`menus/get-menus-by-role/${id}/`);
};
