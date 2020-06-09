import Vue from 'vue'
import Router from 'vue-router'
import HelloWorld from '@/components/HelloWorld'
import AdminHome from '@/adminviews/Index'
import IntvweeHome from '@/intvweeviews/Index'
import LogRegHome from '@/login/Index'
import RegisterHome from '@/register/Index'
import HrHome from '@/hrs/Index'
import IntvwerHome from '@/intvwerviews/Index'
import ScheduleView from '@/intvwerviews/ScheduleView'
import Error from '@/error/Error'

Vue.use(Router)

var router = new Router({
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
      path: '/interviewer',
      name: 'Interviewer',
      component: IntvwerHome
    },
    {
      path: '/schedule',
      name: 'ScheduleView',
      component: ScheduleView
    },
    {
      path: '/login',
      name: 'Login',
      component: LogRegHome
    },
    {
      path: '/register',
      name: 'Register',
      component: RegisterHome
    },
    {
      path: '/hr',
      name: 'Hr',
      component: HrHome
    },
    {
      path: '*',
      name: 'Error',
      component: Error
    }
  ]
})
router.beforeEach((to, from, next) => {
  if (to.path === '/login') {
    window.hideLogin = false
  }
  next()
})

export default router
