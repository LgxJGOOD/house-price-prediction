<template>
  <div style="margin-top: 80px;">
    <el-breadcrumb separator=">">
      <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
      <el-breadcrumb-item>
        <a to="{ path: '/travel/list' }">景区景点</a>
      </el-breadcrumb-item>
      <el-breadcrumb-item>景点列表</el-breadcrumb-item>
    </el-breadcrumb>
  </div>
  <hr>
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
    </div>

    <!-- 表格组件 -->
    <el-table :data="dataList" style="width: 100%; margin-top: 20px;" border>
      <el-table-column label="景点图片" align="center" width="100">
        <template #default="scope">
          <img :src="scope.row.coverImageUrl" alt="景点图片" class="avatar1">
        </template>
      </el-table-column>
      <el-table-column prop="poiName" label="景点名称" width="200" />
      <el-table-column prop="shortFeatures" label="简介" width="220" />
      <el-table-column label="价格" width="90">
        <template #default="scope">
          <span :style="{
            color: '#f60' ,
            fontWeight: '500',
            fontSize: '20px'
          }">
            {{ scope.row.price === 0 ? '免费' : '￥'+scope.row.price }}
          </span>
        </template>
      </el-table-column>
      <el-table-column prop="districtName" label="城市" width="60" />
      <el-table-column prop="zoneName" label="地址" width="180" />
      <el-table-column label="等级" width="80">
        <template #default="scope">
          <span :style="{
            color: '#3263a6' ,
            fontWeight: '400',
            fontSize: '20px'
          }">
            {{  scope.row.sightLevelStr === '' ? '无' : scope.row.sightLevelStr }} 
          </span>
        </template>
      </el-table-column>
      <el-table-column prop="commentScore" label="评分" width="60" align="center" />
      <el-table-column prop="heatScore" label="热度" width="60" />
      <el-table-column prop="tagNameList" label="标签" width="160" />
      <el-table-column prop="distanceStr" label="景点距离" width="160" />
      <el-table-column label="详情" align="center">
        <template #default="scope">
          <el-button type="primary" size="small" icon="Edit" @click="GoRow(scope.row)">详情</el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 分页 -->
    <el-pagination background layout="prev, pager, next, sizes, ->,jumper, total" :page-size="searchParams.pagesize"
      v-model:current-page="searchParams.pagenum" :page-sizes="[10, 15, 20, 25, 30]" :total="total"
      @size-change="handleSizeChange" @current-change="fetchData" style="margin-top: 20px;" />
  </el-card>
</template>

<script setup>
import { reactive, ref, onMounted } from 'vue';
import { traveltList } from '@/api/data/index.js';
import { useRouter } from 'vue-router';
const router = useRouter();

// 定义响应式数据
const searchParams = reactive({
  keyWord: '',
  pagenum: 1,
  pagesize: 15,
});

const dataList = ref([]);
const total = ref(0);

// 获取数据的方法
const fetchData = () => {
  traveltList(searchParams).then((res) => {
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
const GoRow = (row) => {
  router.push({
    path: `/travel/detail/${row.id}`
  });
};



// 组件挂载时获取数据
onMounted(() => {
  fetchData();
});
</script>

<style scoped>
.box-card {
  margin-top: 10px;
}

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

.avatar1 {
  width: 60px;
  height: 60px;
  /* border-radius: 50%; */
  object-fit: cover;
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