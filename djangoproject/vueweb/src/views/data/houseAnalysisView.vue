<template>
    <div class="chart-header">
        <h2 style="margin-top: 20px; color: #303133;">🏠 房屋分析</h2>
        <p class="date-label">2026年4月</p>
    </div>
    <el-row :gutter="20">
        <el-col :span="12">
            <el-card style="margin-top: 10px;">
                <template #header>
                    <h2>户型分布</h2>
                </template>
                <div id="option08" style="width: 100%; height: 400px;"></div>
            </el-card>
        </el-col>
        <el-col :span="12">
            <el-card style="margin-top: 10px;">
                <template #header>
                    <h2>朝向分布</h2>
                </template>
                <div id="option09" style="width: 100%; height: 400px;"></div>
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
const option08  = ref({})
const option09  = ref({})

const fetchChart08 = async () => {
    try {
        const res = await EchartsApi({ lx: 8 });
        if (res.code === 200) {
            option08.value = res.data;
            const myChart = echarts.init(document.getElementById('option08'));
            myChart.setOption(option08.value);
        }
    } catch (error) {
        console.error('数据获取失败:', error);
    }
};

const fetchChart09 = async () => {
    try {
        const res = await EchartsApi({ lx: 9 });
        if (res.code === 200) {
            option09.value = res.data;
            const myChart = echarts.init(document.getElementById('option09'));
            myChart.setOption(option09.value);
        }
    } catch (error) {
        console.error('数据获取失败:', error);
    }
};

onMounted(() => {
    fetchChart08();
    fetchChart09();
});

// 监听整个路径的变化
watch(
    () => route.fullPath,
    () => {
        console.log('路由变化，重新加载图表', route.path);
        fetchChart08();
        fetchChart09();
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
