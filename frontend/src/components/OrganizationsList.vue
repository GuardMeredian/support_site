<template>
    <div class="container">
       <h2>Список организаций</h2>
       <table class="table table-hover">
         <thead>
           <tr>
             <th>Код МО</th>
             <th>Наименование</th>
             <!-- Добавьте здесь другие заголовки столбцов, если они вам нужны -->
           </tr>
         </thead>
         <tbody>
           <tr v-for="organization in sortedOrganizations" :key="organization.id">
                <td>{{ organization.lpucode }}</td>
                <td>
                    <RouterLink class="no-highlight" :to="{ name: 'OrgDetail', params: { orgid: organization.id } }">
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
   import { ref, onMounted, computed } from 'vue';
   import { RouterLink } from 'vue-router';
   import apiService from '@/apiService'; // Путь к вашему сервису API
   
   const organizations = ref([]);
   
   onMounted(async () => {
    try {
       const response = await apiService.getOrgs(); // Предполагается, что у вас есть метод getOrgs в вашем сервисе API
       organizations.value = response.data;
    } catch (error) {
       console.error('Ошибка при загрузке организаций:', error);
    }
   });
   
   // Сортировка организаций по возрастанию поля Lpucode
   const sortedOrganizations = computed(() => {
 return [...organizations.value].sort((a, b) => a.lpucode - b.lpucode);
   });
   </script>
   
   <style scoped>
   .no-highlight {
    text-decoration: none;
    color: inherit;
   }
   </style>