<template>
  <el-card class="box-card">
    <!-- 简单轮播图 -->
    <el-carousel height="300px" style="margin-bottom: 20px;">
      <el-carousel-item v-for="(item, index) in carouselList" :key="index">
        <div class="carousel-item">
          <img :src="item.imageUrl" :alt="item.title" class="carousel-image">
          <div class="carousel-title">{{ item.title }}</div>
        </div>
      </el-carousel-item>
    </el-carousel>
    
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
      <!-- <el-table-column label="图片" align="center" width="100">
        <template #default="scope">
          <img :src="scope.row.img_url" alt="图片" class="avatar1">
        </template>
      </el-table-column> -->
      <el-table-column prop="city" label="城市" width="60" />
      <el-table-column prop="title" label="标题" width="220" />
      <el-table-column prop="position_info" label="房屋位置" width="100" />
      <el-table-column prop="house_info" label="房屋信息" width="220" />
      <el-table-column label="房屋总价" width="90">
        <template #default="scope">
          <span :style="{
            color: '#fa5741' ,
            fontWeight: '700',
            fontSize: '16px'
          }">
            {{  scope.row.total_price }}万
          </span>
        </template>
      </el-table-column>
      <el-table-column prop="unit_price" label="房屋单价" width="110" />
      <el-table-column prop="house_orientation" label="房屋朝向" width="90" />
      <el-table-column prop="house_area" label="房屋面积" width="100" />
      <el-table-column prop="house_decorate" label="装修" width="100" />
      <el-table-column label="操作" align="center">
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
import { houseList } from '@/api/data/index.js';
import { Search } from '@element-plus/icons-vue';

// 定义响应式数据
const searchParams = reactive({
  keyWord: '',
  pagenum: 1,
  pagesize: 10,
});

const dataList = ref([]);
const total = ref(0);

// 简单轮播图数据
const carouselList = ref([
  {
    imageUrl: new URL('@/assets/banner/444.jpg', import.meta.url).href,
    title: '精品房源推荐'
  },
  {
    imageUrl: new URL('@/assets/banner/333.jpg', import.meta.url).href,
    title: '特价好房'
  },
  {
    imageUrl: new URL('@/assets/banner/222.jpg', import.meta.url).href,
    title: '新盘上线'
  },
  {
    imageUrl: new URL('@/assets/banner/111.jpg', import.meta.url).href,
    title: '热门推荐'
  }
]);


const GoRow = (row) => {
  if (row.detail_href) {
    window.open(row.detail_href, '_blank');
  }
};
// 获取数据的方法
const fetchData = () => {
  houseList(searchParams).then((res) => {
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



// 组件挂载时获取数据
onMounted(() => {
  fetchData();
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

/* 简单轮播图样式 */
.el-carousel {
  margin-bottom: 20px;
}

.carousel-item {
  width: 100%;
  height: 100%;
  position: relative;
}

.carousel-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 8px;
}

.carousel-title {
  position: absolute;
  bottom: 20px;
  left: 0;
  right: 0;
  text-align: center;
  color: white;
  font-size: 24px;
  font-weight: bold;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
  z-index: 10;
}
</style>


