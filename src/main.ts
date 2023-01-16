import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import ElementPlus from 'element-plus'
import Vue from 'vue'
import { createRouter, createWebHistory, createWebHashHistory } from 'vue-router'
import Holding from './components/Holding.vue'
import Login from './components/Login.vue'
import Virtue from './components/Virtue.vue'
import Borrowed from './components/Borrowed.vue'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
const router = createRouter({
    history: createWebHistory(),
    routes: [
      { path: '/', component: Holding
      ,meta: {requiresAuth: true} 
    },
      { path: '/login', component: Login  },
      { path: '/virtue', component: Virtue},
      { path: '/borrow', component: Borrowed,meta: {requiresAuth: true}  },
    ],
  })
router.beforeEach((to, from, next) => {
const token = window.localStorage.getItem('WEDORM-uid') // TODO: valid own identifier

if (
  to.matched.some(record => record.meta.requiresAuth) && 
(!token || token === null)) 
{
    // 1. 用户未登录，但想访问需要认证的相关路由时，跳转到 登录 页
    // Vue.toasted.show('Please log in to access this page.', { icon: 'fingerprint' })
    console.log(to.matched)
    window.alert('未登录')
    next({
      path: '/login',
      query: { redirect: to.fullPath }
    })
  } else if (token !== '' && (to.name == 'Login')) {
    // 4. 用户已登录，但又去访问 登录/注册/请求重置密码/重置密码 页面时不让他过去
    next({
      path: from.fullPath
    })
  } else if (to.matched.length === 0) {
    // 5. 要前往的路由不存在时
    window.alert('404：页面不存在')
    if (from.name) {
      next({
        name: from.name
      })
    } else {
      next({
        path: '/'
      })
    }
  }
  else
  {
    // 6. 正常路由出口
    next()
  }
})

createApp(App).use(ElementPlus).use(router).mount('#app')
// 
// for ([name, comp] of Object.entries(ElementPlusIconsVue)) {
//   app.component(name, comp);
// }