import { createRouter, createWebHistory } from 'vue-router'
import Login from '@/components/LoginForm.vue' // Добавьте этот импорт
import Tickets from '@/components/TicketsList.vue' // Добавьте этот импорт
import TicketDetail from '@/components/TicketDetail.vue'

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
      component: Tickets
    },
    {
      path: '/tickets/:ticketId',
      name: 'ticketDetail',
      component: TicketDetail,
      props: true
    }
    // Добавьте другие маршруты по мере необходимости
  ]
})

export default router
