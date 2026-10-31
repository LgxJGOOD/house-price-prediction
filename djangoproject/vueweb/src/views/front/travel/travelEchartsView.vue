<script setup>
import { onMounted,  reactive,ref ,watch} from 'vue'
import { ElMessage, ElCard} from 'element-plus'
import * as echarts from 'echarts'
import {cityListApi, EchartsApi} from '@/api/data/index.js';

const lineChart = ref(null)
const lineChart01 = ref(null)
const barChart = ref(null)
const barChart01 = ref(null)
const pieChart = ref(null)
const pieChart01 = ref(null)
const barChart02 = ref(null)

const data = reactive({
  options: {
    tooltip: { trigger: 'axis' ,
      formatter: '城市景点数量 <br/>{b}: {c}'
    },
    xAxis: { data: [] },
    yAxis: {type: 'value', 
      name: '个', 
      scale: true,
      },
    series: [{ data: [], type: 'line', smooth: true }],
    dataZoom: [
      {
        type: 'inside', 
        start: 0, 
        end: 100 
      },
      {
        type: 'slider', 
        show: true,
        xAxisIndex: [0],
        start: 0,
        end: 100
      }
    ]
  }
})
const data01 = reactive({
  options: {
    tooltip: { trigger: 'axis' ,
      formatter: '城市景点 <br/>{b}: {c}'
    },
    xAxis: { data: [] },
    yAxis: {type: 'value', 
      name: '分', 
      scale: true,
      },
    series: [{ data: [], type: 'line', smooth: true }],
    dataZoom: [
      {
        type: 'inside', 
        start: 0, 
        end: 100 
      },
      {
        type: 'slider', 
        show: true,
        xAxisIndex: [0],
        start: 0,
        end: 100
      }
    ]
  }
})


const bardata = reactive({
      options: {
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          },
           formatter: '城市景点数量 <br/>{b}: {c}'
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
        xAxis: {
          type: 'category',
          name: '城市',
          nameLocation: 'middle',
          nameTextStyle: {
            align: 'center' 
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
        name: '个'
        },
        series: [
          {
            name: '城市',
            type: 'bar',
            data: []
          }
        ]
      }
    })

const bardata01 = reactive({
        city_name: "北京",
      options: {
        color: '#4cabce',
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          },
         formatter: '城市景点 <br/>{b}: {c}分'
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
        xAxis: {
          type: 'category',
          name: '城市',
          nameLocation: 'middle',
          nameTextStyle: {
            align: 'center' 
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
        name: '评分'
        },
        series: [
          {
            name: '城市',
            type: 'bar',
            data: []
          }
        ]
      }
    })    


const bardata02 = reactive({
        city_name: "北京",
      options: {
        color: '#4cabce',
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          },
         formatter: '城市景点热度 <br/>{b}: {c}'
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
        xAxis: {
          type: 'category',
          name: '城市',
          nameLocation: 'middle',
          nameTextStyle: {
            align: 'center' 
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
        name: '热度'
        },
        series: [
          {
            name: '城市',
            type: 'bar',
            data: []
          }
        ]
      }
    })       

const piedata = reactive({
      options: {
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
            name: '城市景点占比',
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
              position: 'center'
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

const piedata01 = reactive({
      options: {
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
            name: '用户角色占比',
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
              position: 'center'
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

// 下拉选择框的数据
const options = ref([])
// 下拉选择框绑定的值
const selectedCity = ref(null)

//获取更新数据并渲染图表
const fetchDataAndRenderChart = async (chartInstanceRef, params, targetData, chartType = 'line') => {
  try {
    const response = await EchartsApi(params);
    if (!response || !response.data) {
      ElMessage.error('数据为空');
      return;
    }

    let data = response.data;

    // 根据图表类型来解析数据
    if (chartType === 'line'||chartType === 'bar' ) {
      let [xAxisData, ...seriesData] = data;
      targetData.options.xAxis.data = xAxisData;
      targetData.options.series = targetData.options.series.map((series, index) => ({
        ...series,
        data: seriesData[index] || [],
      }));
    } else if (chartType === 'pie') {
      const [legendData, ...dataSeries] = data;
      targetData.options.legend.data = legendData;
      targetData.options.series.forEach((series, index) => {
        series.data = dataSeries[index] || [];
      });
    }

    echarts.init(chartInstanceRef.value).setOption(targetData.options);

  } catch (error) {
    console.error('Error fetching data:', error);
    ElMessage.error('获取数据失败，请检查网络连接或服务器状态');
  }
};


 
// 获取城市名称
const fetchCityName = async () => {
  try {
    const response = await cityListApi()
    if (response && response.data) {
        console.log('responseCity:',response.data)
      options.value = response.data.map(item => ({ label: item.name, value: item.name }))
    } else {
      ElMessage.error('数据为空')
    }
  } catch (error) {
    ElMessage.error('获取数据失败3')
    console.error('Error fetching city list:', error)
  }
}

// 初始化
onMounted(async () => {
    await Promise.all([fetchCityName(), 
    fetchDataAndRenderChart(lineChart, { lx: 0, city_name: "" }, data,  'line'),
    fetchDataAndRenderChart(lineChart01, { lx: 1, city_name: "" }, data01,  'line'),
    fetchDataAndRenderChart(barChart, { lx: 2, city_name: "" }, bardata, 'bar'),
    fetchDataAndRenderChart(pieChart, { lx: 4, city_name: "" }, piedata, 'pie'),
    fetchDataAndRenderChart(pieChart01, { lx: 5, city_name: "" }, piedata01, 'pie'),
]);
   // 设置默认值
    selectedCity.value = "北京"
  if (options.value.length > 0) {
    await fetchDataAndRenderChart(barChart01, { lx: 3, city_name: bardata01.city_name }, bardata01,'bar')
    await fetchDataAndRenderChart(barChart02, { lx: 7, city_name: bardata01.city_name }, bardata02, 'bar')
  }
})

// 监听城市选择变化
watch(selectedCity, async (newCity) => {
  if (newCity) {
    bardata01.city_name = newCity;
    await fetchDataAndRenderChart(barChart01, { lx: 3, city_name: bardata01.city_name }, bardata01,'bar');
    await fetchDataAndRenderChart(barChart02, { lx: 7, city_name: bardata01.city_name }, bardata02, 'bar')
  }
});

</script>

<template>
  <el-card style="margin-top: 60px;">
    <template #header>
      <h2>城市景点数量</h2>
    </template>
    <div ref="lineChart" style="width: 100%; height: 400px;"></div>
  </el-card>
  <el-card>
    <template #header>
      <h2>城市景点平均评分</h2>
    </template>
    <div ref="lineChart01" style="width: 100%; height: 400px;"></div>
  </el-card>
  <el-card>
    <template #header>
      <h2>城市景点数量</h2>
    </template>
    <div ref="barChart" style="width: 100%; height: 400px;"></div>
  </el-card>
  <el-card>
    <template #header>
      <h2>{{ bardata01.city_name}}城市景点排名</h2>
      <el-select
        v-model="selectedCity"
        clearable
        placeholder="请选择城市"
        style="width: 120px;margin-top: 10px;"
      >
        <el-option
          v-for="item in options"
          :key="item.value"
          :label="item.label"
          :value="item.value"
        />
      </el-select>
    </template>
    <div ref="barChart01" style="width: 100%; height: 400px;"></div>
  </el-card> 
<!-- 热度 -->
  <el-card>
    <template #header>
      <h2>{{ bardata01.city_name}}城市景点热度排名</h2>
    </template>
    <div ref="barChart02" style="width: 100%; height: 400px;"></div>
  </el-card> 
  <el-row :gutter="20" style="margin-top: 20px;">
    <el-col :span="12">
  <el-card>
    <template #header>
      <h2>城市景点占比</h2>
    </template>
    <div ref="pieChart" style="width: 100%; height: 400px;"></div>
  </el-card>
</el-col>
  <el-col :span="12">
  <el-card>
    <template #header>
      <h2>用户角色占比</h2>
    </template>
    <div ref="pieChart01" style="width: 100%; height: 400px;"></div>
  </el-card>
</el-col>
</el-row>
</template>