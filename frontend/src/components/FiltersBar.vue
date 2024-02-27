<!-- FiltersBar.vue -->
<template>
    <div class="filters">
      <label for="organizationFilter">Код организации:</label>
      <input type="text" id="organizationFilter" v-model="organizationFilter" @input="emitFilterChange" />
  
      <label for="systemFilter">Система:</label>
      <select id="systemFilter" v-model="systemFilter" @change="emitFilterChange">
        <option value="">Все</option>
        <option v-for="system in systems" :key="system.id" :value="system.id">
          {{ system.description }}
        </option>
      </select>
  
      <label for="statusFilter">Статус:</label>
      <select id="statusFilter" v-model="statusFilter" @change="emitFilterChange">
        <option value="">Все</option>
        <option v-for="status in statuses" :key="status.id" :value="status.id">
          {{ status.description }}
        </option>
      </select>
  
      <label for="operatorFilter">Оператор:</label>
      <select id="operatorFilter" v-model="operatorFilter" @change="emitFilterChange">
        <option value="">Все</option>
        <option v-for="operator in operators" :key="operator.id" :value="operator.id">
          {{ operator.surname }} {{ operator.name }} {{ operator.secname }}
        </option>
      </select>
    </div>
  </template>
  
  <script setup>
  import { ref, defineProps, defineEmits  } from 'vue'
  
  const organizationFilter = ref('')
  const systemFilter = ref('')
  const statusFilter = ref('')
  const operatorFilter = ref('')
  

  const props = defineProps({
  systems: Array,
  operators: Array,
  statuses: Array
})
const emit = defineEmits(['filter-change'])

const emitFilterChange = () => {
  // Создаем объект фильтров, исключая пустые значения
  const filters = {
    organization: organizationFilter.value || undefined,
    system: systemFilter.value || undefined,
    status: statusFilter.value || undefined,
    operator: operatorFilter.value || undefined
  };

  // Удаляем пустые значения из объекта фильтров
  Object.keys(filters).forEach(key => filters[key] === '' && delete filters[key]);

  emit('filter-change', filters)
}
  
  </script>