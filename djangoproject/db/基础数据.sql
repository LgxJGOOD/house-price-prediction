INSERT INTO `t_role` (`id`, `created_at`, `updated_at`, `name`) VALUES (1, '2025-1-14 12:38:53', '2025-1-14 12:38:50', '管理员');
INSERT INTO `t_role` (`id`, `created_at`, `updated_at`, `name`) VALUES (2, '2025-1-14 12:39:10', '2025-1-14 06:08:13', '普通用户1');
INSERT INTO `t_role` (`id`, `created_at`, `updated_at`, `name`) VALUES (3, '2025-1-14 12:39:30', '2025-1-14 12:39:27', '临时用户');




INSERT INTO `t_menu` VALUES ('1', '2025-01-14 14:11:09.000000', '2025-01-14 14:11:14.000000', '登录', '/login', '1', '0', null, 'login', null);
INSERT INTO `t_menu` VALUES ('2', '2025-01-14 14:11:53.000000', '2025-01-14 14:11:56.000000', 'layout', '/admin', '1', '1', 'HomeFilled', 'layout', null);
INSERT INTO `t_menu` VALUES ('3', '2025-01-14 14:12:39.000000', '2025-01-14 14:12:42.000000', '首页', '/admin/home', '2', '1', 'HomeFilled', 'home', '2');
INSERT INTO `t_menu` VALUES ('4', '2025-01-14 14:17:28.000000', '2025-01-14 14:17:30.000000', '数据大屏', '/admin/screen', '1', '0', 'Platform', 'Screen', null);
INSERT INTO `t_menu` VALUES ('5', '2025-01-14 14:49:09.000000', '2025-01-14 14:49:06.000000', '个人设置', '/admin/users', '1', '1', null, 'Users', null);
INSERT INTO `t_menu` VALUES ('6', '2025-01-14 14:50:11.000000', '2025-01-14 14:50:08.000000', '个人中心', '/admin/users/user', '2', '1', null, 'UserCenter', '5');
INSERT INTO `t_menu` VALUES ('7', '2025-01-14 14:51:07.000000', '2025-01-14 14:51:03.000000', '权限管理', '/admin/acl', '1', '1', null, 'Acl', null);
INSERT INTO `t_menu` VALUES ('8', '2025-01-14 14:51:16.000000', '2025-01-14 14:51:18.000000', '用户管理', '/admin/acl/user', '2', '1', null, 'User', '7');
INSERT INTO `t_menu` VALUES ('9', '2025-01-14 14:52:57.000000', '2025-01-14 14:52:54.000000', '角色管理', '/admin/acl/role', '2', '1', null, 'Role', '7');
INSERT INTO `t_menu` VALUES ('10', '2025-01-14 14:53:04.000000', '2025-01-14 14:53:07.000000', 'any', '/:pathMatch(.*)*', '1', '0', null, 'notFound', null);
INSERT INTO `t_menu` VALUES ('11', '2025-01-14 14:54:22.000000', '2025-01-14 14:54:24.000000', '404', '/404', '1', '0', null, '404', null);
INSERT INTO `t_menu` VALUES ('13', '2025-02-07 18:33:40.000000', '2025-02-07 18:33:35.000000', '数据分析', '/admin/data/analysis', '1', '1', null, 'Analysis', null);
INSERT INTO `t_menu` VALUES ('14', '2025-02-07 18:35:57.000000', '2025-02-07 18:35:54.000000', '数据信息', '/admin/data/analysis/datalist', '2', '1', null, 'Datalist', '13');
INSERT INTO `t_menu` VALUES ('15', '2025-02-08 02:30:24.000000', '2025-02-08 02:30:21.000000', '城市信息', '/admin/data/analysis/citylist', '2', '1', null, 'Citylist', '13');
INSERT INTO `t_menu` VALUES ('16', '2025-02-11 20:52:51.000000', '2025-02-11 20:52:54.000000', '我的评论', '/admin/users/user/comments', '2', '0', 'Comment', 'UserComments', '5');
INSERT INTO `t_menu` VALUES ('17', '2025-02-11 20:53:41.000000', '2025-02-11 20:53:44.000000', '我的收藏', '/admin/users/user/collects', '2', '0', 'Collection', 'UserCollects', '5');
INSERT INTO `t_menu` VALUES ('18', '2025-02-11 23:40:15.000000', '2025-02-11 23:40:12.000000', '注册 ', '/register', '1', '0', null, 'register', null);
INSERT INTO `t_menu` VALUES ('19', '2025-02-18 11:36:21.000000', '2025-02-18 11:36:24.000000', '图表分析', '/admin/data/analysis/echarts', '2', '1', null, 'dataAnalysis', '13');
INSERT INTO `t_menu` VALUES ('20', '2025-03-24 04:20:53.000000', '2025-03-24 04:20:56.000000', '词云分析', '/admin/data/analysis/wordCloud', '2', '1', null, 'WordCloud', '13');
INSERT INTO `t_menu` VALUES ('21', '2025-03-24 05:15:39.000000', '2025-03-24 05:15:36.000000', '分析报告', '/admin/dadta/analysis/report', '2', '1', null, 'analysisReport', '13');









INSERT INTO `t_role_menus` VALUES ('14', '1', '3');
INSERT INTO `t_role_menus` VALUES ('4', '1', '6');
INSERT INTO `t_role_menus` VALUES ('1', '1', '8');
INSERT INTO `t_role_menus` VALUES ('2', '1', '9');
INSERT INTO `t_role_menus` VALUES ('18', '1', '14');
INSERT INTO `t_role_menus` VALUES ('19', '1', '15');
INSERT INTO `t_role_menus` VALUES ('22', '1', '16');
INSERT INTO `t_role_menus` VALUES ('23', '1', '17');
INSERT INTO `t_role_menus` VALUES ('30', '1', '19');
INSERT INTO `t_role_menus` VALUES ('31', '1', '20');
INSERT INTO `t_role_menus` VALUES ('32', '1', '21');
INSERT INTO `t_role_menus` VALUES ('33', '2', '3');
INSERT INTO `t_role_menus` VALUES ('34', '2', '6');
INSERT INTO `t_role_menus` VALUES ('35', '2', '14');
INSERT INTO `t_role_menus` VALUES ('36', '2', '15');
INSERT INTO `t_role_menus` VALUES ('37', '2', '16');
INSERT INTO `t_role_menus` VALUES ('38', '2', '17');
INSERT INTO `t_role_menus` VALUES ('39', '2', '19');
INSERT INTO `t_role_menus` VALUES ('40', '2', '20');
INSERT INTO `t_role_menus` VALUES ('41', '2', '21');
