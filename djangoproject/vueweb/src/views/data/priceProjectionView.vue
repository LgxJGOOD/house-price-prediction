<template>
  <div class="prediction-container">
    <el-card class="prediction-card">
      <template #header>
        <div class="card-header">
          <span>🏠 二手房价格预测</span>
        </div>
      </template>

      <el-form :model="formData" label-position="top" size="large">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="房屋面积">
              <div class="input-group">
                <el-input-number 
                  v-model="formData.area" 
                  :min="10" 
                  :max="1000" 
                  :step="0.1"
                  style="width: 100%;"
                />
                <span class="unit">m²</span>
              </div>
            </el-form-item>
          </el-col>

          <el-col :span="12">
            <el-form-item label="房屋构造">
              <div class="room-selector">
                <div class="room-item">
                  <el-button @click="decreaseRoom" circle size="small">−</el-button>
                  <el-input-number 
                    v-model="formData.rooms" 
                    :min="1" 
                    :max="10" 
                    :controls="false"
                    style="width: 80px; text-align: center;"
                  />
                  <el-button @click="increaseRoom" circle size="small">+</el-button>
                  <span class="room-label">室</span>
                </div>
                <div class="room-item">
                  <el-button @click="decreaseHall" circle size="small">−</el-button>
                  <el-input-number 
                    v-model="formData.halls" 
                    :min="1" 
                    :max="10" 
                    :controls="false"
                    style="width: 80px; text-align: center;"
                  />
                  <el-button @click="increaseHall" circle size="small">+</el-button>
                  <span class="room-label">厅</span>
                </div>
              </div>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="建造年份">
              <el-input-number 
                v-model="formData.build_year" 
                :min="1980" 
                :max="2025"
                style="width: 100%;"
              />
            </el-form-item>
          </el-col>

          <el-col :span="12">
            <el-form-item label="楼层">
              <el-select v-model="formData.floor" placeholder="请选择楼层" style="width: 100%;">
                <el-option 
                  v-for="item in floorOptions" 
                  :key="item" 
                  :label="item" 
                  :value="item"
                />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="楼型">
              <el-select v-model="formData.building_type" placeholder="请选择楼型" style="width: 100%;">
                <el-option 
                  v-for="item in buildingTypeOptions" 
                  :key="item" 
                  :label="item" 
                  :value="item"
                />
              </el-select>
            </el-form-item>
          </el-col>

          <el-col :span="12">
            <el-form-item label="装修情况">
              <el-select v-model="formData.decorate" placeholder="请选择装修情况" style="width: 100%;">
                <el-option 
                  v-for="item in decorateOptions" 
                  :key="item" 
                  :label="item" 
                  :value="item"
                />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="区域">
              <el-select v-model="formData.zone" placeholder="请选择区域" style="width: 100%;">
                <el-option 
                  v-for="item in zoneOptions" 
                  :key="item" 
                  :label="item" 
                  :value="item"
                />
              </el-select>
            </el-form-item>
          </el-col>

          <el-col :span="12">
            <el-form-item label="房屋朝向">
              <el-select v-model="formData.orientation" placeholder="请选择房屋朝向" style="width: 100%;">
                <el-option 
                  v-for="item in orientationOptions" 
                  :key="item" 
                  :label="item" 
                  :value="item"
                />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>

        <el-form-item>
          <el-button 
            type="primary" 
            @click="handlePredict" 
            :loading="loading"
            class="predict-btn"
          >
            {{ loading ? '正在智能分析中...' : '开始预测' }}
          </el-button>
        </el-form-item>

        <div v-if="showResult" :class="['result-box', resultType]">
          <div class="result-title">预测总价</div>
          <div class="result-price">
            <small>¥</small>{{ resultPrice }}<small>万元</small>
          </div>
        </div>

        <!-- 区域价格分析 -->
        <div v-if="showZoneAnalysis" class="zone-analysis">
          <el-divider />
          <h3 class="analysis-title">📊 {{ formData.zone }} 价格分析</h3>
          
          <!-- 统计卡片 -->
          <el-row :gutter="20" class="stats-cards">
            <el-col :span="8">
              <el-card shadow="hover" class="stat-card">
                <div class="stat-label">平均总价</div>
                <div class="stat-value price-primary">{{ zoneStats.avg_price }}万</div>
              </el-card>
            </el-col>
            <el-col :span="8">
              <el-card shadow="hover" class="stat-card">
                <div class="stat-label">最高总价</div>
                <div class="stat-value price-danger">{{ zoneStats.max_price }}万</div>
              </el-card>
            </el-col>
            <el-col :span="8">
              <el-card shadow="hover" class="stat-card">
                <div class="stat-label">最低总价</div>
                <div class="stat-value price-warning">{{ zoneStats.min_price }}万</div>
              </el-card>
            </el-col>
          </el-row>

          <!-- 价格分布图表 -->
          <div ref="zoneChartRef" class="zone-chart"></div>
        </div>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue';
import { ElMessage } from 'element-plus';
import { EchartsApi } from '@/api/data/index.js';
import * as echarts from 'echarts';

// 表单数据
const formData = ref({
  area: 100,
  rooms: 3,
  halls: 2,
  build_year: 2015,
  floor: '中楼层',
  building_type: '板楼',
  decorate: '精装',
  zone: '濂溪区',
  orientation: '南北'
});

// 选项数据
const floorOptions = ref([]);
const buildingTypeOptions = ref([]);
const decorateOptions = ref([]);
const zoneOptions = ref([]);
const orientationOptions = ref([]);

// 状态
const loading = ref(false);
const showResult = ref(false);
const resultPrice = ref('');
const resultType = ref('success');

// 区域分析相关
const showZoneAnalysis = ref(false);
const zoneStats = ref({
  avg_price: 0,
  max_price: 0,
  min_price: 0
});
const zoneChartRef = ref(null);
let zoneChart = null;

// 房间数量控制
const increaseRoom = () => {
  if (formData.value.rooms < 10) {
    formData.value.rooms++;
  }
};

const decreaseRoom = () => {
  if (formData.value.rooms > 1) {
    formData.value.rooms--;
  }
};

const increaseHall = () => {
  if (formData.value.halls < 10) {
    formData.value.halls++;
  }
};

const decreaseHall = () => {
  if (formData.value.halls > 1) {
    formData.value.halls--;
  }
};

// 加载特征选项
const loadFeatureOptions = async () => {
  try {
    const response = await EchartsApi({ lx: 'get_options' });
    if (response.code === 200 && response.data) {
      const data = response.data;
      
      // 填充楼层选项
      if (data.floors && data.floors.length > 0) {
        floorOptions.value = data.floors;
      }
      
      // 填充楼型选项
      if (data.building_types && data.building_types.length > 0) {
        buildingTypeOptions.value = data.building_types;
      }
      
      // 填充装修选项
      if (data.decorate_types && data.decorate_types.length > 0) {
        decorateOptions.value = data.decorate_types;
      }
      
      // 填充区域选项
      if (data.zones && data.zones.length > 0) {
        zoneOptions.value = data.zones;
      }
      
      // 填充朝向选项
      if (data.orientations && data.orientations.length > 0) {
        orientationOptions.value = data.orientations;
      }
    }
  } catch (error) {
    console.error('加载特征选项失败:', error);
    setDefaultOptions();
  }
};

// 设置默认选项
const setDefaultOptions = () => {
  floorOptions.value = ['低楼层', '中楼层', '高楼层'];
  buildingTypeOptions.value = ['板楼', '塔楼', '板塔结合'];
  decorateOptions.value = ['毛坯', '简装', '精装', '豪装'];
  zoneOptions.value = ['浔阳区', '濂溪区', '八里湖新区', '开发区', '柴桑区'];
  orientationOptions.value = ['南', '北', '南北', '东', '东南', '西南', '东西', '西北'];
};

// 预测函数
const handlePredict = async () => {
  // 验证输入
  if (!formData.value.area || formData.value.area <= 0) {
    ElMessage.warning('请输入有效的房屋面积');
    return;
  }
  
  if (!formData.value.zone) {
    ElMessage.warning('请选择区域');
    return;
  }

  loading.value = true;
  showResult.value = false;
  showZoneAnalysis.value = false;

  try {
    const response = await EchartsApi({
      lx: 2,
      area: formData.value.area,
      floor: formData.value.floor,
      zhuangxiu: formData.value.decorate,
      zone: formData.value.zone,
      floor1: formData.value.building_type,
      room2: formData.value.rooms,
      room1: formData.value.halls,
      year: formData.value.build_year,
      orientation: formData.value.orientation
    });

    if (response.code === 200) {
      resultPrice.value = response.data.replace('万', '');
      resultType.value = 'success';
      showResult.value = true;
      ElMessage.success('预测成功');
      
      // 加载区域价格分析
      await loadZoneAnalysis(formData.value.zone);
    } else {
      throw new Error(response.message || '预测失败');
    }
  } catch (error) {
    console.error('预测失败:', error);
    ElMessage.error(error.message || '预测过程中出现错误');
    resultType.value = 'error';
    showResult.value = true;
  } finally {
    loading.value = false;
  }
};

// 加载区域价格分析
const loadZoneAnalysis = async (zoneName) => {
  try {
    console.log('开始加载区域分析:', zoneName);
    const response = await EchartsApi({
      lx: 'zone_analysis',
      zone: zoneName
    });

    console.log('区域分析响应:', response);

    if (response.code === 200 && response.data) {
      const { chart, stats } = response.data;
      
      console.log('图表数据:', chart);
      console.log('统计数据:', stats);
      
      if (chart) {
        zoneStats.value = stats;
        showZoneAnalysis.value = true;
        console.log('显示区域分析，showZoneAnalysis:', showZoneAnalysis.value);
        
        // 渲染图表
        await nextTick();
        console.log('DOM 已更新，准备初始化图表');
        initZoneChart(chart);
      } else {
        console.warn('没有图表数据返回');
      }
    } else {
      console.error('区域分析 API 返回错误:', response);
    }
  } catch (error) {
    console.error('加载区域分析失败:', error);
  }
};

// 初始化区域价格分布图表
const initZoneChart = (chartData) => {
  if (zoneChartRef.value) {
    if (zoneChart) {
      zoneChart.dispose();
    }
    
    zoneChart = echarts.init(zoneChartRef.value);
    zoneChart.setOption(chartData);
    
    // 响应式调整
    window.addEventListener('resize', () => {
      zoneChart.resize();
    });
  }
};

// 页面加载时初始化
onMounted(() => {
  loadFeatureOptions();
});
</script>

<style scoped>
.prediction-container {
  padding: 20px;
  background-color: #f5f7fa;
  min-height: calc(100vh - 84px);
}

.prediction-card {
  max-width: 900px;
  margin: 0 auto;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 18px;
  font-weight: bold;
}

.input-group {
  display: flex;
  align-items: center;
  gap: 10px;
}

.unit {
  color: #909399;
  font-size: 14px;
}

.room-selector {
  display: flex;
  align-items: center;
  gap: 20px;
}

.room-item {
  display: flex;
  align-items: center;
  gap: 10px;
}

.room-label {
  color: #606266;
  font-size: 14px;
}

.predict-btn {
  width: 100%;
  height: 40px;
  font-size: 16px;
  margin-top: 10px;
}

.result-box {
  margin-top: 20px;
  padding: 20px;
  border-radius: 8px;
  text-align: center;
  background-color: #f0f9eb;
  border: 1px solid #e1f3d8;
}

.result-box.error {
  background-color: #fef0f0;
  border-color: #fde2e2;
}

.result-title {
  font-size: 14px;
  color: #606266;
  margin-bottom: 10px;
}

.result-price {
  font-size: 36px;
  font-weight: bold;
  color: #67c23a;
}

.result-box.error .result-price {
  color: #f56c6c;
}

.result-price small {
  font-size: 16px;
  color: #909399;
  margin-left: 5px;
}

.zone-analysis {
  margin-top: 30px;
  padding: 20px;
  background-color: #fff;
  border-radius: 8px;
}

.analysis-title {
  font-size: 18px;
  font-weight: bold;
  color: #303133;
  margin: 20px 0;
  text-align: center;
}

.stats-cards {
  margin-bottom: 20px;
}

.stat-card {
  text-align: center;
  border-radius: 8px;
}

.stat-label {
  font-size: 14px;
  color: #909399;
  margin-bottom: 10px;
}

.stat-value {
  font-size: 24px;
  font-weight: bold;
}

.price-primary {
  color: #409EFF;
}

.price-danger {
  color: #F56C6C;
}

.price-warning {
  color: #E6A23C;
}

.zone-chart {
  width: 100%;
  height: 400px;
  margin-top: 20px;
}</style>
