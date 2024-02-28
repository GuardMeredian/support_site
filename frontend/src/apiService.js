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
  getTickets(filters = {}) {
    const params = new URLSearchParams();
    Object.keys(filters).forEach(key => {
      if (filters[key]) {
        params.append(key, filters[key]);
      }
    });
    return apiClient.get(`/tickets/all_tickets?${params.toString()}`);
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
  },
  getSystems() {
    return apiClient.get('/systems/')
  },
  createTicket(ticketData) {
    return apiClient.post(`/tickets/add_ticket`, ticketData);
  },
  getOperators() {
    return apiClient.get('auth/users/')
  },
  updateTicketOperator(ticketId, operator_id) {
    return apiClient.put(`/tickets/${ticketId}/operator`, { assigned_id: operator_id });
  },
  getOrgs() {
    return apiClient.get('/med_org/med_orgs/')
  },
  getNews() {
    return apiClient.get('/news/news')
  },
  getOrgDetail(orgid) {
    return apiClient.get(`/med_org/${orgid}`)
  }
  // Добавьте другие методы для взаимодействия с API по мере необходимости
}