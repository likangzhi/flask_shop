import Vue from 'vue'
import App from './App.vue'
import router from './router'
import './plugins/element.js'
import './assets/css/global.css'
import axios from 'axios'
import qs from 'qs'

Vue.config.productionTip = false
Vue.prototype.$axios = axios
Vue.prototype.$qs = qs

axios.interceptors.request.use(
  config => {
    const tokenStr = window.sessionStorage.getItem('token')
    if (tokenStr) {
      config.headers.token = tokenStr
    }
    return config
  }
)

axios.interceptors.response.use(
  response => {
    if (response.data.stutas === 10016 || response.data.stutas === 10017) {
      window.sessionStorage.removeItem('token')
      router.replace(
        {
          path: '/login'
        }
      )
    }
    return response
  }
)

axios.defaults.baseURL = 'http://127.0.0.1:5000'
new Vue({
  router,
  render: h => h(App)
}).$mount('#app')
