<template>
    <div class="word-cloud-container">
    
      <el-card class="word-cloud-card">
        <div class="card-title">
          <span>长沙城市评论词云图</span>
        </div>
        <img src="http://localhost:8899/upload/长沙.png" alt="长沙城市评论词云图" class="word-cloud-image">
      </el-card>

      <el-card class="word-cloud-card">
        <div class="card-title">
          <span>广州城市评论词云图</span>
        </div>
        <img src="http://localhost:8899/upload/广州.png" alt="广州城市评论词云图" class="word-cloud-image">
      </el-card>
      <el-card class="word-cloud-card">
        <div class="card-title">
          <span>福州城市评论词云图</span>
        </div>
        <img src="http://localhost:8899/upload/福州.png" alt="福州城市评论词云图" class="word-cloud-image">
      </el-card>



      <el-card class="word-cloud-card">
        <div class="card-title">
          <span>一点点评论词云图</span>
        </div>
        <img src="http://localhost:8899/upload/一点点.png" alt="一点点评论词云图" class="word-cloud-image">
      </el-card>

      <el-card class="word-cloud-card">
        <div class="card-title">
          <span>古茗评论词云图</span>
        </div>
        <img src="http://localhost:8899/upload/古茗.png" alt="古茗评论词云图" class="word-cloud-image">
      </el-card>
      <el-card class="word-cloud-card">
        <div class="card-title">
          <span>霸王茶姬评论词云图</span>
        </div>
        <img src="http://localhost:8899/upload/霸王茶姬.png" alt="霸王茶姬评论词云图" class="word-cloud-image">
      </el-card>
    </div>
  </template>
  
  <style scoped>
  /* 容器样式 */
  .word-cloud-container {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 20px; /* 卡片之间的间距 */
    padding: 20px;
  }
  
  /* 卡片样式 */
  .word-cloud-card {
    width: 450px; /* 卡片宽度 */
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* 卡片阴影 */
    transition: box-shadow 0.3s ease;
  }
  
  /* 鼠标悬停时卡片阴影加深 */
  .word-cloud-card:hover {
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
  }
  
  /* 卡片标题样式 */
  .card-title {
    text-align: center;
    padding: 10px;
    font-size: 18px;
    font-weight: bold;
    color: #333;
    border-bottom: 1px solid #eee; /* 标题底部边框 */
  }
  
  /* 词云图图片样式 */
  .word-cloud-image {
    width: 100%;
    height: auto;
    border-bottom-left-radius: 8px;
    border-bottom-right-radius: 8px;
  }
  </style>