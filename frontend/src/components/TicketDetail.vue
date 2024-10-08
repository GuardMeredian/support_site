<template>
  <div class="container">
    <h2 v-if="ticket">Информация о заявке № {{ ticket.id }}</h2>
    <div v-if="ticket">
      <table class="table">
        <tbody>
          <tr>
            <th scope="row">Тема</th>
            <td>{{ ticket.title }}</td>
          </tr>
          <tr>
            <th scope="row">Организация</th>
            <td>{{ ticket.organization.lpucode }} - {{ ticket.organization.name }}</td>
          </tr>
          <tr>
            <th scope="row">Система</th>
            <td>{{ ticket.system.description }}</td>
          </tr>
          <tr>
            <th scope="row">Статус</th>
            <td>
              <span v-if="currentUserRoleId === 2">{{ ticket.status.description }}</span>
              <select v-else v-model="selectedStatus" class="form-control" @change="updateStatus">
                <option v-for="status in statuses" :key="status.id" :value="status.id">
                  {{ status.description }}
                </option>
              </select>
            </td>
          </tr>
          <tr>
            <th scope="row">Создал</th>
            <td>{{ ticket.creator.surname }}</td>
          </tr>
          <tr>
            <th scope="row">Оператор</th>
            <td>
              <span v-if="currentUserRoleId === 2">{{
                ticket.assigned ? ticket.assigned.surname : 'Не назначен'
              }}</span>
              <select
                v-else
                v-model="selectedOperator"
                class="form-control"
                @change="updateOperator"
              >
                <option v-for="operator in operators" :key="operator.id" :value="operator.id">
                  {{ operator.surname }} {{ operator.name }} {{ operator.secname }}
                </option>
                <option v-if="!selectedOperator" value="">Не назначен</option>
              </select>
            </td>
          </tr>
          <tr>
            <th scope="row">Дата создания</th>
            <td>{{ ticket.created_at }}</td>
          </tr>
          <tr>
            <th scope="row">Контрольная дата</th>
            <td>
              <span v-if="currentUserRoleId === 2">{{ ticket.control_date }}</span>
              <input
                v-else
                type="date"
                class="form-control"
                :value="ticket.control_date"
                @input="updateControlDate"
              />
            </td>
          </tr>
        </tbody>
      </table>
      <h4>Описание:</h4>
      <p>{{ ticket.description }}</p>
      <h4>Сообщения:</h4>
      <ul>
        <li v-for="message in ticket.messages" :key="message.id" class="alert alert-info">
          <strong
            >{{ message.creator.surname }} {{ message.creator.name.substring(0, 1) }}.{{
              message.creator.secname.substring(0, 1)
            }}
            ({{ message.created_at.split('T')[0] }}):</strong
          >
          {{ message.content }}
        </li>
      </ul>
      <h4>
        Вложения:<button
          type="button"
          class="btn btn-primary"
          data-bs-toggle="modal"
          data-bs-target="#uploadModal"
        >
          Загрузить файл
        </button>
      </h4>
      <UploadModal @refresh-ticket-data="handleRefreshTicketData" />
      <ul>
        <li
          v-for="attachment in ticket.attachments"
          :key="attachment.id"
          class="alert alert-secondary"
        >
          <a :href="attachment.file_url" :download="attachment.filename">{{
            attachment.filename
          }}</a>
        </li>
      </ul>
      <h4>Добавить сообщение:</h4>
      <form @submit.prevent="addMessage">
        <div class="form-group">
          <textarea
            v-model="newMessage"
            class="form-control"
            rows="3"
            placeholder="Введите ваше сообщение"
            @input="autoResize"
            style="resize: none;"
          ></textarea>
        </div>
        <button type="submit" class="btn btn-primary mt-4 mb-5">Написать</button>
      </form>
    </div>
    <div v-else>
      <p>Загрузка...</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import apiService from '@/apiService'
import UploadModal from '@/components/UploadModal.vue'

const route = useRoute()
const ticket = ref(null)
const statuses = ref([])
const selectedStatus = ref(null)
const newMessage = ref('')
const operators = ref([])
const selectedOperator = ref('')

const currentUserRoleId = ref(null)

const autoResize = (event) => {
 event.target.style.height = 'auto'; // Сначала сбросить высоту
 event.target.style.height = `${event.target.scrollHeight}px`; // Затем установить высоту, равную scrollHeight
};

// Определение функции refreshTicketData
const refreshTicketData = async () => {
  try {
    const response = await apiService.getTicketDetail(route.params.ticketId)
    ticket.value = response.data
  } catch (error) {
    console.error('Ошибка при обновлении данных о заявке:', error)
  }
}

const handleRefreshTicketData = () => {
  refreshTicketData()
}

onMounted(async () => {
  try {
    const userResponse = await apiService.getUserData()
    const currentUser = userResponse.data.User
    currentUserRoleId.value = currentUser.role.id
    console.log(currentUserRoleId)
    const response = await apiService.getTicketDetail(route.params.ticketId)
    ticket.value = response.data
    if (currentUserRoleId.value !== 2) {
      const statusesResponse = await apiService.getStatuses()
      statuses.value = statusesResponse.data
      if (ticket.value && ticket.value.status && ticket.value.status.id) {
        selectedStatus.value = ticket.value.status.id
      }
      const OperatorsResponse = await apiService.getOperators()
      operators.value = OperatorsResponse.data
      if (ticket.value && ticket.value.assigned) {
        selectedOperator.value = ticket.value.assigned.id // Устанавливаем selectedOperator в id назначенного оператора
      }
    }
  } catch (error) {
    console.error('Ошибка при загрузке деталей тикета:', error)
  }
})

const updateStatus = async () => {
  try {
    await apiService.updateTicketStatus(ticket.value.id, selectedStatus.value)
    // Обновляем статус тикета в локальном состоянии
    ticket.value.status = statuses.value.find((status) => status.id === selectedStatus.value)
  } catch (error) {
    console.error('Ошибка при обновлении статуса тикета:', error)
  }
}

const updateControlDate = async (event) => {
  const newControlDate = event.target.value
  try {
    await apiService.updateTicketControlDate(ticket.value.id, newControlDate)
    ticket.value.control_date = newControlDate
  } catch (error) {
    console.error('Ошибка при обновлении контрольной даты:', error)
  }
}

// Метод для обновления оператора
const updateOperator = async () => {
  try {
    // Предполагается, что selectedOperator содержит id оператора
    const operatorId = selectedOperator.value
    console.log('selectedOperator = ', selectedOperator.value)
    if (operatorId) {
      await apiService.updateTicketOperator(ticket.value.id, operatorId)
      // Обновляем оператора тикета в локальном состоянии
      ticket.value.assigned = operators.value.find((operator) => operator.id === operatorId)
      console.log(ticket.value)
    } else {
      console.error('Оператор не выбран')
    }
  } catch (error) {
    console.error('Ошибка при обновлении оператора тикета:', error)
  }
}

const addMessage = async () => {
  try {
    // Получаем токен из куки
    const token = document.cookie
      .split('; ')
      .find((cookie) => cookie.startsWith('user_access='))
      .split('=')[1]

    // Делаем запрос к конечной точке /auth/user для получения данных пользователя
    const userResponse = await apiService.getUserData()

    // Извлекаем данные пользователя из ответа
    const userData = userResponse.data.User
    console.log(userResponse.data)

    await apiService.addMessage(ticket.value.id, {
      content: newMessage.value,
      ticket_id: ticket.value.id,
      creator: {
        id: userData.id,
        surname: userData.surname,
        name: userData.name,
        secname: userData.secname
      },
      created_at: new Date().toISOString()
    })
    newMessage.value = ''
    const response = await apiService.getTicketDetail(route.params.ticketId)
    ticket.value = response.data
  } catch (error) {
    console.error('Ошибка при добавлении сообщения:', error)
  }
}
// Убедитесь, что handleRefreshTicketData возвращается из setup
</script>
