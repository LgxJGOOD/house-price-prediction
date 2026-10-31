<template>
    <div class="chart-header">
        <h2 style="margin-top: 20px; color: #303133;">💰 房价分析</h2>
        <p class="date-label">2026年4月</p>
    </div>
    <el-card style="margin-top: 10px;">
        <template #header>
            <h2>各区域平均房价对比</h2>
        </template>
        <div id="option02" style="width: 100%; height: 400px;"></div>
    </el-card>
</template>

<script setup>
import { onMounted , ref, watch} from 'vue'
import { useRoute } from 'vue-router'
import * as echarts from 'echarts'
import { EchartsApi } from '@/api/data/index.js';

const route = useRoute()
const option02  = ref({})

const fetchChart02 = async () => {
    try {
        const res = await EchartsApi({ lx: 1 });
        if (res.code === 200) {
            option02.value = res.data;
            const myChart = echarts.init(document.getElementById('option02'));
            myChart.setOption(option02.value);
        }
    } catch (error) {
        console.error('数据获取失败:', error);
    }
};

onMounted(() => {
    fetchChart02();
});

// 监听整个路径的变化
watch(
    () => route.fullPath,
    () => {
        console.log('路由变化，重新加载图表', route.path);
        fetchChart02();
    }
);
</script>    

<style scoped>
h2 {
    margin-bottom: 15px;
}
.chart-header {
    display: flex;
    align-items: center;
    gap: 15px;
}
.date-label {
    color: #909399;
    font-size: 14px;
    margin: 0;
    padding: 4px 12px;
    background: #f0f2f5;
    border-radius: 20px;
}
</style>
