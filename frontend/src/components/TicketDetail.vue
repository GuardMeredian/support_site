<template>
    <div class="container">
      <h2 v-if="ticket">Информация о заявке № {{ ticket.id }}</h2>
      <div v-if="ticket">
        <h3>{{ ticket.title }}</h3>
        <p><strong>Код организации:</strong> {{ ticket.organization.lpucode }}</p>
        <p><strong>Описание системы:</strong> {{ ticket.system.description }}</p>
        <p><strong>Статус:</strong> {{ ticket.status.description }}</p>
        <p><strong>Фамилия создателя:</strong> {{ ticket.creator.surname }}</p>
        <p><strong>Дата создания:</strong> {{ ticket.created_at }}</p>
        <p><strong>Дата обновления:</strong> {{ ticket.updated_at }}</p>
        <h4>Описание:</h4>
        <p>{{ ticket.description }}</p>
        <h4>Сообщения:</h4>
        <ul>
          <li v-for="message in ticket.messages" :key="message.id">
           {{ message.creator.surname }}: {{ message.content }} ({{ message.created_at }})
          </li>
        </ul>
        <h4>Вложения:</h4>
        <ul>
          <li v-for="attachment in ticket.attachments" :key="attachment.id">
            <a :href="attachment.file_url">{{ attachment.filename }}</a>
          </li>
        </ul>
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


onMounted(async () => {
  try {
    const response = await apiService.getTicketDetail(route.params.ticketId)
    ticket.value = response.data
  } catch (error) {
    console.error('Ошибка при загрузке деталей тикета:', error)
  }
})
  </script>