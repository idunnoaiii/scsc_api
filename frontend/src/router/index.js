import Vue from 'vue'
import VueRouter from 'vue-router'
import Login from '../views/pages/Login.vue'
import POS from '../views/pages/POS.vue'
import User from '../views/pages/User'
import Inventory from '../views/pages/Inventory'
import Transaction from '../views/pages/Transaction'
import Category from '../views/pages/Category'
import Discount from '../views/pages/Discount'
import Testlayout from '../views/pages/Testlayout'


Vue.use(VueRouter)

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/',
    name: 'POS',
    component: POS,
    meta: {
      requireLogin: true
    }
  },
  {
    path: '/users',
    name: 'User',
    component: User,
    meta: {
      requireLogin: true
    }
  },
  {
    path: '/inventory',
    name: 'Inventory',
    component: Inventory,
    meta: {
      requireLogin: true
    }
  },
  {
    path: '/transaction',
    name: 'Transaction',
    component: Transaction,
    meta: {
      requireLogin: true
    }
  },
  {
    path: '/category',
    name: 'Category',
    component: Category,
    meta: {
      requireLogin: true
    }
  },
    {
    path: '/discount',
    name: 'Discount',
    component: Discount,
    meta: {
      requireLogin: true
    }
  },
  {
    path: '/test',
    name: 'Test',
    component: Testlayout
  },
  {
    path: '/about',
    name: 'About',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    // component: () => import(/* webpackChunkName: "about" */ '../views/About.vue')
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})


router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.requireLogin) && !localStorage.getItem("token")) {
    next('/login')
  } else {
    next()
  }
})


export default router
