<template>
  <div class="container">
    <h2>Заявки</h2>
    <table class="table">
      <thead>
        <tr>
          <th scope="col">#</th>
          <th scope="col">Код организации</th>
          <th scope="col">Заголовок</th>
          <th scope="col">Система</th>
          <th scope="col">Статус</th>
          <th scope="col">Оператор</th>
          <th scope="col">Создал</th>
          <th scope="col">Дата создания</th>
        </tr>
      </thead>
      <tbody>
        <template v-for="ticket in tickets">
          <tr v-if="ticket.status.id ===  4" :key="`completed-${ticket.id}`" class="table-success">
            <th scope="row">{{ ticket.id }}</th>
            <td>{{ ticket.organization.lpucode }}</td>
            <td>
              <RouterLink :to="`/tickets/${ticket.id}`">{{ ticket.title }}</RouterLink>
            </td>
            <td>{{ ticket.system.description }}</td>
            <td>{{ ticket.status.description }}</td>
            <td>
              <span v-if="ticket.assigned">{{ ticket.assigned.surname }}</span>
              <span v-else>Не назначен</span>
            </td>
            <td>{{ ticket.creator.surname }}</td>
            <td>{{ ticket.created_at }}</td>
          </tr>
          <tr v-else-if="ticket.assigned" :key="`assigned-${ticket.id}`" class="table-warning">
            <th scope="row">{{ ticket.id }}</th>
            <td>{{ ticket.organization.lpucode }}</td>
            <td>
              <RouterLink :to="`/tickets/${ticket.id}`">{{ ticket.title }}</RouterLink>
            </td>
            <td>{{ ticket.system.description }}</td>
            <td>{{ ticket.status.description }}</td>
            <td>{{ ticket.assigned.surname }}</td>
            <td>{{ ticket.creator.surname }}</td>
            <td>{{ ticket.created_at }}</td>
          </tr>
          <tr v-else :key="`unassigned-${ticket.id}`" class="table-info">
            <th scope="row">{{ ticket.id }}</th>
            <td>{{ ticket.organization.lpucode }}</td>
            <td>
              <RouterLink :to="`/tickets/${ticket.id}`">{{ ticket.title }}</RouterLink>
            </td>
            <td>{{ ticket.system.description }}</td>
            <td>{{ ticket.status.description }}</td>
            <td>Не назначен</td>
            <td>{{ ticket.creator.surname }}</td>
            <td>{{ ticket.created_at }}</td>
          </tr>
        </template>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import apiService from '@/apiService'

const tickets = ref([])

onMounted(async () => {
  try {
    const response = await apiService.getTickets()
    response.data.sort((a, b) => b.id - a.id);
    tickets.value = response.data
  } catch (error) {
    // Обработка ошибок, например, отображение сообщения об ошибке
  }
})
</script>
