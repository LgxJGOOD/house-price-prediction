import router from '@/router';
import nprogress from 'nprogress';
import "nprogress/nprogress.css";
import useUserStore from '@/store/modules/user';

nprogress.configure({ showSpinner: false });


// 全局前置守卫
router.beforeEach(async (to, from, next) => {
  document.title = to.meta.title || 'Default Title'; 
  nprogress.start();

  const userStore = useUserStore();
  const token = localStorage.getItem('token');

  if (token) {
    await userStore.getRoleMenus();
    // 登录成功后处理
    if (to.path === '/login') {
      next({ path: '/admin/home' }); 
    }
    else {
      // 特殊处理：图表分析的子菜单继承父级权限
      const chartAnalysisChildren = ['dataAnalysisArea', 'dataAnalysisQuantity', 'dataAnalysisHouse', 'dataAnalysisPrice'];
      let hasPermission = false;
        
      if (chartAnalysisChildren.includes(to.name)) {
        // 如果访问的是图表分析子菜单，检查父级 dataAnalysis 权限
        hasPermission = userStore.roleMenus.includes('dataAnalysis');
      } else {
        // 其他菜单正常检查
        hasPermission = userStore.roleMenus.includes(to.name);
      }
        
      console.log('Route permission check:', to.name, 'hasPermission:', hasPermission, 'roleMenus:', userStore.roleMenus);
        
      if (hasPermission || !to.meta.requiresAuth) {
        next();
      } else {
        // 用户没有权限，重定向至 403 页面
        next({ path: '/403', query: { redirect: to.fullPath } });
      }
    }
  } else {
    // 用户未登录时的处理
    if (to.path === '/login'  ||to.path === '/register'|| to.path === '/admin/home') {
      // 如果用户未登录但访问的是登录界面或首页，允许访问
      next();
    } else {
      // 用户未登录且尝试访问其他页面，重定向至登录界面，并保留当前试图访问的路径作为查询参数
      next({ path: '/login', query: { redirect: to.fullPath } });
    }
  }
});

// 全局后置守卫
router.afterEach(() => {
  nprogress.done();
});