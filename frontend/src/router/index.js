import { createRouter, createWebHistory } from 'vue-router'
import { isAuthenticated, checkAuthentication } from '@/utils/authHelper'
import Login from '@/components/LoginForm.vue'
import Tickets from '@/components/TicketsList.vue'
import TicketDetail from '@/components/TicketDetail.vue'
import OrganizationsList from '@/components/OrganizationsList.vue'
import NewsList from '@/components/NewsList.vue'
import OrgDetail from '@/components/OrgDetail.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: Login
    },
    {
      path: '/tickets',
      name: 'tickets',
      component: Tickets,
      meta: { requiresAuth: true } // Добавляем мета-тег для маршрутов, требующих аутентификации
    },
    {
      path: '/tickets/:ticketId',
      name: 'ticketDetail',
      component: TicketDetail,
      props: true,
      meta: { requiresAuth: true } // Добавляем мета-тег для маршрутов, требующих аутентификации
    },
    {
      path: '/orgs',
      name: 'orgs',
      component: OrganizationsList,
      meta: { requiresAuth: true } // Добавляем мета-тег для маршрутов, требующих аутентификации
    },
    {
      path: '/news',
      name: 'news',
      component: NewsList,
      meta: { requiresAuth: true } // Добавляем мета-тег для маршрутов, требующих аутентификации
    },
    {
      path: '/med_org/:orgid',
      name: 'OrgDetail',
      component: OrgDetail,
      props: true,
      meta: { requiresAuth: true } // Добавляем мета-тег для маршрутов, требующих аутентификации
    }
    // Добавьте другие маршруты по мере необходимости
  ]
})

router.beforeEach((to, from, next) => {
  checkAuthentication()
  if (to.matched.some((record) => record.meta.requiresAuth)) {
    if (isAuthenticated.value) {
      next()
    } else {
      next({
        name: 'login',
        query: { redirect: to.fullPath }
      })
    }
  } else {
    next() // Для маршрутов, которые не требуют аутентификации
  }
})

export default router
