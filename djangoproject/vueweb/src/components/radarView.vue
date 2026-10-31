<script setup>
import { onMounted, onUnmounted, reactive, ref } from 'vue'
import { ElMessage } from 'element-plus'
import * as echarts from 'echarts'
import { radarEchartsApi } from '@/api/data/index.js'

const radarChart = ref(null)
const chartInstance = ref(null)

const data = reactive({
  options: {
    title: {
      text: '森林资源雷达图',
    },
    legend: {
      data: ['2005', '2023'],
    },
    radar: {
      // shape: 'circle',
      indicator: [],
    },
    series: [
      {
        type: 'radar',
        data: [
          {
            value: [],
            name: '2005',
            label: {
              show: true,
              color: '#fff'
            }
          },
          {
            value: [],
            name: '2023',
            label: {
              show: true,
              color: '#00f'
            }
          }
        ]
      }
    ]
  }
})

// 获取并更新天气数据
const fetchDataAndUpdate = async (chartInstanceRef, params, targetData) => {
  try {
    const response = await radarEchartsApi(params)
    if (response && response.data) {
      const [data01, data02, data03] = response.data
      // targetData.options.radar.indicator = data01
      const colors = ['#000', '#000', '#000', '#000', '#000', '#000'];

      // 更新 targetData 的 radar indicators
      targetData.options.radar.indicator = data01.map((indicator, index) => {
        return {
          ...indicator,
          nameTextStyle: {
            color: colors[index % colors.length] // 使用颜色数组循环颜色
          }
        };
      });
      targetData.options.series[0].data[0].value = data02
      targetData.options.series[0].data[1].value = data03

      chartInstance.value = echarts.init(chartInstanceRef.value)
      chartInstance.value.setOption(targetData.options)
      window.dispatchEvent(new Event('resize')) // 强制触发resize事件以确保图表正确初始化
    } else {
      ElMessage.error('数据为空')
    }
  } catch (error) {
    ElMessage.error('获取数据失败')
    console.error('Error fetching data:', error)
  }
}

// 处理窗口大小变化
const handleResize = () => {
  if (chartInstance.value) {
    chartInstance.value.resize()
  }
}

// 初始化
onMounted(async () => {
  await fetchDataAndUpdate(radarChart, { lx: 0, city_name: "全国" }, data)
  window.addEventListener('resize', handleResize)
})

// 清除事件监听器
onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
})
</script>

<template>
  <div ref="radarChart" style="width: 100%; height: 100%;"></div>
</template>

<style scoped>
/* 确保父级元素也设置了适当的宽度和高度 */
:deep(.el-container) {
  width: 100%;
  height: 600px;
  /* 使用视口高度 */
}
</style>