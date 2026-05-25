import { createRouter, createWebHistory } from "vue-router"

import LoginView from "../views/LoginView.vue"
import RegisterView from "../views/RegisterView.vue"
import DashboardView from "../views/DashboardView.vue"


const router = createRouter({
  history: createWebHistory(),

  routes: [
    {
      path: "/",
      component: LoginView
    },
    {
      path: "/register",
      component: RegisterView
    },
    {
      path: "/dashboard",
      component: DashboardView,
      meta: {
        requiresAuth: true
      }
    }
  ]
})


router.beforeEach((to, from, next) => {
  const token = localStorage.getItem("token")

  if (to.meta.requiresAuth && !token) {
    next("/")
  } else {
    next()
  }
})


export default router