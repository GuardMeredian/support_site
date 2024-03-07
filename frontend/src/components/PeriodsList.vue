<template>
  <div class="container">
      <h1 class="text-center">Единый областной банк данных</h1>
      <div v-for="(lpuGroup, lpucode) in groupedPeriods" :key="lpucode">
        <button class="btn btn-outline-primary mb-3 text-start" style="width: 100%;" type="button" @click="toggleCollapse(lpucode)">
          {{ lpucode }} - {{ orgNames[lpucode] || 'Название не найдено' }}
        </button>
        <div v-show="isCollapsed(lpucode)" class="card card-body">
          <table class="table table-bordered" style="border-color: black;">
            <tbody>
              <tr>
                <th class="text-center">Тип помощи</th>
                <th class="text-center">Квартал</th>
                <th class="text-center">Период</th>
                <th class="text-center">Статус</th>
                <th class="text-center">Действия</th>
              </tr>
              <template v-for="(modeGroup, mode) in lpuGroup" :key="mode">
                <tr>
                  <td :rowspan="modeGroup.length" class="col-md-2 text-center">{{ modeDescription(mode) }}</td>
                  <td class="text-center">{{ modeGroup[0].NAME }}</td>
                  <td class="text-center">{{ modeGroup[0].DATE_BEG }} - {{ modeGroup[0].DATE_END }}</td>
                  <td :class="statusClass(modeGroup[0].STATUS)" class="text-center">{{ statusDescription(modeGroup[0].STATUS) }}</td>
                  <td >
                    <router-link v-if="[3, 5, 6].includes(modeGroup[0].STATUS)" :to="{ name: 'ambProtocolDetail', params: { chief: modeGroup[0].LPUCODE, Year: modeGroup[0].YEAR, Year_qr: modeGroup[0].NUMBER_PER } }" class="btn btn-success" style="width: 50%; height: 30px; font-size: 12px;">
                      Протокол
                    </router-link>
                    <button v-else-if="modeGroup[0].STATUS === 1" class="btn btn-primary" @click="startControl(modeGroup[0].LPUCODE)" style="width: 50%; height: 30px; font-size: 12px;">
                     Контроль
                   </button>
                  </td>
                </tr>
                <template v-for="(period, index) in modeGroup.slice(1)" :key="`${period.LPUCODE}-${index}`">
                  <tr>
                    <td class="text-center">{{ period.NAME }}</td>
                    <td class="text-center">{{ period.DATE_BEG }} - {{ period.DATE_END }}</td>
                    <td class="text-center" :class="statusClass(period.STATUS)">{{ statusDescription(period.STATUS) }}</td>
                    <td>
                      <router-link v-if="[3, 5, 6].includes(period.STATUS)" :to="{ name: 'ambProtocolDetail', params: { chief: period.LPUCODE, Year: period.YEAR, Year_qr: period.NUMBER_PER } }" class="btn btn-success" style="width: 50%; height: 30px; font-size: 12px;">
                        Протокол
                      </router-link>
                      <button v-else-if="modeGroup[0].STATUS === 1" class="btn btn-primary" style="width: 50%; height: 30px; font-size: 12px;" @click="startControl(modeGroup[0].LPUCODE) ">
                     Контроль
                   </button>
                    </td>
                  </tr>
                </template>
              </template>
            </tbody>
          </table>
        </div>
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
     1: 'Амбулаторно-поликлиническая помощь',
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

 const orgNames = ref({});

 const fetchOrgNames = async (roleId) => {
 try {
    const response = await apiService.getOrgs(roleId);
    response.data.forEach(org => {
      orgNames.value[org.LPUCODE] = org.NAME; // Предполагается, что у вас есть LPUCODE и NAME в ответе
    });
 } catch (error) {
    console.error('Error fetching org names:', error);
 }
};

onMounted(() => {
 fetchOrgNames(1); // Используйте нужный roleId
});
 
 onMounted(fetchPeriods);

 const collapsedItems = ref([]);

const toggleCollapse = (lpucode) => {
 const index = collapsedItems.value.indexOf(lpucode);
 if (index > -1) {
    collapsedItems.value.splice(index, 1);
 } else {
    collapsedItems.value.push(lpucode);
 }
};

const isCollapsed = (lpucode) => {
 return collapsedItems.value.includes(lpucode);
};
 </script>
 
 <style scoped>
 /* Add any styles specific to this component here */
 </style>