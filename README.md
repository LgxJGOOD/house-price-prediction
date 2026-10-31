# 九江市二手房数据可视化与价格预测系统

基于 Django + Vue 的二手房数据平台：房源数据入库、多维度可视化分析、价格预测，配套后台管理。

## 技术栈

| 层 | 技术 |
|---|---|
| 后端 | Django、PyMySQL |
| 前端 | Vue 2、Element UI、ECharts、Axios |
| 数据 | MySQL（附带建表与样例数据 `db/old_house_data.sql`） |
| 建模 | 特征工程 + 回归模型预测房源总价 |

## 功能

**数据侧**
- 房源列表：分页、多条件筛选（区域 / 户型 / 面积区间 / 价格区间）
- 数据详情：单房源历史与周边对比

**可视化侧（ECharts）**
- 区域均价分布、面积-价格散点、户型占比、挂牌量趋势
- 价格预测页：输入面积、户型、楼层、朝向等条件，输出预测总价与参考区间

**管理侧**
- 房源维护（增删改查）、上传数据、账号与角色权限

## 目录结构

```
djangoproject/
├── manage.py
├── djangoproject/        # 配置：settings.py、myconfig.py（数据库连接，走环境变量）
├── ershoufang_app/       # 房源应用：模型、视图、预测逻辑
├── adminuserapp/         # 后台账号与权限
├── vueweb/               # Vue 前端工程
├── db/old_house_data.sql # 建表 + 样例数据
└── upload/               # 上传文件目录
```

## 运行

```bash
# 1. 建库导数据
mysql -u root -p < djangoproject/db/old_house_data.sql

# 2. 后端
pip install -r djangoproject/requirements.txt
cd djangoproject
cp ../.env.example .env        # 填 DB_PASSWORD、DJANGO_SECRET_KEY
python manage.py migrate
python manage.py runserver

# 3. 前端
cd vueweb
npm install
npm run serve
```

## 说明

数据库密码与 Django `SECRET_KEY` 均通过环境变量读取（见 `.env.example`），仓库不含明文凭据。

## 联系

刘冠湘 · 湖南第一师范学院 · 人工智能专业 · 2027 届 · sxangus@qq.com
