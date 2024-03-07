<template>
  <div class="container">
     <h2>Детальная информация об организации</h2>
     <hr />
     <div v-if="organization">
       <h3>{{ organization.NAME }}</h3>
       <h3>Код организации: {{ organization.LPUCODE }}</h3>
       <h4>Контактная информация:</h4>
       <ul>
         <li>Телефон: {{ organization.PHONE }}</li>
         <li>Факс: {{ organization.FAX }}</li>
         <li>E-mail: {{ organization.E_MAIL3 }}</li>
         <li>Сайт: <a :href="organization.WWW" target="_blank">{{ organization.WWW }}</a></li>
       </ul>
       <h4>Список руководителей:</h4>
       <table class="table">
         <thead>
           <tr>
             <th>ФИО</th>
             <th>Должность</th>
             <th>Телефон</th>
           </tr>
         </thead>
         <tbody>
           <tr>
             <td>{{ organization.FACE }}</td>
             <td>Главный врач</td>
             <td>{{ organization.PHONE }}</td>
           </tr>
           <tr>
             <td>{{ organization.FACE1 }}</td>
             <td>Заместитель главного врача</td>
             <td>{{ organization.PHONE1 }}</td>
           </tr>
           <tr>
             <td>{{ organization.FACE3 }}</td>
             <td>Начальник отдела АСУ</td>
             <td>{{ organization.PHONE3 }}</td>
           </tr>
         </tbody>
       </table>
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
const organizationId = ref(null)
const organization = ref(null)

onMounted(async () => {
  organizationId.value = parseInt(route.params.orgid)
  try {
    const response = await apiService.getOrgDetail(organizationId.value) // Предполагается, что у вас есть метод getOrganizationDetail в вашем сервисе API
    organization.value = response.data
  } catch (error) {
    console.error('Ошибка при загрузке деталей организации:', error)
  }
})
</script>

<style scoped>
/* Добавьте здесь стили для таблицы, если они вам нужны */
</style>
