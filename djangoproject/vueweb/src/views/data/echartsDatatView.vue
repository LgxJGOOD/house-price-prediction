<template>
    <!-- 一、面积分析模块 -->
    <h2 style="margin-top: 20px; color: #303133;">一、面积分析</h2>
    <el-row :gutter="20">
        <el-col :span="12">
            <el-card style="margin-top: 10px;">
                <template #header>
                    <h2>九江市房屋面积分析</h2>
                </template>
                <div id="option05" style="width: 100%; height: 400px;"></div>
            </el-card>
        </el-col>
        <el-col :span="12">
            <el-card style="margin-top: 10px;">
                <template #header>
                    <h2>房屋面积占比</h2>
                </template>
                <div id="option07" style="width: 100%; height: 400px;"></div>
            </el-card>
        </el-col>
    </el-row>

    <!-- 二、数量分析模块 -->
    <h2 style="margin-top: 20px; color: #303133;">二、数量分析</h2>
    <el-row :gutter="20">
        <el-col :span="12">
            <el-card style="margin-top: 10px;">
                <template #header>
                    <h2>各区域房源数量分布</h2>
                </template>
                <div id="option01" style="width: 100%; height: 400px;"></div>
            </el-card>
        </el-col>
        <el-col :span="12">
            <el-card style="margin-top: 10px;">
                <template #header>
                    <h2>建筑时间分布</h2>
                </template>
                <div id="option03" style="width: 100%; height: 400px;"></div>
            </el-card>
        </el-col>
    </el-row>

    <!-- 三、房屋分析模块 -->
    <h2 style="margin-top: 20px; color: #303133;">三、房屋分析</h2>
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

    <!-- 四、房价分析模块 -->
    <h2 style="margin-top: 20px; color: #303133;">四、房价分析</h2>
    <el-card style="margin-top: 10px;">
        <template #header>
            <h2>各区域平均房价对比</h2>
        </template>
        <div id="option02" style="width: 100%; height: 400px;"></div>
    </el-card>
</template>

<script setup>
import { onMounted , ref} from 'vue'
import * as echarts from 'echarts'
import { EchartsApi } from '@/api/data/index.js';

const option01  = ref({})
const option02  = ref({})
const option03  = ref({})
const option05  = ref({})
const option07  = ref({})
const option08  = ref({})
const option09  = ref({})

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

const fetchChart05 = async () => {
    try {
        const res = await EchartsApi({ lx: 5 });
        if (res.code === 200) {
            option05.value = res.data;
            const myChart = echarts.init(document.getElementById('option05'));
            myChart.setOption(option05.value);
        }
    } catch (error) {
        console.error('数据获取失败:', error);
    }
};
const fetchChart07 = async () => {
    try {
        const res = await EchartsApi({ lx: 7 });
        if (res.code === 200) {
            option07.value = res.data;
            const myChart = echarts.init(document.getElementById('option07'));
            myChart.setOption(option07.value);
        }
    } catch (error) {
        console.error('数据获取失败:', error);
    }
};

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
    fetchChart01();
    fetchChart02();
    fetchChart03();
    fetchChart05();
    fetchChart07();
    fetchChart08();
    fetchChart09();
});
</script>    