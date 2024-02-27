<template>
  <div class="container">
    <h2>Заявки</h2>
    <hr>
    <button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#createTicketModal">
      Создать заявку
    </button>
    <hr>
    <CreateTicketModal @ticketCreated="onTicketCreated" />
    <FiltersBar
      :systems="systems"
      :operators="operators"
      :statuses="statuses"
      @filter-change="onFilterChange"
    />
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
import { ref, onMounted, watchEffect } from 'vue'
import apiService from '@/apiService'

import CreateTicketModal from '@/components/CreateTicketModal.vue'
import FiltersBar from '@/components/FiltersBar.vue'


const systems = ref([]) // Инициализация массива систем
const operators = ref([])
const statuses = ref([]) // Инициализация массива операторов


const tickets = ref([])

onMounted(async () => {
  // Загрузка систем и операторов для фильтров
  const systemsResponse = await apiService.getSystems()
  systems.value = systemsResponse.data
  const operatorsResponse = await apiService.getOperators()
  operators.value = operatorsResponse.data
  const statusesResponse = await apiService.getStatuses()
  statuses.value = statusesResponse.data

  // Загрузка тикетов с начальными фильтрами
  fetchTickets()
})

const fetchTickets = async (filters) => {
  try {
    const response = await apiService.getTickets(filters)
    tickets.value = response.data
  } catch (error) {
    console.error('Ошибка при загрузке тикетов:', error)
  }
}

const onFilterChange = (filters) => {
  // Удаляем пустые значения из объекта фильтров перед передачей в fetchTickets
  Object.keys(filters).forEach(key => filters[key] === '' && delete filters[key]);
  fetchTickets(filters)
}

// Слушаем событие 'ticketCreated' для обновления списка тикетов
const onTicketCreated = () => {
  fetchTickets()
}

// Используем watchEffect для автоматического обновления списка тикетов при изменении tickets
watchEffect(() => {
  fetchTickets()
})

// Экспортируем onTicketCreated, чтобы его можно было использовать в шаблоне или других компонентах
const emit = defineEmits(['ticketCreated', 'filter-change'])
</script>
