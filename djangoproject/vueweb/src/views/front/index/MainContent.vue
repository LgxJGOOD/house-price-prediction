<template>
  <div>
    <!-- Carousel -->
    <el-carousel height="500px">
      <el-carousel-item v-for="(item, index) in carouselImages" :key="index">
        <img :src="item" alt="carousel" style="width: 100%; height: 100%; object-fit: cover;">
      </el-carousel-item>
    </el-carousel>

    <!-- Popular Scenic Spots -->
    <div class="popular-spots">
      <h2>HOT SPOTS</h2>
      <p>&nbsp;&mdash;&mdash;&nbsp;热门景点&nbsp;&mdash;&mdash;&nbsp;</p>
      <el-row :gutter="16" style="justify-content: center; margin-top: 30px;">
        <el-col :span="8" v-for="(spot, index) in hotSpots" :key="index" style="margin-bottom: 20px;">
          <el-card style="height: 100%;">
            <div style="display: flex; height: 100%;">
              <div class="image-container" style="flex-shrink: 0; margin-right: 10px;">
                <img :src="spot.coverImageUrl" alt="Spot Image"
                  style="width: 200px; height: 100%; object-fit: contain;">
              </div>
              <div class="spot-info" style="display: flex; flex-direction: column; justify-content: space-between;">
                <span class="poiName">
                  {{ spot.poiName }}
                </span>
                <div> <span class="cur_score">{{ spot.commentScore }}</span>
                  <span class="total_score">/ 5分</span>
                  &nbsp;&nbsp;&nbsp;&nbsp;
                  <span> {{ spot.districtName }}</span>
                </div>
                <span class="en_tit">
                  <svg t="1739860943041" class="icon" viewBox="0 0 1024 1024" version="1.1"
                    xmlns="http://www.w3.org/2000/svg" p-id="1536" width="24" height="24">
                    <path
                      d="M442.514286 73.142857c82.529524 64.24381 140.239238 126.610286 173.129143 187.099429 31.158857 57.295238 43.666286 115.907048 37.546666 175.835428l-1.219047 9.996191 6.095238-4.973715a174.055619 174.055619 0 0 0 49.249524-69.607619l2.681904-7.411809 7.704381-23.04c82.285714 55.734857 123.440762 150.064762 123.440762 283.062857C841.142857 823.515429 665.795048 950.857143 521.654857 950.857143c-144.11581 0-308.224-85.333333-334.750476-263.875048-26.550857-178.541714 83.480381-261.90019 158.427429-378.197333C395.288381 231.253333 427.690667 152.697905 442.514286 73.142857z m33.718857 154.575238c-17.554286 41.447619-39.424 82.407619-65.536 122.904381l-8.313905 12.653714c-8.411429 12.507429-17.310476 24.941714-28.818286 40.374858l-40.96 54.467047c-63.634286 86.869333-80.944762 136.021333-68.851809 217.526857 17.92 120.441905 128.341333 197.778286 257.901714 197.778286 120.905143 0 241.785905-110.933333 241.785905-249.344 0-61.976381-9.825524-111.323429-29.110857-149.699048-8.240762 9.411048-17.237333 18.285714-26.965334 26.59962l-159.085714 130.023619 26.697143-195.364572c6.41219-46.811429-2.462476-92.208762-27.648-138.483809-13.214476-24.30781-31.98781-49.737143-56.368762-76.166096l-8.338286-8.850285-6.387809 15.579428z"
                      p-id="1537" fill="#ff525a"></path>
                  </svg>
                  {{ spot.heatScore }}</span>
                <span style="margin-top: 10px;">{{ spot.shortFeatures }} {{ spot.tagNameList }}</span>
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <!-- 景区景点推荐 -->
    <!-- Popular Scenic Spots -->
    <div class="popular-spots">
      <h2>ATTRACTIONS</h2>
      <p>&nbsp;&mdash;&mdash;&nbsp;景点推荐(基于协同过滤算法推荐)&nbsp;&mdash;&mdash;&nbsp;</p>
      <el-row :gutter="16" style="justify-content: center; margin-top: 30px;">
        <el-col :span="8" v-for="(spot, index) in Spots" :key="index" style="margin-bottom: 20px;">
          <el-card style="height: 100%;">
            <div style="display: flex; height: 100%;">
              <div class="image-container" style="flex-shrink: 0; margin-right: 10px;">
                <img :src="spot.coverImageUrl" alt="Spot Image" style="width: 200px; height: 100%; object-fit: contain;">
              </div>
              <div class="spot-info" style="display: flex; flex-direction: column; justify-content: space-between;">
                <span class="cn_tit">
                  {{ spot.poiName }}
                </span>
                <div> <span class="cur_score">{{ spot.commentScore }}</span>
                  <span class="total_score">/ 5分</span>
                  &nbsp;&nbsp;&nbsp;&nbsp;
                  <span> {{ spot.districtName }}</span>
                </div>
                <span class="en_tit">
                  <svg t="1739860943041" class="icon" viewBox="0 0 1024 1024" version="1.1"
                    xmlns="http://www.w3.org/2000/svg" p-id="1536" width="24" height="24">
                    <path
                      d="M442.514286 73.142857c82.529524 64.24381 140.239238 126.610286 173.129143 187.099429 31.158857 57.295238 43.666286 115.907048 37.546666 175.835428l-1.219047 9.996191 6.095238-4.973715a174.055619 174.055619 0 0 0 49.249524-69.607619l2.681904-7.411809 7.704381-23.04c82.285714 55.734857 123.440762 150.064762 123.440762 283.062857C841.142857 823.515429 665.795048 950.857143 521.654857 950.857143c-144.11581 0-308.224-85.333333-334.750476-263.875048-26.550857-178.541714 83.480381-261.90019 158.427429-378.197333C395.288381 231.253333 427.690667 152.697905 442.514286 73.142857z m33.718857 154.575238c-17.554286 41.447619-39.424 82.407619-65.536 122.904381l-8.313905 12.653714c-8.411429 12.507429-17.310476 24.941714-28.818286 40.374858l-40.96 54.467047c-63.634286 86.869333-80.944762 136.021333-68.851809 217.526857 17.92 120.441905 128.341333 197.778286 257.901714 197.778286 120.905143 0 241.785905-110.933333 241.785905-249.344 0-61.976381-9.825524-111.323429-29.110857-149.699048-8.240762 9.411048-17.237333 18.285714-26.965334 26.59962l-159.085714 130.023619 26.697143-195.364572c6.41219-46.811429-2.462476-92.208762-27.648-138.483809-13.214476-24.30781-31.98781-49.737143-56.368762-76.166096l-8.338286-8.850285-6.387809 15.579428z"
                      p-id="1537" fill="#ff525a"></path>
                  </svg>
                  {{ spot.heatScore }}</span>
                <span style="margin-top: 10px;">{{ spot.shortFeatures }} {{ spot.tagNameList }}</span>
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { HotSpotsList, AttractionsViewList } from '@/api/data/index.js';
import useUserStore from '@/store/modules/user';
const userStore = useUserStore();
const imageContext = require.context('@/assets/banner', false, /\.(jpg|jpeg|png|gif)$/);
const carouselImages = ref(imageContext.keys().map(key => imageContext(key)));

const hotSpots = ref([]);
const Spots = ref([]);
const error = ref(null);

const fetchHotSpots = async () => {
  try {
    const response = await HotSpotsList({ city: '' });
    hotSpots.value = response.data;
  } catch (err) {
    error.value = err;
    console.error('获取热门景点信息失败:', err);
  }
};



const fetchSpots = async () => {
  try {
    const response = await AttractionsViewList(userStore.id);
    Spots.value = response.data;
  } catch (err) {
    error.value = err;
    console.error('获取推荐景点信息失败:', err);
  }
};

onMounted(() => {
  fetchHotSpots();
  fetchSpots();
});
</script>

<style scoped lang="scss">
.popular-spots {
  text-align: center;
  margin-top: 100px;

  h2 {
    margin-bottom: 5px;
    font-size: 30px;
    color: #409EFF;
  }

  p {
    font-size: 24px;
    color: #606266;
  }

  .el-row {
    width: 100%;
  }

  .el-card {
    border-radius: 4px;
    transition: all .5s;
  }

  .image-container {
    width: 200px;
    /* 设置固定宽度 */
    overflow: hidden;
  }

  img {
    width: 100%;
    height: 100%;
    object-fit: contain;
  }

  .spot-info {
    text-align: left;
    padding: 10px;

    .cn_tit {
      font-size: 20px;
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
    }

    .cur_score {
      font-size: 30px;
      color: #1badb6;
    }

    .total_score {
      font-size: 16px;
      color: #666;
    }


  }
}
</style>