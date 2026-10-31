<template>
    <div>
      <el-carousel :interval="4000" type="card" height="300px">
        <el-carousel-item v-for="(item, index) in carouselImages" :key="index">
          <img :src="item" alt="carousel" style="width: 100%; height: 100%; object-fit: cover;">
        </el-carousel-item>
      </el-carousel>
      <div class="house-list">
        <el-row :gutter="20">
          <el-col :span="8" v-for="(house, index) in houses" :key="index">
            <el-card :body-style="{ padding: '0px' }">
              <img :src="house.image" class="image">
              <div style="padding: 14px;">
                <span>{{ house.title }}</span>
                <div class="bottom clearfix">
                  <time class="time">{{ house.date }}</time>
                  <el-button type="text" class="button">查看详情</el-button>
                </div>
              </div>
            </el-card>
          </el-col>
        </el-row>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  
  
  // const carouselImages = ref([
  //  require('@/assets/banner/bannerV1.jpg'),
  //  require('@/assets/banner/bannerV2.jpg'),
  //  require('@/assets/banner/bannerV3.jpg')
  // ]);
  
  const imageContext = require.context('@/assets/banner', false, /\.(jpg|jpeg|png|gif)$/);
  const carouselImages = ref(imageContext.keys().map(key => imageContext(key)));
  
  const houses = ref([
    { title: '房屋1', date: '2023-10-01', image: 'https://via.placeholder.com/300' },
    { title: '房屋2', date: '2023-10-02', image: 'https://via.placeholder.com/300' },
    { title: '房屋3', date: '2023-10-03', image: 'https://via.placeholder.com/300' },
    { title: '房屋4', date: '2023-10-04', image: 'https://via.placeholder.com/300' },
    { title: '房屋5', date: '2023-10-05', image: 'https://via.placeholder.com/300' },
    { title: '房屋6', date: '2023-10-06', image: 'https://via.placeholder.com/300' },
    { title: '房屋7', date: '2023-10-07', image: 'https://via.placeholder.com/300' },
    { title: '房屋8', date: '2023-10-08', image: 'https://via.placeholder.com/300' },
    { title: '房屋9', date: '2023-10-09', image: 'https://via.placeholder.com/300' }
  ]);
  
  const handleSelect = (key, keyPath) => {
    console.log(key, keyPath);
  };
  </script>
  
  <style scoped lang="scss">
  .el-main {
    padding-top: 60px; /* 确保内容不会被固定头部遮挡 */
  }
  .house-list {
    margin-top: 320px; /* 根据轮播图的高度调整 */
  }
  .time {
    font-size: 13px;
    color: #999;
  }
  .bottom {
    margin-top: 13px;
    line-height: 12px;
  }
  .button {
    padding: 0;
    float: right;
  }
  .image {
    width: 100%;
    display: block;
  }
  .clearfix:before,
  .clearfix:after {
    display: table;
    content: "";
  }
  .clearfix:after {
    clear: both;
  }
  </style>