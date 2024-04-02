import axios from 'axios'

const apiClient = axios.create({
  baseURL: 'http://127.0.0.1:8000',
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
    const params = new URLSearchParams()
    Object.keys(filters).forEach((key) => {
      if (filters[key]) {
        params.append(key, filters[key])
      }
    })
    return apiClient.get(`/tickets/all_tickets?${params.toString()}`)
  },
  getTicketDetail(ticketId) {
    return apiClient.get(`/tickets/${ticketId}`)
  },
  getStatuses(roleId) {
    // Проверяем, не является ли текущий пользователь пользователем с role_id = 2
    if (roleId !== 2) {
      return apiClient.get('/statuses/')
    } else {
      // Если пользователь имеет role_id = 2, возвращаем Promise, который не выполняется
      return Promise.resolve({ data: [] })
    }
  },
  updateTicketStatus(ticketId, statusId) {
    return apiClient.put(`/tickets/${ticketId}/status`, { status_id: statusId })
  },
  addMessage(ticketId, messageContent) {
    return apiClient.post(`/tickets/${ticketId}/add_message`, {
      content: messageContent.content,
      ticket_id: messageContent.ticket_id,
      creator: messageContent.creator,
      created_at: messageContent.created_at
    })
  },
  getUserData() {
    return apiClient.get('/auth/user')
  },
  getSystems() {
    return apiClient.get('/systems/')
  },
  createTicket(ticketData) {
    return apiClient.post(`/tickets/add_ticket`, ticketData)
  },
  getOperators(roleId) {
    // Проверяем, не является ли текущий пользователь пользователем с role_id = 2
    if (roleId !== 2) {
      return apiClient.get('auth/users/')
    } else {
      // Если пользователь имеет role_id = 2, возвращаем Promise, который не выполняется
      return Promise.resolve({ data: [] })
    }
  },
  updateTicketOperator(ticketId, operator_id) {
    return apiClient.put(`/tickets/${ticketId}/operator`, { assigned_id: operator_id })
  },
  getOrgs(roleId) {
    // Проверяем, не является ли текущий пользователь пользователем с role_id = 2
    if (roleId !== 2) {
      return apiClient.get('/med_org/med_orgs/')
    } else {
      // Если пользователь имеет role_id = 2, возвращаем Promise, который не выполняется
      return Promise.resolve({ data: [] })
    }
  },
  getNews() {
    return apiClient.get('/news/news')
  },
  getOrgDetail(lpucode) {
    return apiClient.get(`/med_org/${lpucode}`)
  },
  uploadFile(ticketId, formData) {
    return apiClient.post(`/tickets/upload_file/${ticketId}`, formData)
  },
  updateTicketControlDate(ticketId, control_date) {
    return apiClient.put(`/tickets/${ticketId}/control_date`, { control_date: control_date })
  }
  // Добавьте другие методы для взаимодействия с API по мере необходимости
}
