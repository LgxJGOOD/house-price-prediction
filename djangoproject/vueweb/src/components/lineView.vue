<script setup>
import { onMounted, onUnmounted, reactive, ref } from 'vue'
import { ElMessage } from 'element-plus'
import * as echarts from 'echarts'
import { EchartLinesApi } from '@/api/data/index.js';

const lineChart = ref(null)
const chartInstance = ref(null)

const data02 =  reactive({
  options: {
    title: {
      text: '全国人工林面积',
      textStyle: {
      color: '#fff'
        },
    },
    tooltip: { trigger: 'axis' ,
      formatter: '人工林面积 <br/>{b}年：{c} 公顷'
    },
    xAxis: { data: [],
        axisLabel: {
          interval: 0,
          rotate: '45',
        },
     },
    grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
    yAxis: {type: 'value', 
      name: '面积 (公顷)', 
      scale: true,
      },
    series: [{ data: [], type: 'line', smooth: true }],
   
  }
})

// 获取并更新数据
const fetchDataAndUpdate = async (chartInstanceRef, params, targetData) => {
  try {
    const response = await EchartLinesApi(params)
    if (response && response.data) {
      const [month, ...dataSeries] = response.data
      targetData.options.xAxis.data = month
      targetData.options.series.forEach((series, index) => {
        series.data = dataSeries[index] || []
      })
      const chartInstance = echarts.init(chartInstanceRef.value)
      chartInstance.setOption(targetData.options)
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
await fetchDataAndUpdate(lineChart, { lx: 4, city_name: "全国" }, data02)
  window.addEventListener('resize', handleResize)
})

// 清除事件监听器
onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
})
</script>

<template>
  <div ref="lineChart" style="width: 100%; height: 100%;"></div>
</template>

<style scoped>
/* 确保父级元素也设置了适当的宽度和高度 */
:deep(.el-container) {
  width: 100%;
  height: 600px; /* 使用视口高度 */
}
</style>