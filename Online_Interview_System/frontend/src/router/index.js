import Vue from 'vue'
import Router from 'vue-router'
import HelloWorld from '@/components/HelloWorld'
import AdminHome from '@/adminviews/Index'
import IntvweeHome from '@/intvweeviews/Index'
import LogRegHome from '@/login/Index'
import RegisterHome from '@/register/Index'
import HrHome from '@/hrs/Index'
import HrWatch from '@/hrs/HrWatch'
import HrRecall from '@/hrs/HrRecall'
import HrVideo from '@/hrs/HrVideo'
import IntvwerHome from '@/intvwerviews/Index'
import ScheduleView from '@/intvwerviews/ScheduleView'
import ItvrRoom from '@/itvrroom/Index'
import Error from '@/error/Error'
import HrWatchHome from '@/hrviews/Index'

Vue.use(Router)

var router = new Router({
  routes: [
    {
      path: '/',
      name: 'HelloWorld',
      component: HelloWorld,
      meta: {
        title: '首页 - 在线面试平台'
      }
    },
    {
      path: '/admin',
      name: 'Admin',
      component: AdminHome,
      meta: {
        title: '管理员 - 在线面试平台'
      }
    },
    {
      path: '/interviewee/:roomid',
      name: 'Interviewee',
      component: IntvweeHome,
      meta: {
        title: '面试 - 在线面试平台'
      }
    },
    {
      path: '/interviewer/:roomid',
      name: 'InterviewerRoom',
      component: ItvrRoom,
      meta: {
        title: '面试 - 在线面试平台'
      }
    },
    {
      path: '/interviewer',
      name: 'Interviewer',
      component: IntvwerHome,
      meta: {
        title: '面试官 - 在线面试平台'
      }
    },
    {
      path: '/schedule',
      name: 'ScheduleView',
      component: ScheduleView,
      meta: {
        title: '面试安排 - 在线面试平台'
      }
    },
    {
      path: '/login',
      name: 'Login',
      component: LogRegHome,
      meta: {
        title: '登陆 - 在线面试平台'
      }
    },
    {
      path: '/register',
      name: 'Register',
      component: RegisterHome,
      meta: {
        title: '注册 - 在线面试平台'
      }
    },
    {
      path: '/hr',
      name: 'Hr',
      component: HrHome,
      meta: {
        title: 'HR - 在线面试平台'
      }
    },
    {
      path: '/watch',
      name: 'Watch',
      component: HrWatch,
      meta: {
        title: '观看面试 - 在线面试平台'
      }
    },
    {
      path: '/hr/:roomid',
      name: 'HrviewRoom',
      component: HrWatchHome,
      meta: {
        title: '观看面试 - 在线面试平台'
      }
    },
    {
      path: '/recall',
      name: 'Recall',
      component: HrRecall,
      meta: {
        title: '回溯面试 - 在线面试平台'
      }
    },
    {
      path: '/recall/:roomid/:filename',
      name: 'RecallVideo',
      component: HrVideo,
      meta: {
        title: '回溯面试 - 在线面试平台'
      }
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
  /* 路由发生变化修改页面title */
  if (to.meta.title) {
    document.title = to.meta.title
  }
  next()
})

export default router
