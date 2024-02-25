import axios from 'axios'

const apiClient = axios.create({
  baseURL: 'http://localhost:8000',
  withCredentials: true // Это позволит отправлять и получать куки
})

export default {
  login(credentials) {
    return apiClient.post('/auth/login', credentials)
  },
  logout() {
    return apiClient.post('/auth/logout')
  },
  getTickets() {
    return apiClient.get('/tickets/all_tickets')
  },
  getTicketDetail(ticketId) {
    return apiClient.get(`/tickets/${ticketId}`)
  },
  // Добавьте другие методы для взаимодействия с API по мере необходимости
}
