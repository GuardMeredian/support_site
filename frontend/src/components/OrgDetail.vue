<template>
    <div class="container">
       <h2>Детальная информация об организации</h2>
       <hr>
       <div v-if="organization">
         <h3>{{ organization.name }}</h3>
         <h3>Код организации: {{ organization.lpucode }}</h3>
         <h4>Список пользователей:</h4>
         <table class="table">
           <thead>
             <tr>
               <th>ФИО</th>
               <th>Должность</th>
               <th>Телефон</th>
             </tr>
           </thead>
           <tbody>
             <tr v-for="user in organization.users" :key="user.id">
               <td>{{ user.surname }} {{ user.name }} {{ user.secname }}</td>
               <td>{{ user.post }}</td>
               <td>{{ user.contact_tel }}</td>
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
   import { ref, onMounted } from 'vue';
   import { useRoute } from 'vue-router';
   import apiService from '@/apiService'; // Путь к вашему сервису API
   
   const route = useRoute();
   const organizationId = ref(null);
   const organization = ref(null);
   
   onMounted(async () => {
    organizationId.value = parseInt(route.params.orgid);
    try {
       const response = await apiService.getOrgDetail(organizationId.value); // Предполагается, что у вас есть метод getOrganizationDetail в вашем сервисе API
       organization.value = response.data;
    } catch (error) {
       console.error('Ошибка при загрузке деталей организации:', error);
    }
   });
   </script>
   
   <style scoped>
   /* Добавьте здесь стили для таблицы, если они вам нужны */
   </style>