<template>
  <h4>Фильтры</h4>
  <div class="filters">
    <div class="row">
      <div class="col-md-4">
        <div class="form-group">
          <label for="ticketIdFilter">Номер заявки:</label>
          <input
            id="ticketIdFilter"
            class="form-control"
            v-model="ticketIdFilter"
            @change="emitFilterChange"
          />
        </div>
      </div>

      <div class="col-md-4">
        <div class="form-group">
          <label for="organizationFilter">Организации:</label>
          <select
            id="organizationFilter"
            class="form-control"
            v-model="organizationFilter"
            @change="emitFilterChange"
          >
            <option value="">Все</option>
            <option
              v-for="organization in organizations"
              :key="organization.id"
              :value="organization.id"
            >
              {{ organization.name }}
            </option>
          </select>
        </div>
      </div>

      <div class="col-md-4">
        <div class="form-group">
          <label for="systemFilter">Система:</label>
          <select
            id="systemFilter"
            class="form-control"
            v-model="systemFilter"
            @change="emitFilterChange"
          >
            <option value="">Все</option>
            <option v-for="system in systems" :key="system.id" :value="system.id">
              {{ system.description }}
            </option>
          </select>
        </div>
      </div>
    </div>

    <div class="row">
      <div class="col-md-6">
        <div class="form-group">
          <label for="statusFilter">Статус:</label>
          <select
            id="statusFilter"
            class="form-control"
            v-model="statusFilter"
            @change="emitFilterChange"
          >
            <option value="">Все</option>
            <option v-for="status in statuses" :key="status.id" :value="status.id">
              {{ status.description }}
            </option>
          </select>
        </div>
      </div>

      <div class="col-md-6">
        <div class="form-group">
          <label for="assignedFilter">Оператор:</label>
          <select
            id="assignedFilter"
            class="form-control"
            v-model="assignedFilter"
            @change="emitFilterChange"
          >
            <option value="">Все</option>
            <option v-for="operator in operators" :key="operator.id" :value="operator.id">
              {{ operator.surname }} {{ operator.name }} {{ operator.secname }}
            </option>
          </select>
        </div>
      </div>
    </div>
    <br />
    <div class="row">
      <div class="col-md-12">
        <button class="btn btn-secondary" @click="resetFilters">Сбросить фильтры</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, defineProps, defineEmits } from 'vue'

const ticketIdFilter = ref('')
const organizationFilter = ref('')
const systemFilter = ref('')
const statusFilter = ref('')
const assignedFilter = ref('')

const props = defineProps({
  organizations: Array,
  systems: Array,
  operators: Array,
  statuses: Array,
  ticket_id: Number
})

const emit = defineEmits(['filter-change'])

watch(
  [ticketIdFilter, organizationFilter, systemFilter, statusFilter, assignedFilter],
  () => {
    const filters = {
      ticket_id: ticketIdFilter.value || '',
      organization: organizationFilter.value || '',
      system: systemFilter.value || '',
      status: statusFilter.value || '',
      assigned: assignedFilter.value || ''
    }

    // Фильтрация пустых фильтров
    const filteredFilters = Object.fromEntries(
      Object.entries(filters).filter(([key, value]) => value !== '')
    )

    emit('filter-change', filteredFilters)
  },
  { deep: true }
)

const resetFilters = () => {
  ticketIdFilter.value = ''
  organizationFilter.value = ''
  systemFilter.value = ''
  statusFilter.value = ''
  assignedFilter.value = ''
  emit('filter-change', {})
}
</script>
