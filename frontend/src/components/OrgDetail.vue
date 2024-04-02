<template>
  <div class="container">
     <h2>Детальная информация об организации</h2>
     <hr />
     <div v-if="organization">
       <h3>{{ organization.name }}</h3>
       <h3>Код организации: {{ organization.lpucode }}</h3>
       <div v-if="organization.users && organization.users.length > 0">
         <h4>Список пользователей:</h4>
         <table class="table table-bordered">
           <thead>
             <tr>
               <th class="text-center">Фамилия</th>
               <th class="text-center">Имя</th>
               <th class="text-center">Отчество</th>
               <th class="text-center">Должность</th>
               <th class="text-center">Телефон</th>
             </tr>
           </thead>
           <tbody>
             <tr v-for="user in organization.users" :key="user.name">
               <td>{{ user.surname }}</td>
               <td>{{ user.name }}</td>
               <td>{{ user.secname }}</td>
               <td>{{ user.post }}</td>
               <td>{{ user.contact_tel }}</td>
             </tr>
           </tbody>
         </table>
       </div>
       <div v-else>
         <p>Нет данных о пользователях.</p>
       </div>
     </div>
     <div v-else>
       <p>Загрузка данных об организации...</p>
     </div>
  </div>
 </template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import apiService from '@/apiService' // Путь к вашему сервису API

const route = useRoute()
const lpucode = ref(null)
const organization = ref(null)

onMounted(async () => {
  lpucode.value = parseInt(route.params.lpucode)
  try {
    const response = await apiService.getOrgDetail(lpucode.value) // Предполагается, что у вас есть метод getOrganizationDetail в вашем сервисе API
    organization.value = response.data
    console.log(organization.value)
  } catch (error) {
    console.error('Ошибка при загрузке деталей организации:', error)
  }
})
</script>

<style scoped>
/* Добавьте здесь стили для таблицы, если они вам нужны */
</style>
