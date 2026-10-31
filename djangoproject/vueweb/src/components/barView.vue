<script setup>
import { onMounted, onUnmounted, reactive, ref } from 'vue'
import { ElMessage } from 'element-plus'
import * as echarts from 'echarts'
import { EchartBarsApi } from '@/api/data/index.js';

const barChart02 = ref(null)
const chartInstance = ref(null)

const data02 = reactive({
      year: "2023",
      options: {
        title: {
      text: '各地区森林面积',
      textStyle: {
      color: '#fff'
        },
    },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow',
            lineStyle: {
              color: '#2D3443'
            }
          },
          formatter: function (params) {
            return params[0].seriesName + '<br>' + params[0].name+': ' + params[0].value + '万公顷';
        }
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
        xAxis: {
          type: 'category',
          name: '森林总面积',
          nameLocation: 'middle',
          nameTextStyle: {
            align: 'center' // 确保文本居中对齐
        },
        nameGap: 25,
          axisLabel: {
          interval: 0,
          rotate: '30',
        },
          data: []
        },
        yAxis: {
          type: 'value',
        name: '万公顷',
        },
        series: [
          {
            name: '森林面积',
            type: 'bar',
            label: {
              textStyle: {
                color: '#0ff'
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
    const response = await EchartBarsApi(params)
    if (response && response.data) {
      const [month, ...dataSeries] = response.data
      if (params.lx ===2||params.lx ===3)
      {targetData.options.yAxis.data = month}
      else
      {targetData.options.xAxis.data = month}
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
    await fetchDataAndUpdate(barChart02, { lx: 1,  year: 2023 }, data02)
  window.addEventListener('resize', handleResize)
})

// 清除事件监听器
onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
})
</script>

<template>
  <div ref="barChart02" style="width: 100%; height: 100%;"></div>
</template>

<style scoped>
/* 确保父级元素也设置了适当的宽度和高度 */
:deep(.el-container) {
  width: 100%;
  height: 600px; /* 使用视口高度 */
}
</style>