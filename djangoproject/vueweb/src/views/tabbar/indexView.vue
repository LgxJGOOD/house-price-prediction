<template>
    <div class="tabbar">
        <div class="tabbar-left">
          <Breadcrumb></Breadcrumb>
        </div>
        <div class="tabbar-right">
           <Setting></Setting>
        </div>
    </div>
</template>

<script setup>
import Breadcrumb from './breadcrumb/indexView.vue'
import Setting from './setting/indexView.vue'
</script>

<style scoped lang="scss">
.tabbar {
    width: 100%;
    height: 100%;
    display: flex;
    justify-content: space-between;
    align-items: center;

    .tabbar-left {
        display: flex;
        align-items: center;

        // margin-left: 10px;
        .el-breadcrumb {
            font-size: 14px;
            color: #333;

            .el-breadcrumb__item {
                a {
                    color: #333;
                }
            }
        }
    }

    .tabbar-right {
        display: flex;
        align-items: center;

        .el-dropdown {
            margin-right: 10px;
        }
    }
}
</style>