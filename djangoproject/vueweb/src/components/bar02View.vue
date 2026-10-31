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
      text: '各地区森林覆盖率',
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
            return params[0].seriesName + '<br>' + params[0].name+': ' + params[0].value + '%';
        }
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
        xAxis: {
          type: 'value',
          name: '',
          nameLocation: 'middle',
          nameTextStyle: {
            align: 'center' // 确保文本居中对齐
        },
        nameGap: 25,
          axisLabel: {
          interval: 0,
          rotate: '30',
        },
         
        },
        yAxis: {
          type: 'category',
        name: '地区',
        data: []
        },
        series: [
          {
            name: '森林覆盖率',
            type: 'bar',
            label: {
              textStyle: {
                color: 'white'
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
      targetData.options.yAxis.data = month;
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

onMounted(async () => {
    await fetchDataAndUpdate(barChart02, { lx: 3,  year: 2023 }, data02)
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
})
</script>

<template>
  <div ref="barChart02" style="width: 100%; height: 100%;"></div>
</template>

<style scoped>
:deep(.el-container) {
  width: 100%;
  height: 600px; /* 使用视口高度 */
}
</style>