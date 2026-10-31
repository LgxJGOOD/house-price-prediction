// eslint-disable-next-line no-unused-vars
import { createRouter, createWebHashHistory } from 'vue-router'
import { constantRoutes } from './router.js'


const router = createRouter({
    history: createWebHashHistory(),
    routes:constantRoutes,
    scrollBehavior() {
        return {
            left: 0,
            top: 0
        }
    }
})


export default router;