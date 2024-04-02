<template>
  <div class="container">
    <hr />
    <h2 class="text-center">Список организаций</h2>
    <input
      type="text"
      class="form-control"
      v-model="searchQuery"
      placeholder="Поиск по коду организации и названию"
    />
    <hr />
    <table class="table table-hover">
      <thead>
        <tr>
          <th>Код МО</th>
          <th>Наименование</th>
          <!-- Добавьте здесь другие заголовки столбцов, если они вам нужны -->
        </tr>
      </thead>
      <tbody>
        <tr v-for="organization in filteredOrganizations" :key="organization.id">
          <td>{{ organization.lpucode }}</td>
          <td>
            <RouterLink
              class="no-highlight"
              :to="{ name: 'OrgDetail', params: { lpucode: organization.lpucode } }"
            >
              {{ organization.name }}
            </RouterLink>
          </td>
          <!-- Добавьте здесь ячейки для других данных организации -->
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { RouterLink } from 'vue-router'
import apiService from '@/apiService' // Путь к вашему сервису API

const organizations = ref([])
const searchQuery = ref('')

onMounted(async () => {
  try {
    const response = await apiService.getOrgs() // Предполагается, что у вас есть метод getOrgs в вашем сервисе API
    organizations.value = response.data
    console.log(organizations.value)
  } catch (error) {
    console.error('Ошибка при загрузке организаций:', error)
  }
})

// Сортировка организаций по возрастанию поля Lpucode
const sortedOrganizations = computed(() => {
  return [...organizations.value].sort((a, b) => a.lpucode - b.lpucode)
})

// Фильтрация организаций по коду или имени, не учитывая регистр и отбрасывая кавычки при фильтрации по имени
const filteredOrganizations = computed(() => {
  if (!searchQuery.value) return organizations.value
  return organizations.value.filter((org) => {
    // Преобразование LPUCODE в строку и приведение к нижнему регистру для корректной работы метода includes
    const lpucodeStr = org.lpucode.toString().toLowerCase()
    // Проверка, содержит ли LPUCODE поисковой запрос, приведенный к нижнему регистру
    const lpucodeMatches = lpucodeStr.includes(searchQuery.value.toLowerCase())
    // Удаление кавычек из NAME и приведение к нижнему регистру для проверки на соответствие поисковому запросу
    const nameWithoutQuotes = org.name.replace(/"/g, '').toLowerCase()
    const nameMatches = nameWithoutQuotes.includes(searchQuery.value.toLowerCase())
    // Включение организации в результаты, если LPUCODE или NAME (без кавычек) соответствует поисковому запросу
    return lpucodeMatches || nameMatches
  })
})
</script>

<style scoped>
.no-highlight {
  text-decoration: none;
  color: inherit;
}
</style>
