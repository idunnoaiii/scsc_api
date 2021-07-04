import Vue from 'vue'
import VueRouter from 'vue-router'
import Login from '../views/pages/Login.vue'
import POS from '../views/pages/POS.vue'
import User from '../views/pages/User'
import Inventory from '../views/pages/Inventory'
import Transaction from '../views/pages/Transaction'
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
    // children:[{
    //   path:'pos',
    //   component:POS
    // }]
  },
  {
    path: '/users',
    name: 'User',
    component: User
  }, 
  {
    path: '/inventory',
    name: 'Inventory',
    component: Inventory
  },
  {
    path: '/transaction',
    name: 'Transaction',
    component: Transaction
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

export default router
