import { defineStore } from 'pinia';
import { login, logout,getRoleMenu } from '@/api/user';
import { constantRoutes } from '@/router/router';
const updateAuthInfo = (store, data) => {
  const userKeys = ['id', 'username', 'email', 'nickname', 'gender', 'is_active', 'is_superuser', 'bio', 'avatar', 'role_id', 'role_name', 'last_login'];
  
  store.token = data.access;
  localStorage.setItem('token', data.access);
  
  if (data.refresh) {
    store.refresh = data.refresh;
    localStorage.setItem('refresh', data.refresh);
  }

  userKeys.forEach(key => {
    if (Reflect.has(data.user, key)) { 
      store[key] = data.user[key];
      localStorage.setItem(key, store[key]);
    }
  });
  if (store.role_id) {
    store.getRoleMenus();
  }
};


const clearAuthInfo = (store) => {
  const keys = ['token', 'refresh', 'id', 'username', 'email', 'nickname', 'gender', 'is_active', 'is_superuser', 'bio', 'avatar', 'role_id', 'role_name','last_login','roleMenus'];
  keys.forEach(key => {
    store[key] = '';
    localStorage.removeItem(key);
  });
};

const useUserStore = defineStore('User', {
  state: () => ({
    token: localStorage.getItem('token') || '',
    refresh: localStorage.getItem('refresh') || '', 
    id: localStorage.getItem('id') || '',
    username: localStorage.getItem('username') || '',
    email: localStorage.getItem('email') || '',
    nickname: localStorage.getItem('nickname') || '',
    gender: localStorage.getItem('gender') || null,
    is_active: JSON.parse(localStorage.getItem('is_active') || 'false'),
    is_superuser: JSON.parse(localStorage.getItem('is_superuser') || 'false'),
    bio: localStorage.getItem('bio') || null,
    avatar: localStorage.getItem('avatar') || null,
    role_id: localStorage.getItem('role_id') || null,
    role_name: localStorage.getItem('role_name') || null,
    last_login: localStorage.getItem('last_login') || null,
    menuRoutes: constantRoutes,
    roleMenus: JSON.parse(localStorage.getItem('roleMenus')) || []
  }),
  
  actions: {
    async userLogin(data) {
      try {
        const result = await login(data);
        if (result.code === "200") {
          updateAuthInfo(this, result.data);
          return Promise.resolve(result);
        }
        throw new Error(result.message);
      } catch (error) {
        return Promise.reject(error);
      }
    },

    async useLogout() {
      try {
        const result = await logout();
        console.log("result",result.code);
        if ([200, 401, 403].includes(Number(result.code))) {
          clearAuthInfo(this);
          return Promise.resolve(result);
        }
        throw new Error(result.message);
      } catch (error) {
        return Promise.reject(error);
      }
    },

//获取用户角色菜单
    async getRoleMenus() {
      if (!this.role_id) {
        this.roleMenus = [];
        localStorage.setItem('roleMenus', JSON.stringify([]));
        return;
      }
      try {
        const response = await getRoleMenu(this.role_id);
        if (response.code === 200) {
          this.roleMenus = response.data.menus.map(menu => menu.name);
          localStorage.setItem('roleMenus', JSON.stringify(this.roleMenus));
        }
        else {
          throw new Error(response.message || 'Failed to fetch role menus');}
      } catch (error) {
        console.error('Failed to fetch role menus:', error);
        this.roleMenus = [];
        localStorage.setItem('roleMenus', JSON.stringify([]));
      }
    },

  },
});

export default useUserStore;