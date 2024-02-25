<template>
  <div class="container">
    <h2>Заявки</h2>
    <table class="table">
      <thead>
        <tr>
          <th scope="col">#</th>
          <th scope="col">Код организации</th>
          <th scope="col">Заголовок</th>
          <th scope="col">Описание системы</th>
          <th scope="col">Статус</th>
          <th scope="col">Фамилия создателя</th>
          <th scope="col">Дата создания</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="ticket in tickets" :key="ticket.id">
          <th scope="row">{{ ticket.id }}</th>
          <td>{{ ticket.organization.lpucode }}</td>
          <td>
            <RouterLink :to="`/tickets/${ticket.id}`">{{ ticket.title }}</RouterLink>
          </td>
          <td>{{ ticket.system.description }}</td>
          <td>{{ ticket.status.description }}</td>
          <td>{{ ticket.creator.surname }}</td>
          <td>{{ ticket.created_at }}</td>
        </tr>
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
    tickets.value = response.data
  } catch (error) {
    // Обработка ошибок, например, отображение сообщения об ошибке
  }
})
</script>
