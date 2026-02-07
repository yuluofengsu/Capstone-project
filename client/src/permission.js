import router from './router'
import store from './store'
import storage from 'store'
import { ADMIN_TOKEN, TOKEN } from '@/store/constants'

// 路由权限白名单
const allowList = ['admin-login', 'login', 'register', 'portal', 'search', 'detail', '403', '404']
// 前台登录地址
const loginRoutePath = '/index/login'
// 后台登录地址
const adminLoginRoutePath = '/admin-login'

//
// router.afterEach(() => {
//   NProgress.done() // finish progress bar
// })
