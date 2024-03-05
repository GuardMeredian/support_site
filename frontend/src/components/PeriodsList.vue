<template>
    <div class="container">
       <h1 class="text-center">Единый областной банк данных</h1>
       <div class="accordion" id="periodsAccordion">
         <template v-for="(lpuGroup, lpucode) in groupedPeriods" :key="lpucode">
           <div class="accordion-item">
             <h2 class="accordion-header" :id="`heading-${lpucode}`">
               <button class="accordion-button collapsed alert alert-info" type="button" data-bs-toggle="collapse" :data-bs-target="`#collapse-${lpucode}`" aria-expanded="false" :aria-controls="`collapse-${lpucode}`">
                 {{ lpucode }}
               </button>
             </h2>
             <div :id="`collapse-${lpucode}`" class="accordion-collapse collapse" :aria-labelledby="`heading-${lpucode}`" data-bs-parent="#periodsAccordion">
               <div class="accordion-body">
                 <table class="table">
                   <tbody>
                    <tr>
                       
                       <th scope="col">Тип помощи</th>
                       <th scope="col">Квартал</th>
                       <th scope="col">Период</th>
                       <th scope="col">Статус</th>
                       <th scope="col">Действия</th>
                    </tr>
                 <template v-for="(modeGroup, mode) in lpuGroup" :key="mode">
                    <tr>
                      <td :rowspan="modeGroup.length" class="col-md-3">{{ modeDescription(mode) }}</td>
                      <td>{{ modeGroup[0].NAME }}</td>
                      <td>{{ modeGroup[0].DATE_BEG }} - {{ modeGroup[0].DATE_END }}</td>
                      <td :class="statusClass(modeGroup[0].STATUS)">{{ statusDescription(modeGroup[0].STATUS) }}</td>
                      <td>{{ actionText(modeGroup[0].STATUS) }}</td>
                    </tr>
                    <template v-for="(period, index) in modeGroup.slice(1)" :key="`${period.LPUCODE}-${index}`">
                      <tr>
                        <td>{{ period.NAME }}</td>
                        <td>{{ period.DATE_BEG }} - {{ period.DATE_END }}</td>
                        <td :class="statusClass(period.STATUS)">{{ statusDescription(period.STATUS) }}</td>
                        <td>{{ actionText(period.STATUS) }}</td>
                      </tr>
                       </template>
                    </template>
                   </tbody>
                 </table>
               </div>
             </div>
           </div>
         </template>
       </div>
    </div>
   </template>
   
   <script setup>
   import { ref, onMounted, computed } from 'vue';
   import apiService from '@/apiService'; // Adjust the import path as necessary
   
   const periods = ref([]);
   const groupedPeriods = computed(() => {
    const grouped = {};
    periods.value.forEach(period => {
       if (!grouped[period.LPUCODE]) {
         grouped[period.LPUCODE] = {};
       }
       if (!grouped[period.LPUCODE][period.MODE]) {
         grouped[period.LPUCODE][period.MODE] = [];
       }
       grouped[period.LPUCODE][period.MODE].push(period);
    });
    return grouped;
   });
   
   const modeDescription = (mode) => {
    const descriptions = {
       1: 'Амбулаторно поликлиническая помощь',
       2: 'Стоматологическая помощь',
       3: 'Ортопедическая помощь',
       5: 'Стационарная помощь',
    };
    return descriptions[mode] || 'Unknown';
   };
   
   const statusDescription = (status) => {
    const descriptions = {
       1: 'не загружен',
       2: 'загружается',
       3: 'загружен',
       4: 'проверяется',
       5: 'подписан ЛПУ',
       6: 'подписан МИАЦ',
       7: 'идет подпись',
    };
    return descriptions[status] || 'Unknown';
   };
   
   const statusClass = (status) => {
    const classes = {
       1: 'text-danger',
       2: 'text-danger',
       3: 'text-danger',
       4: 'text-danger',
       5: 'text-warning',
       6: 'text-success',
       7: 'text-danger',
    };
    return classes[status] || 'text-danger';
   };
   
   const actionText = (status) => {
    const actions = {
       3: 'Посмотреть протокол',
       5: 'Посмотреть протокол',
       6: 'Посмотреть протокол',
       1: 'Запустить контроль',
    };
    return actions[status] || '';
   };
   
   const fetchPeriods = async () => {
    try {
       const response = await apiService.getPeriods();
       periods.value = response.data;
    } catch (error) {
       console.error('Error fetching periods:', error);
    }
   };
   
   onMounted(fetchPeriods);
   </script>
   
   <style scoped>
   /* Add any styles specific to this component here */
   </style>