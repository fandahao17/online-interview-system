import Vue from 'vue'
import Router from 'vue-router'
import HelloWorld from '@/components/HelloWorld'
import AdminHome from '@/adminviews/Index'
import IntvweeHome from '@/intvweeviews/Index'
import LogRegHome from '@/login_register/Index'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'HelloWorld',
      component: HelloWorld
    },
    {
      path: '/admin',
      name: 'Admin',
      component: AdminHome
    },
    {
      path: '/interviewee',
      name: 'Interviewee',
      component: IntvweeHome
    },
    {
      path: '/login',
      name: 'Login',
      component: LogRegHome
    }
  ]
})
