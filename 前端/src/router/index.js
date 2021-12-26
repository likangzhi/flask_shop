import Vue from 'vue'
import VueRouter from 'vue-router'
import Login from '../components/Login.vue'
import Home from '../components/home.vue'
import Welcome from '../components/welcome.vue'
import User from '../components/user/user.vue'
import Menu from '../components/power/menu.vue'
import Role from '../components/power/role.vue'
import Cate from '../components/good/cate.vue'
import Attr from '../components/good/attribute.vue'
import Good from '../components/good/good.vue'
import Add from '../components/good/add.vue'
import Order from '../components/order/order.vue'
import Data from '../components/data/data.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/login',
    component: Login
  },
  {
    path: '/home',
    component: Home,
    redirect: '/welcome',
    children: [{
      path: '/welcome', component: Welcome
    },
    {
      path: '/user_list', component: User
    },
    {
      path: '/menu_list', component: Menu
    },
    {
      path: '/role_list', component: Role
    },
    {
      path: '/cate_list', component: Cate
    },
    {
      path: '/attr_list', component: Attr
    },
    {
      path: '/goods_list', component: Good
    },
    {
      path: '/add_good', component: Add
    },
    {
      path: '/order_list', component: Order
    },
    {
      path: '/data_list', component: Data
    }
    ]
  }
]

const router = new VueRouter({
  routes
})

export default router

router.beforeEach((to, from, next) => {
  if (to.path === '/login') return next()
  const tokenStr = window.sessionStorage.getItem('token')
  if (!tokenStr) return next('/login')
  next()
})
