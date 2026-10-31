<template>
    <el-card>
      <template #header>
        <h2>全国森林面积</h2>
      </template>
      <div class="content">
        <div
          ref="charts"
          style="width: 100%; height: 800px; margin: 0 auto"
        ></div>
      </div>
    </el-card>
  </template>
  
  <script>
  import * as echarts from 'echarts'
  import china from '@/assets/china.json'
  
  export default {
    data() {
      return {
        points: [
        {
                "name": "北京",
                "value": 71.82
            },
            {
                "name": "天津",
                "value": 13.64
            },
            {
                "name": "河北",
                "value": 502.69
            },
            {
                "name": "山西",
                "value": 321.09
            },
            {
                "name": "内蒙古",
                "value": 2614.85
            },
            {
                "name": "辽宁",
                "value": 571.83
            },
            {
                "name": "吉林",
                "value": 784.87
            },
            {
                "name": "黑龙江",
                "value": 1990.46
            },
            {
                "name": "上海",
                "value": 8.9
            },
            {
                "name": "江苏",
                "value": 155.99
            },
            {
                "name": "浙江",
                "value": 604.99
            },
            {
                "name": "安徽",
                "value": 395.85
            },
            {
                "name": "福建",
                "value": 811.58
            },
            {
                "name": "江西",
                "value": 1021.02
            },
            {
                "name": "山东",
                "value": 266.51
            },
            {
                "name": "河南",
                "value": 403.18
            },
            {
                "name": "湖北",
                "value": 736.27
            },
            {
                "name": "湖南",
                "value": 1052.58
            },
            {
                "name": "广东",
                "value": 945.98
            },
            {
                "name": "广西",
                "value": 1429.65
            },
            {
                "name": "海南",
                "value": 194.49
            },
            {
                "name": "重庆",
                "value": 354.97
            },
            {
                "name": "四川",
                "value": 1839.77
            },
            {
                "name": "贵州",
                "value": 771.03
            },
            {
                "name": "云南",
                "value": 2106.16
            },
            {
                "name": "西藏",
                "value": 1490.99
            },
            {
                "name": "陕西",
                "value": 886.84
            },
            {
                "name": "甘肃",
                "value": 509.73
            },
            {
                "name": "青海",
                "value": 419.75
            },
            {
                "name": "宁夏",
                "value": 65.6
            },
            {
                "name": "新疆",
                "value": 802.23
            }

        ]
      }
    },
    mounted() {
      this.initCharts()
    },
    methods: {
      initCharts() {
        const charts = echarts.init(this.$refs['charts'])
        const option = {
          backgroundColor: '#dcdfe6', // 背景颜色
          tooltip: {
            trigger: 'item',
            formatter: function (params) {
            if (params.value) { // Check if value exists
              return `${params.name}<br/>森林面积 ${params.value} 万公顷`;
            }
            return '';
          }
          },
          geo: {
            map: 'china',
            roam:true,
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
              data: this.points
            },
            {
              data:[ { value: [116.4074, 39.9042] } ],
              type:'effectScatter',
              coordinateSystem:'geo',
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
            min: 5,
            max: 3000,
            text: ['高', '低'],
            inRange:{
              color: ['#fff','#d1edc4','#67c23a' ]
            },
            realtime: false,
            calculable: true,
            // color: ['#f44336', '#fc9700', '#ffde00', '#ffde00', '#00eaff']
          }
        }
        echarts.registerMap('china', china)
        charts.setOption(option)
      }
    }
  }
  </script>
  
  <style scoped>
  .content {
    background-color: #072c92;
    height: 100%;
  }
  </style>