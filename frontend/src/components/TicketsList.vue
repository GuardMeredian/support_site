<template>
  <div class="container">
    <h2>Заявки</h2>
    <hr>
    <button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#createTicketModal">
      Создать заявку
    </button>
    <hr>
    <CreateTicketModal @ticketCreated="onTicketCreated" />
    <h4>Фильтры</h4>
    <FiltersBar
      :ticket_id="ticket_id"
      :systems="systems"
      :operators="operators"
      :statuses="statuses"
      :organizations="organizations"
      @filter-change="onFilterChange"
    />
    <hr>
    <table class="table table-hover">
      <thead>
        <tr>
          <th scope="col">#</th>
          <th scope="col">Код организации</th>
          <th scope="col">Тема</th>
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
              <RouterLink class="no-highlight" :to="`/tickets/${ticket.id}`">
                <strong>{{ ticket.title }}</strong>
              </RouterLink>
            </td>
            <td>{{ ticket.system.description }}</td>
            <td>{{ ticket.status.description }}</td>
            <td>
              <span v-if="ticket.assigned">{{ ticket.assigned.surname }}</span>
              <span v-else><i>Регистрируется</i></span>
            </td>
            <td>{{ ticket.creator.surname }}</td>
            <td>{{ ticket.created_at }}</td>
          </tr>
          <tr v-else-if="ticket.assigned" :key="`assigned-${ticket.id}`" class="table-warning">
            <th scope="row">{{ ticket.id }}</th>
            <td>{{ ticket.organization.lpucode }}</td>
            <td>
              <RouterLink class="no-highlight" :to="`/tickets/${ticket.id}`"><strong>{{ ticket.title }}</strong></RouterLink>
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
              <RouterLink class="no-highlight" :to="`/tickets/${ticket.id}`"><strong>{{ ticket.title }}</strong></RouterLink>
            </td>
            <td>{{ ticket.system.description }}</td>
            <td>{{ ticket.status.description }}</td>
            <td><i>Регистрируется</i></td>
            <td>{{ ticket.creator.surname }}</td>
            <td>{{ ticket.created_at }}</td>
          </tr>
        </template>
      </tbody>
    </table>
  </div>
</template>

<style scoped>
.no-highlight {
 text-decoration: none;
 color: inherit;
}
</style>

<script setup>
import { ref, onMounted } from 'vue'
import apiService from '@/apiService'

import CreateTicketModal from '@/components/CreateTicketModal.vue'
import FiltersBar from '@/components/FiltersBar.vue'

const ticket_id = ref(null)
const systems = ref([])
const operators = ref([])
const statuses = ref([])
const organizations = ref([]) 

const tickets = ref([])

onMounted(async () => {
 // Загрузка систем и статусов для фильтров
 const systemsResponse = await apiService.getSystems()
 systems.value = systemsResponse.data
 const operatorsResponse = await apiService.getOperators()
 operators.value = operatorsResponse.data
 const statusesResponse = await apiService.getStatuses()
 statuses.value = statusesResponse.data
 const organizationsResponse = await apiService.getOrgs()
 organizations.value = organizationsResponse.data
 console.log(organizations.value)

 // Загрузка тикетов с начальными фильтрами
 fetchTickets()
})

const fetchTickets = async (filters = {}) => {
 const response = await apiService.getTickets(filters);
 tickets.value = response.data.sort((a, b) => b.id - a.id);
}

const onFilterChange = (filters) => {
 fetchTickets(filters)
}

// Слушаем событие 'ticketCreated' для обновления списка тикетов
const onTicketCreated = () => {
 fetchTickets()
}
</script>