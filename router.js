// router.js
import Router from "vue-router"
import Vue from "vue"

Vue.use(Router)

export default new Router({
  base: "/", // this should match the root path for your app
  mode: "history",
  routes: [{
    name: "UserMeta",
    path: "/user/:username@",
    component: () => import("./path/to/UserMeta.vue"),
    props: true
  }, {
    name: "User",
    path: "/user/:username",
    component: () => import("./path/to/User.vue"),
    props: true
  }]
})