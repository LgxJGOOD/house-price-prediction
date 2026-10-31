<template>
    <div class="screen-container" :style="containerStyle">
      <header class="screen-header">
        <div>
          <img src="http://127.0.0.1:8899/upload/header_border_dark.png" alt="">
        </div>
        <span class="logo">
          <div>
            <el-button type="primary" tag="a" href="/">首页</el-button>
          </div>
        </span>
        <span class="title">森林资源大屏可视化系统</span>
        <div class="title-right">
          <span class="datetime">{{ currentTime }}</span>
        </div>
      </header>
      <div class="screen-body">
        <section class="screen-left">
          <div id="left-top">
            <Radar></Radar>
          </div>
          <div id="left-bottom">
            <barCountry></barCountry>
          </div>
        </section>
        <section class="screen-middle">
          <div id="middle-top">
            <Map></Map>
          </div>
          <div id="middle-bottom">
            <barCity></barCity>
          </div>
        </section>
        <section class="screen-right">
          <div id="right-top">
            <!-- 占比图表 -->
            <pie></pie>
          </div>
          <div id="right-bottom">
            <Line></Line>
          </div>
        </section>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted, onUnmounted } from 'vue';
  import Radar from '@/components/radarView.vue'
  import barCity from '@/components/barView.vue'
  import pie from '@/components/pieView.vue'
  import barCountry from '@/components/bar02View.vue'
  import Line from '@/components/lineView.vue'
  import Map from '@/components/mapView.vue'
  
  const currentTime = ref(new Date().toLocaleString());
  let intervalId;
  
  function updateTime() {
    currentTime.value = new Date().toLocaleString();
  }
  
  onMounted(() => {
    intervalId = setInterval(updateTime, 1000); // 每隔1秒更新一次时间
  });
  
  onUnmounted(() => {
    clearInterval(intervalId); // 清除定时器以防止内存泄漏
  });
  </script>
  
  <style lang="scss" scoped>
  // 全屏样式的定义
  .screen-container {
    width: 100%;
    height: 100vh;
    padding: 0 20px;
    background-color: #79b3f1;
    color: #fff;
    box-sizing: border-box;
  }
  .screen-header {
    width: 100%;
    height: 64px;
    font-size: 20px;
    position: relative;
    > div {
      img {
        width: 100%;
      }
    }
    .title {
      position: absolute;
      left: 50%;
      top: 50%;
      font-size: 20px;
      transform: translate(-50%, -50%);
    }
    .title-right {
      display: flex;
      align-items: center;
      position:absolute;
      right: 0px;
      top: 50%;
      transform: translateY(-80%);
    }
    .qiehuan {
      width: 28px;
      height: 21px;
      cursor: pointer;
    }
    .datetime {
      font-size: 15px;
      margin-left: 10px;
    }
    .logo {
      position: absolute;
      left: 0px;
      top: 50%;
      transform: translateY(-80%);
      img {
        height: 35px;
        width: 40px;
      }
    }
  }
  .screen-body {
    width: 100%;
    height: 100%;
    display: flex;
    margin-top: 10px;
    .screen-left {
      height: 100%;
      width: 27.6%;
      #left-top {
        height: 53%;
        position: relative;
      }
      #left-bottom {
        height: 31%;
        margin-top: 25px;
        position: relative;
      }
    }
    .screen-middle {
      height: 100%;
      width: 41.5%;
      margin-left: 1.6%;
      margin-right: 1.6%;
      #middle-top {
        width: 100%;
        height: 56%;
        position: relative;
      }
      #middle-bottom {
        margin-top: 25px;
        width: 100%;
        height: 28%;
        position: relative;
      }
    }
    .screen-right {
      height: 100%;
      width: 27.6%;
      #right-top {
        height: 46%;
        position: relative;
      }
      #right-bottom {
        height: 38%;
        margin-top: 25px;
        position: relative;
      }
    }
  }
  section > div{
    border: 1px solid rgb(114, 73, 73);
  }
  </style>
  