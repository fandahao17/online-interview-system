// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import App from './App'
import router from './router'
import axios from 'axios'
import store from './store/store'
import VueSocketIO from 'vue-socket.io'
Vue.use(VueSocketIO, 'http://106.14.227.202:8011')
// Vue.use(VueSocketIO, 'http://localhost:8011')
// Vue.use(new VueSocketIO({
//   debug: true,
//   connection: 'http://localhost:8080'
// }))

Vue.prototype.axios = axios

Vue.config.productionTip = false

Vue.use(ElementUI)

Vue.prototype.$eventHub = Vue.prototype.$eventHub || new Vue()

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,
  components: { App },
  template: '<App/>',
  data: {
    eventHub: new Vue()
  }
})
