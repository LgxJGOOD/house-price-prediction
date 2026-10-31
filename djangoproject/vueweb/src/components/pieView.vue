<script setup>
import { onMounted, onUnmounted, reactive, ref } from 'vue'
import { ElMessage } from 'element-plus'
import * as echarts from 'echarts'
import {EchartPiesApi} from '@/api/data/index.js';

const pieChart = ref(null)
const chartInstance = ref(null)

const data = reactive({
      year: "2023",
      options: {
        title: {
          text: '各地区森林面积占比',
          left: 'center',
        },
      
        tooltip: {
          trigger: 'item',
          formatter: '{a}<br/>{b}: {c} ({d}%)}'
        },
        legend: {
          type:'scroll',
          orient: 'vertical',
          right: '10',
          top: '20',
          bottom: '20',
          data: []
        },
        
        series: [
          {
            name: '森林面积占比',
            type: 'pie',
            radius: ['40%', '70%'],
            avoidLabelOverlap: false,
            itemStyle: {
            borderRadius: 10,
            borderColor: '#fff',
            borderWidth: 2
          },
            label: {
              show: false,
              position: 'center',
              textStyle: {
                color: 'white'
              }
            },
            labelLine: {
              show: false
            },
            emphasis: {
              label: {
                show: true,
                fontSize: '30',
                fontWeight: 'bold'
              }
            },
            data: []
          }
        ]
      
     
      }
    })
// 获取并更新数据
const fetchDataAndUpdate = async (chartInstanceRef, params, targetData) => {
  try {
    const response = await EchartPiesApi(params)
    if (response && response.data) {
      const [month, ...dataSeries] = response.data
      targetData.options.legend.data = month
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
await fetchDataAndUpdate(pieChart, { lx: 0,  year: data.year }, data)
  window.addEventListener('resize', handleResize)
})

// 清除事件监听器
onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
})
</script>

<template>
  <div ref="pieChart" style="width: 100%; height: 100%;"></div>
</template>

<style scoped>
/* 确保父级元素也设置了适当的宽度和高度 */
:deep(.el-container) {
  width: 100%;
  height: 600px; /* 使用视口高度 */
}
</style>