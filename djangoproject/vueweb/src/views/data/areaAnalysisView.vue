                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              <template>
    <div class="chart-header">
        <h2 style="margin-top: 20px; color: #303133;">📊 面积分析</h2>
        <p class="date-label">2026年4月</p>
    </div>
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
</template>

<script setup>
import { onMounted , ref, watch} from 'vue'
import { useRoute } from 'vue-router'
import * as echarts from 'echarts'
import { EchartsApi } from '@/api/data/index.js';

const route = useRoute()
const option05  = ref({})
const option07  = ref({})

const fetchChart05 = async () => {
    try {
        console.log('开始加载面积分析图表...');
        const res = await EchartsApi({ lx: 5 });
        console.log('面积分析响应:', res);
        if (res.code === 200) {
            option05.value = res.data;
            const myChart = echarts.init(document.getElementById('option05'));
            myChart.setOption(option05.value);
            console.log('面积分析图表渲染成功');
        }
    } catch (error) {
        console.error('面积分析数据获取失败:', error);
    }
};

const fetchChart07 = async () => {
    try {
        console.log('开始加载面积占比图表...');
        const res = await EchartsApi({ lx: 7 });
        console.log('面积占比响应:', res);
        if (res.code === 200) {
            option07.value = res.data;
            const myChart = echarts.init(document.getElementById('option07'));
            myChart.setOption(option07.value);
            console.log('面积占比图表渲染成功');
        }
    } catch (error) {
        console.error('面积占比数据获取失败:', error);
    }
};

onMounted(() => {
    fetchChart05();
    fetchChart07();
});

// 监听整个路径的变化
watch(
    () => route.fullPath,
    () => {
        console.log('路由变化，重新加载图表', route.path);
        fetchChart05();
        fetchChart07();
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
