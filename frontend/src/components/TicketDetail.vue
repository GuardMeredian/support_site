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
            <th scope="row">Код организации</th>
            <td>{{ ticket.organization.lpucode }}</td>
          </tr>
          <tr>
            <th scope="row">Система</th>
            <td>{{ ticket.system.description }}</td>
          </tr>
          <tr>
            <th scope="row">Статус</th>
            <td>
              <select v-model="selectedStatus" @change="updateStatus">
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
                <select v-model="selectedOperator" @change="updateOperator">
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
        </tbody>
      </table>
      <h4>Описание:</h4>
      <p>{{ ticket.description }}</p>
      <h4>Сообщения:</h4>
      <ul>
        <li v-for="message in ticket.messages" :key="message.id" class="alert alert-info">
          <strong>{{ message.creator.surname }} ({{ message.created_at }}):</strong> {{ message.content }}
        </li>
      </ul>
      <h4>Вложения:</h4>
      <ul>
        <li v-for="attachment in ticket.attachments" :key="attachment.id">
          <a :href="attachment.file_url">{{ attachment.filename }}</a>
        </li>
      </ul>
      <h4>Добавить сообщение:</h4>
      <form @submit.prevent="addMessage">
        <div class="form-group">
          <textarea v-model="newMessage" class="form-control" rows="3" placeholder="Введите ваше сообщение"></textarea>
        </div>
        <button type="submit" class="btn btn-primary">Написать</button>
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

const route = useRoute()
const ticket = ref(null)
const statuses = ref([])
const selectedStatus = ref(null) // Инициализируем selectedStatus как null
const newMessage = ref('')
const operators = ref([]) // Инициализация массива операторов
const selectedOperator = ref(null) // Инициализация выбранного оператора

onMounted(async () => {
  try {
    const response = await apiService.getTicketDetail(route.params.ticketId);
    ticket.value = response.data;
    const statusesResponse = await apiService.getStatuses();
    statuses.value = statusesResponse.data;
    if (ticket.value && ticket.value.status && ticket.value.status.id) {
      selectedStatus.value = ticket.value.status.id;
    }
    const OperatorsResponse = await apiService.getOperators();
    operators.value = OperatorsResponse.data;
    if (ticket.value && ticket.value.assigned) {
      selectedOperator.value = ticket.value.assigned.id; // Устанавливаем selectedOperator в id назначенного оператора
    }
  } catch (error) {
    console.error('Ошибка при загрузке деталей тикета:', error);
  }
});

const updateStatus = async () => {
  try {
    await apiService.updateTicketStatus(ticket.value.id, selectedStatus.value)
    // Обновляем статус тикета в локальном состоянии
    ticket.value.status = statuses.value.find(status => status.id === selectedStatus.value)
  } catch (error) {
    console.error('Ошибка при обновлении статуса тикета:', error)
  }
}

// Метод для обновления оператора
const updateOperator = async () => {
  try {
    // Предполагается, что selectedOperator содержит id оператора
    const operatorId = selectedOperator.value;
    console.log('selectedOperator = ',selectedOperator.value)
    if (operatorId) {
      await apiService.updateTicketOperator(ticket.value.id, operatorId);
      // Обновляем оператора тикета в локальном состоянии
      ticket.value.assigned = operators.value.find(operator => operator.id === operatorId);
      console.log(ticket.value)
    } else {
      console.error('Оператор не выбран');
    }
  } catch (error) {
    console.error('Ошибка при обновлении оператора тикета:', error);
  }
};


const addMessage = async () => {
  try {
    // Получаем токен из куки
    const token = document.cookie.split('; ').find(cookie => cookie.startsWith('user_access=')).split('=')[1];

    // Делаем запрос к конечной точке /auth/user для получения данных пользователя
    const userResponse = await apiService.getUserData();

    // Извлекаем данные пользователя из ответа
    const userData = userResponse.data.User;
    console.log(userResponse.data)

    await apiService.addMessage(ticket.value.id, {
      content: newMessage.value,
      ticket_id: ticket.value.id,
      creator: {
        id: userData.id,
        surname: userData.surname,
        name: userData.name,
        secname: userData.secname,
      },
    created_at: new Date().toISOString()
});
    newMessage.value = '';
    const response = await apiService.getTicketDetail(route.params.ticketId);
    ticket.value = response.data;
  } catch (error) {
    console.error('Ошибка при добавлении сообщения:', error);
  }
};
</script>