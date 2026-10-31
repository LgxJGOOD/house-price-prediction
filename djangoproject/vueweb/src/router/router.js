export const constantRoutes = [
    //登录
    {
        path: '/front/login',
        name: 'login',
        component: () => import("../views/login/indexView.vue"),
        meta: {
            title: '登录',
            hidden: true,
            icon: '',
            requiresAuth: false,
            role: []
        }
    },

        //后台登录
        {
            path: '/login',
            name: 'adminlogin',
            component: () => import("../views/login/adminIndexView.vue"),
            meta: {
                title: '登录',
                hidden: true,
                icon: '',
                requiresAuth: false,
                role: []
            }
        },

    //注册
    {
        path: '/register',
        name: 'register',
        component: () => import("../views/register/registerView.vue"),
        meta: {
            title: '注册',
            hidden: true,
            icon: '',
            requiresAuth: false,
            role: []
        }
    },
    {
        path: '/front',
        name: 'Base',
        component: () => import("../views/front/baseView.vue"),
        meta: {
            title: 'base',
            hidden: false,
            icon: 'HomeFilled',
            requiresAuth: false,
            role: [0,1,2]
        },
        redirect: '/front/index',
        children: [
            {
                path: '/front/index',
                name: 'index',
                component: () => import("../views/front/index/MainContent.vue"),
                meta: {
                    title: '前台首页',
                    hidden: false,
                    icon: 'HomeFilled',
                    requiresAuth: false,
                    role: [0,1,2]
                }
            },
            {
                path: '/front/travel/list',
                name: 'TravelData',
                component: () => import("../views/front/travel/travelListView.vue"),
                meta: {
                    title: '景点列表',
                    hidden: false,
                    icon: 'HomeFilled',
                    requiresAuth: false,
                    role: [0,1,2]
                }
            },
            {
                path: '/front/travel/detail/:id',
                name: 'DetailData',
                component: () => import("../views/front/travel/travelDetailView.vue"),
                meta: {
                    title: '景点详情',
                    hidden: false,
                    icon: 'HomeFilled',
                    requiresAuth: false,
                    role: [0,1,2]
                }
            },
            {
                path: '/front/travel/echarts/',
                name: 'EchartsTravel',
                component: () => import("../views/front/travel/travelEchartsView.vue"),
                meta: {
                    title: '图表分析',
                    hidden: false,
                    icon: 'HomeFilled',
                    requiresAuth: false,
                    role: [0,1,2]
                }
            },
            
            {
                path: '/front/data/visual/map',
                name: 'VisualMap',
                component: () => import("../views/front/travel/echartsMapView.vue"),
                meta: {
                    title: '景点地图',
                    hidden: false,
                    icon: 'DataLine',
                    requiresAuth: false,
                    role: [0,1,2]
                }
            }
        ]
    },

    //后台首页
    {
        path: '/admin',
        name: 'layout',
        component: () => import("../views/layout/indexView.vue"),
        meta: {
            title: 'layout',
            hidden: false,
            icon: 'HomeFilled',
            requiresAuth: false,
            role: [0,1,2]
        },
        redirect: '/admin/home',
        children: [
            {
                path: '/admin/home',
                name: 'home',
                component: () => import("../views/home/indexView.vue"),
                meta: {
                    title: '首页',
                    hidden: false,
                    icon: 'HomeFilled',
                    requiresAuth: false,
                    role: [0,1,2]
                }
            }
        ]
    },
    //大屏
    // {
    //     path: '/admin/screen',
    //     name: 'Screen',
    //     component: () => import("../views/screen/indexView.vue"),
    //     meta: {
    //         title: '数据大屏',
    //         hidden: false,
    //         icon: 'Platform',
    //         requiresAuth: false,
    //         role: [0,1,2]
    //     }

    // },
    
    //个人中心
    {
        path: '/admin/users',
        name: 'Users',
        component: () => import("../views/layout/indexView.vue"),
        meta: {
            title: '个人设置',
            hidden: false,
            icon: 'Lock',
            requiresAuth: true,
            role: [1,2]
        },
        children: [
            {
                path: '/admin/users/user',
                name: 'UserCenter',
                component: () => import("../views/user/indexView.vue"),
                meta: {
                    title: '个人中心',
                    hidden: false,
                    icon: 'User',
                    requiresAuth: true,
                    role: [1,2]
                }
            },
          

        ]
    },
    //数据分析
    {
        path: '/admin/data/analysis',
        name: 'Analysis',
        component: () => import("../views/layout/indexView.vue"),
        meta: {
            title: '数据分析',
            hidden: false,
            icon: 'DataLine',
            requiresAuth: true,
            role: [0,1,2]
        },
        children: [
            {
                path: '/admin/data/analysis/data-list',
                name: 'Datalist',
                component: () => import("../views/data/dataListView.vue"),
                meta: {
                    title: '数据信息',
                    hidden: false,
                    icon: 'List',
                    requiresAuth: true,
                    role: [0,1,2]
                },
            },
            {
                path: '/admin/data/analysis/echarts',
                name: 'dataAnalysis',
                meta: {
                    title: '图表分析',
                    hidden: false,
                    icon: 'List',
                    requiresAuth: true,
                    role: [0,1,2]
                },
                children: [
                    {
                        path: '/admin/data/analysis/echarts/area',
                        name: 'dataAnalysisArea',
                        component: () => import("../views/data/areaAnalysisView.vue"),
                        meta: {
                            title: '面积分析',
                            hidden: false,
                            icon: 'OfficeBuilding',
                            requiresAuth: true,
                            role: [0,1,2]
                        },
                    },
                    {
                        path: '/admin/data/analysis/echarts/quantity',
                        name: 'dataAnalysisQuantity',
                        component: () => import("../views/data/quantityAnalysisView.vue"),
                        meta: {
                            title: '数量分析',
                            hidden: false,
                            icon: 'DataLine',
                            requiresAuth: true,
                            role: [0,1,2]
                        },
                    },
                    {
                        path: '/admin/data/analysis/echarts/house',
                        name: 'dataAnalysisHouse',
                        component: () => import("../views/data/houseAnalysisView.vue"),
                        meta: {
                            title: '房屋分析',
                            hidden: false,
                            icon: 'HomeFilled',
                            requiresAuth: true,
                            role: [0,1,2]
                        },
                    },
                    {
                        path: '/admin/data/analysis/echarts/price',
                        name: 'dataAnalysisPrice',
                        component: () => import("../views/data/priceAnalysisView.vue"),
                        meta: {
                            title: '房价分析',
                            hidden: false,
                            icon: 'Money',
                            requiresAuth: true,
                            role: [0,1,2]
                        },
                    },
                ]
            },
            {
                path: '/admin/data/price/projection',
                name: 'priceProjection',
                component: () => import("../views/data/priceProjectionView.vue"),
                meta: {
                    title: '价格预测',
                    hidden: false,
                    icon: 'TrendCharts',
                    requiresAuth: false,
                    role: [0,1,2]
                }
            },

           
        ]
    },
    //404
    {
        path: '/404',
        name: '404',
        component: () => import("../views/error/404/indexView.vue"),
        meta: {
            title: '404',
            hidden: true,
            icon: '',
            requiresAuth: false,
            role: [0,]
        }

    },

      //403
      {
        path: '/403',
        name: '403',
        component: () => import("../views/error/403/indexView.vue"),
        meta: {
            title: '403',
            hidden: true,
            icon: '',
            requiresAuth: false,
            role: [0,]
        }

    },
     //权限管理
     {
        path: '/admin/acl',
        name: 'Acl',
        component: () => import("../views/layout/indexView.vue"),
        meta: {
            title: '权限管理',
            hidden: false,
            icon: 'Lock',
            requiresAuth: true,
            role: [1,]
        },
        children: [
            {
                path: '/admin/acl/user',
                name: 'User',
                component: () => import("../views/acl/user/indexView.vue"),
                meta: {
                    title: '用户管理',
                    hidden: false,
                    icon: 'User',
                    requiresAuth: true,
                    role: [1,]
                }
            },
            {
                path: '/admin/acl/role',
                name: 'Role',
                component: () => import("../views/acl/role/indexView.vue"),
                meta: {
                    title: '角色管理',
                    hidden: false,
                    icon: 'UserFilled',
                    requiresAuth: true,
                    role: [1,]
                }
            },
            {
                path: '/admin/acl/permission',
                name: 'Permission',
                component: () => import("../views/acl/permission/indexView.vue"),
                meta: {
                    title: '菜单管理',
                    hidden: true,
                    icon: 'Menu',
                    requiresAuth: true,
                    role: [0,]
                }
            },
        ]
    },
    //任意路由匹配
    {
        path: '/:pathMatch(.*)*',
        name: 'notFound',
        redirect: '/404',
        meta: {
            title: 'any',
            hidden: true,
            icon: 'DataLine',
            requiresAuth: false,
            role: [0,]
        }
    }


];


