<template>
    <div class="chart-header">
        <h2 style="margin-top: 20px; color: #303133;">📊 数量分析</h2>
        <p class="date-label">2026年4月</p>
    </div>
    <el-row :gutter="20">
        <el-col :span="12">
            <el-card style="margin-top: 10px;">
                <template #header>
                    <h2>各区域房源数量分布</h2>
                </template>
                <div id="option01" style="width: 100%; height: 400px;"></div>
            </el-card>
        </el-col>
        <el-col :span="24">
            <el-card style="margin-top: 10px;">
                <template #header>
                    <h2>建筑时间分布</h2>
                </template>
                <div id="option03" style="width: 100%; height: 400px;"></div>
            </el-card>
        </el-col>
    </el-row>
</template>

<script setup>
import { onMounted , ref, watch} from 'vue'
import { useRoute } from 'vue-router'
import * as echarts from 'echarts'
import { EchartsApi } from '@/api/data/index.js';

const route = useRoute()
const option01  = ref({})
const option03  = ref({})

const fetchChart01 = async () => {
    try {
        const res = await EchartsApi({ lx: 0 });
        if (res.code === 200) {
            option01.value = res.data;
            const myChart = echarts.init(document.getElementById('option01'));
            myChart.setOption(option01.value);
        }
    } catch (error) {
        console.error('数据获取失败:', error);
    }
};

const fetchChart03 = async () => {
    try {
        const res = await EchartsApi({ lx: 3 });
        if (res.code === 200) {
            option03.value = res.data;
            const myChart = echarts.init(document.getElementById('option03'));
            myChart.setOption(option03.value);
        }
    } catch (error) {
        console.error('数据获取失败:', error);
    }
};

onMounted(() => {
    fetchChart01();
    fetchChart03();
});

// 监听整个路径的变化
watch(
    () => route.fullPath,
    () => {
        console.log('路由变化，重新加载图表', route.path);
        fetchChart01();
        fetchChart03();
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
