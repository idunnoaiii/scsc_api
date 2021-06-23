import Vue from 'vue'
import VueRouter from 'vue-router'
import Dashboard from '../views/layouts/Dashboard.vue'
import Login from '../views/layouts/Login.vue'

import Home from '../views/dashboard/Home.vue'
import User from '../views/dashboard/User.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/',
    name: 'Dashboard',
    component: Dashboard,
    children: [
      {
        path: '/user',
        component: User
      },
        {
        path: '/home',
        component: Home
      },
    ]
  },
  {
    path: '/about',
    name: 'About',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/About.vue')
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
