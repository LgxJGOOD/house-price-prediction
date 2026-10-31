<template>
    <div style="margin-top: 80px;">
        <el-breadcrumb separator=">">
            <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
            <el-breadcrumb-item>
                <router-link :to="{ path: '/travel/list' }">景区景点</router-link>
            </el-breadcrumb-item>
            <el-breadcrumb-item>景点详情</el-breadcrumb-item>
        </el-breadcrumb>
    </div>
    <hr>

    <div class="container">
        <div class="left">
            <el-card class="spot-card">
                <div class="spot-info">
                    <div class="image-container">
                        <img :src="detailData.coverImageUrl" alt="Spot Image" class="spot-image">
                    </div>
                    <div class="text-info">
                        <div style="display: flex; align-items: center;">
                            <span class="cn_tit">{{ detailData.poiName }}
                            </span>
                            <span class="en_tit">
                                <svg t="1739860943041" class="icon" viewBox="0 0 1024 1024" version="1.1"
                                    xmlns="http://www.w3.org/2000/svg" p-id="1536" width="24" height="24">
                                    <path
                                        d="M442.514286 73.142857c82.529524 64.24381 140.239238 126.610286 173.129143 187.099429 31.158857 57.295238 43.666286 115.907048 37.546666 175.835428l-1.219047 9.996191 6.095238-4.973715a174.055619 174.055619 0 0 0 49.249524-69.607619l2.681904-7.411809 7.704381-23.04c82.285714 55.734857 123.440762 150.064762 123.440762 283.062857C841.142857 823.515429 665.795048 950.857143 521.654857 950.857143c-144.11581 0-308.224-85.333333-334.750476-263.875048-26.550857-178.541714 83.480381-261.90019 158.427429-378.197333C395.288381 231.253333 427.690667 152.697905 442.514286 73.142857z m33.718857 154.575238c-17.554286 41.447619-39.424 82.407619-65.536 122.904381l-8.313905 12.653714c-8.411429 12.507429-17.310476 24.941714-28.818286 40.374858l-40.96 54.467047c-63.634286 86.869333-80.944762 136.021333-68.851809 217.526857 17.92 120.441905 128.341333 197.778286 257.901714 197.778286 120.905143 0 241.785905-110.933333 241.785905-249.344 0-61.976381-9.825524-111.323429-29.110857-149.699048-8.240762 9.411048-17.237333 18.285714-26.965334 26.59962l-159.085714 130.023619 26.697143-195.364572c6.41219-46.811429-2.462476-92.208762-27.648-138.483809-13.214476-24.30781-31.98781-49.737143-56.368762-76.166096l-8.338286-8.850285-6.387809 15.579428z"
                                        p-id="1537" fill="#ff525a"></path>
                                </svg>
                                {{ detailData.heatScore }}</span>
                        </div>
                        <div>
                            <span class="cur_score">{{ detailData.commentScore }}</span>
                            <span class="total_score">/ 5分</span>
                            &nbsp;&nbsp;&nbsp;&nbsp;
                            <span>{{ detailData.districtName }}</span>
                        </div>
                        <span style="margin-top: 10px;">{{ detailData.distanceStr }}</span>
                        <span style="margin-top: 10px;">标签：{{ detailData.shortFeatures }} {{ detailData.tagNameList
                            }}</span>
                        <span class="description">我的评分：{{ detailData.rating }} &nbsp;&nbsp;
                            <el-button type="primary" size="small" icon="Edit" @click="openEditDialog"></el-button>
                        </span>
                        <div class="favorite-wrapper" @click="toggleCollect">
                            <p v-if="detailData.is_collect">已收藏&nbsp;&nbsp;</p>
                            <p v-else>收藏&nbsp;&nbsp;</p>
                            <el-icon v-if="detailData.is_collect" style="color: #f80;">
                                <StarFilled />
                            </el-icon>
                            <el-icon v-else style="color: #f80;">
                                <Star />
                            </el-icon>
                        </div>
                    </div>
                </div>
            </el-card>
            <!-- 新增评论部分 -->
            <div class="comment-section" style="flex: 8; margin-top: 20px;">
                <span class="e_title_content">用户点评</span>
                <hr>

                <ul style="list-style-type: none; padding: 0;">
                    <li v-for="comment in comments" :key="comment.id" class="comment-item">
                        <div class="comment-content">
                            <p>{{ comment.review_content }}</p>
                            <div class="comment-meta">
                                <span>由 {{ comment.reviewer_name }} 发布于 {{ comment.create_date }}</span>
                            </div>
                        </div>
                        <hr style="border-top: 1px solid #ddd; margin: 15px 0;">
                    </li>
                </ul>

                <div v-if="isLoggedIn">
                    <el-form @submit.prevent="addComment">
                        <el-input type="textarea" v-model="newComment" placeholder="请输入您的评论"></el-input>
                        <el-button type="primary" native-type="submit" style="margin-top: 10px;">发表评论</el-button>
                    </el-form>
                </div>
                <div v-else>
                    <p style="color: #999;">请<router-link :to="{ path: '/login' }"
                            style="color: #1badb6; text-decoration: underline;">登录</router-link>后评论。</p>
                </div>

            </div>
        </div>

        <div class="right">
            <span class="spots">当前热门景点</span>
            <el-table :data="hotSpots" style="width: 100%; margin-top: 20px;">
                <el-table-column type="index" width="50" />
                <el-table-column label="景点" width="200">
                    <template #default="scope">
                        <span class="clickable" @click="goToDetail(scope.row)">
                            {{ scope.row.poiName }}
                        </span>
                    </template>
                </el-table-column>
                <el-table-column prop="districtName" label="城市" width="80" />
                <el-table-column prop="commentScore" label="评分" />
            </el-table>
            <div style="margin-top: 10px;">
                <span class="spots">旅游线路推荐</span>
                <el-table :data="SpotRecommendation" style="width: 100%; margin-top: 20px;" @row-click="handleRowClick">
                    <el-table-column type="index" width="50" />
                    <el-table-column prop="title" label="标题" width="300" />
                </el-table>
            </div>

            <div style="margin-top: 10px;">
                <span class="spots">旅游景点推荐</span>
                <el-table :data="RecommendSimilarSpot" style="width: 100%; margin-top: 20px;">
                    <el-table-column type="index" width="50" />
                    <el-table-column label="景点" width="200">
                        <template #default="scope">
                            <span class="clickable" @click="goToDetail(scope.row)">
                                {{ scope.row.poiName }}
                            </span>
                        </template>
                    </el-table-column>
                    <el-table-column prop="districtName" label="城市" width="80" />
                    <el-table-column prop="commentScore" label="评分" />
                </el-table>
            </div>
        </div>

        <!-- 添加 Dialog 来展示旅游线路推荐详情 -->
        <el-dialog v-model="dialogVisible" title="旅游线路详情" destroy-on-close>
            <el-table :data="selectedRecommendation" style="width: 100%; margin-top: 20px;">
                <el-table-column label="行程" width="200">
                    <template #default="scope">
                        <span>
                            {{ '第' + scope.row.journey_time + '天' }} <br />
                            {{ scope.row.scheduling }}
                        </span>
                    </template>
                </el-table-column>
                <el-table-column prop="dine" label="用餐" width="180" />
                <el-table-column prop="Activities" label="景点/场馆&活动" width="320" />
                <el-table-column prop="hotel" label="酒店" />
            </el-table>
            <template #footer>
                <span class="dialog-footer">
                    <el-button @click="dialogVisible = false">关闭</el-button>
                </span>
            </template>
        </el-dialog>
        <!--修改评分对话框 -->
        <el-dialog v-model="dialogFormVisible" title="修改评分" width="30%" @closed="resetForm">
            <el-form ref="dataFormRef" :model="ratingForm" :rules="rules" label-width="100px" label-position="left">
                <el-form-item label="我的评分:" prop="rating">
                    <el-input-number v-model="ratingForm.rating" :precision="1" :step="0.1" :min="0" :max="5" />
                </el-form-item>
            </el-form>
            <template #footer>
                <el-button @click="closeDialog">取消</el-button>
                <el-button type="primary" :loading="loading" @click="handleCreateOrUpdate">确认</el-button>
            </template>
        </el-dialog>


    </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRoute } from 'vue-router';
import useUserStore from '@/store/modules/user';
import { travelDetail, HotSpotsList, travelCommentList, travelCommentAdd, travelCollect, SpotRecommendationApi, SpotRecommendationDetailApi, RecommendSimilarSpotList } from '@/api/data/index.js';
import { ElMessage } from 'element-plus';
import { useRouter } from 'vue-router';
const router = useRouter();

const route = useRoute();
const detailData = ref({});
const hotSpots = ref([]);
const SpotRecommendation = ref([]);
const dialogFormVisible = ref(false);

const comments = ref([]);
const newComment = ref('');

const userStore = useUserStore();
const dataFormRef = ref(null);
const loading = ref(false);


const dialogVisible = ref(false);
const selectedRecommendation = ref({});
const RecommendSimilarSpot = ref(null);


// 定义一个方法来处理点击事件
const handleRowClick = async (row) => {
    try {
        const res = await SpotRecommendationDetailApi({ title: row.title });
        if (res.code === 200) {
            selectedRecommendation.value = res.data;
            dialogVisible.value = true;
        }
    } catch (error) {
        console.error('Failed to fetch recommendation details:', error);
    }
};

const goToDetail = async (row) => {
    router.push({
        path: `/travel/detail/${row.id}`
    });
    route.params.id = row.id;
    await fetchData();
    await fetchComments();
};



const formatDate = (isoString) => {
    const date = new Date(isoString);
    return new Intl.DateTimeFormat('zh-CN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
        hour12: false, // 使用24小时制
    }).format(date);
};



const fetchComments = async () => {
    try {
        const res = await travelCommentList({ spots: route.params.id });
        if (res.code === 200) {
            comments.value = res.data.results.map(comment => {
                return {
                    ...comment,
                    create_date: formatDate(comment.create_date),
                };
            });

        }
    } catch (error) {
        console.error('Failed to fetch comments:', error);
    }
};

//获取当前页面数据
const fetchData = async () => {
    const id = route.params.id;
    try {
        const res = await travelDetail(id, userStore.id);
        if (res.code === 200) {
            detailData.value = res.data || {};
            const response = await HotSpotsList({ city: res.data.districtName });
            hotSpots.value = response.data;
            const res01 = await SpotRecommendationApi({ spots_id: id });
            SpotRecommendation.value = res01.data;
            const res02 = await RecommendSimilarSpotList(id);
            if (res02.code === 200) {
                RecommendSimilarSpot.value = res02.data;
            }
            else {
                ElMessage.error('操作失败,' + res02.message);
            }
            
        }
    } catch (error) {
        console.error('Failed to fetch detail data:', error);
    }
};



// 计算属性来处理描述信息
// const memo2Display = computed(() => detailData.value.memo2 ? detailData.value.memo2 : '四季皆宜');

// 判断用户是否登录
const isLoggedIn = computed(() => !!userStore.id);
const addComment = async () => {
    try {
        const res = await travelCommentAdd({
            review_content: newComment.value,
            spots: route.params.id,
            poiName: detailData.value.poiName,
            reviewer_id: userStore.username,
            reviewer_name: userStore.nickname || '匿名用户',
            rating: 0
        });
        if (res.code === 200) {
            newComment.value = '';
            fetchComments(); // 更新评论列表
        }
    } catch (error) {
        console.error('Failed to add comment:', error);
    }
};

const openEditDialog = () => {

    ratingForm.value.rating = detailData.value.rating;
    dialogFormVisible.value = true;
};
// 关闭对话框并重置表单
const closeDialog = () => {
    dialogFormVisible.value = false;
};

const ratingForm = ref({
    rating: null,
});

const rules = {
    rating: [
        { required: true, message: '请输入景点评分', trigger: 'blur' },
    ],
};

// 提交表单的方法
const handleCreateOrUpdate = async () => {
    try {
        await dataFormRef.value.validate();
        loading.value = true; // 开始加载动画
        const response = await travelCollect({
            user: userStore.id,
            qunar: route.params.id,
            rating: ratingForm.value.rating,
            is_collect: detailData.value.is_collect,
        });
        if (response.code === 200) {
            ElMessage.success("景点评分修改成功");
            fetchData();
            closeDialog();

        } else {
            ElMessage.error('保存失败，请稍后再试' + response.message);
        }
    } catch (error) {
        ElMessage.error('保存失败，请检查输入信息');
        console.error('Failed to create or update user:', error);
    } finally {
        loading.value = false;
    }
};

const toggleCollect = async () => {
    try {
        const newCollectStatus = !detailData.value.is_collect;
        const response = await travelCollect({
            user: userStore.id,
            qunar: route.params.id,
            rating: detailData.value.rating,
            is_collect: newCollectStatus,
        });
        if (response.code === 200) {
            detailData.value.is_collect = newCollectStatus;
            ElMessage.success(newCollectStatus ? "收藏成功" : "取消收藏成功");
        } else {
            ElMessage.error('操作失败，请稍后再试' + response.message);
        }
    } catch (error) {
        console.error('Failed to collect/uncollect spot:', error);
        ElMessage.error('请求过程中出现问题');
    }
};

onMounted(() => {
    fetchData();
    fetchComments();
});
</script>

<style scoped lang="scss">
.container {
    display: flex;
    width: 100%;
    margin-top: 20px;
}

.left {
    flex: 8;
    margin-right: 80px;
    height: 100%;
}

.right {
    flex: 2;
    padding: 3px;
    background-color: #f0f0f0;
}

.spot-card {
    height: 100%;
}

.spot-info {
    display: flex;
    align-items: center;
    justify-content: space-between;

    .image-container {
        flex-shrink: 0;
        margin-right: 10px;
    }

    .spot-image {
        width: 445px;
        height: auto;
        object-fit: contain;
    }

    .text-info {
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        width: 100%;

        .cn_tit {
            font-size: 30px;
            color: #666;
            cursor: pointer;
            transition: color .3s;

            &:hover {
                color: #00b5c2;
            }

        }

        .en_tit {
            display: flex;
            align-items: center;
            font-size: 20px;
            color: #ff525a;
            margin-left: 10px;
        }



        .cur_score {
            font-size: 30px;
            color: #1badb6;
        }

        .total_score {
            font-size: 16px;
            color: #666;
        }

        .description {
            margin-top: 10px;
        }
    }
}

.favorite-wrapper {
    margin-top: 20px;
    width: 110px;
    border: 1px solid #f80;
    padding: 2px 6px;
    border-radius: 4px;
    display: inline-flex;
    align-items: center;
    color: #f80;
    font-size: 20px;

}

.spots {
    font-size: 20px;
    color: #333;
    font-weight: bold;
    margin-top: 20px;
    text-align: center;
}

.e_title_content {
    color: #1badb6;
    font-size: 20px;
    line-height: 20px;
}

.comment-item {
    margin-top: 20px;

    .comment-content {
        p {
            font-size: 16px;
            line-height: 1.6;
            color: #333;
        }

        .comment-meta {
            margin-top: 10px;
            font-size: 14px;
            color: #999;

            span {
                display: inline-block;
            }
        }
    }
}
</style>