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
  getStatuses() {
    return apiClient.get('/statuses/')
  },
  updateTicketStatus(ticketId, statusId) {
    return apiClient.put(`/tickets/${ticketId}/status`, { status_id: statusId });
  },
  addMessage(ticketId, messageContent) {
    return apiClient.post(`/tickets/${ticketId}/add_message`, {
      content: messageContent.content,
      ticket_id: messageContent.ticket_id,
      creator: messageContent.creator,
      created_at: messageContent.created_at
    });
  },
  getUserData() {
    return apiClient.get('/auth/user');
  }
  // Добавьте другие методы для взаимодействия с API по мере необходимости
}



