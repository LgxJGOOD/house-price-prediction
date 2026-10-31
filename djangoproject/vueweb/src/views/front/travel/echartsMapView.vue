<template>
  <el-card>
    <template #header>
      <h2>全国景点数量分布</h2>
    </template>
    <div class="content">
      <div ref="chartsRef" style="width: 100%; height: 800px; margin: 0 auto"></div>
    </div>
  </el-card>
</template>

<script setup>
import * as echarts from 'echarts';
import china from '@/assets/china.json';
import { onMounted, ref } from 'vue';
import { EchartsApi } from '@/api/data/index.js';

const chartsRef = ref(null);
const data = ref([]);

const fetchData = async () => {
  try {
    const res = await EchartsApi({ 'lx': 6 });
    if (res.code === 200) {
      data.value = res.data || [];
    }
  } catch (error) {
    console.error('Failed to fetch data:', error);
  }
};

const initCharts = () => {
  const chartInstance = echarts.init(chartsRef.value);
  const option = {
    backgroundColor: '#dcdfe6',
    tooltip: {
      trigger: 'item',
      formatter: function (params) {
        if (params.value) {
          return `${params.name}<br/> ${params.value} 个景点`;
        }
        return '';
      }
    },
    geo: {
      map: 'china',
      roam: true,
      label: {
        normal: {
          show: true,
          textStyle: {
            color: '#000'
          }
        },
        emphasis: {
          textStyle: {
            color: '#fff'
          }
        }
      },
      itemStyle: {
        normal: {
          borderColor: '#5089EC',
          borderWidth: 1,
          areaColor: {
            type: 'radial',
            x: 0.5,
            y: 0.5,
            r: 0.8,
            colorStops: [
              { offset: 0, color: 'rgba(0, 102, 154, 0)' },
              { offset: 1, color: 'rgba(0, 102, 154, .4)' }
              // { offset: 0, color: 'rgba(255, 255, 0, 0)' }, 
              // { offset: 0.5, color: 'rgba(255, 255, 0, .2)' }, 
              // { offset: 1, color: 'rgba(255, 0, 0, .4)' }
                  ]
                }
              },
emphasis: {
  areaColor: '#2386AD',
    borderWidth: 0
}
            }
          },
series: [
  {
    type: 'map',
    geoIndex: 0,
    data: data.value,
  },
  {
    data: [{ value: [116.4074, 39.9042] }],
    type: 'effectScatter',
    coordinateSystem: 'geo',
    rippleEffect: {
      brushType: 'stroke', // 设置涟漪动画的效果
      scale: 5, // 涟漪大小
      period: 4, // 动画周期
      color: 'red'
    },
    label: {
      normal: {
        show: true,
        position: 'right',
        formatter: '{b}'
      }
    },
    symbolSize: 10, // 标记大小
    itemStyle: {
      normal: {
        color: '#F62157' // 颜色
      }
    },
  }
],
  visualMap: {
  min: 0,
    max: 200,
      text: ['高', '低'],
        inRange: {
    // color: ['#fff', '#d1edc4', '#67c23a']
    color: ['#FFFF00', '#FF7F00', '#FF0000'] // 从黄色到橙色再到红色
  },
  realtime: false,
    calculable: true,
    }
  };
echarts.registerMap('china', china);
chartInstance.setOption(option);
};

onMounted(() => {
  fetchData().then(() => {
    initCharts();
  });
});
</script>

<style scoped>
.content {
  background-color: #072c92;
  height: 100%;
}
</style>