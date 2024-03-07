<template>
    <div class="container">
       <div class=" btn-group mb-3">
         <button class="btn btn-outline-primary" @click="downloadProtocolApp">Скачать протокол</button>
         <button class="btn btn-outline-primary">Форма 39</button>
         <button class="btn btn-outline-primary">Форма 12</button>
       </div>

       <div v-if="loading" class="d-flex justify-content-center">
         <div class="spinner-border text-primary" role="status">
           <span class="visually-hidden">Загрузка...</span>
         </div>
       </div>
   
       <div v-else>
        <div v-if="!loadingFirst">
      <table class="table table-bordered" style="border-color: black;">
        <thead style="font-size: 14px">
          <tr>
            <th rowspan="3" style="background-color:lightgray;" class="text-center">Код ЛПУ</th>
            <th rowspan="3" style="background-color:lightgray;" class="text-center">Карты ЗС</th>
            <th rowspan="3" style="background-color:lightgray;" class="text-center">Диагнозы</th>
            <th colspan="5" style="background-color:lightgray;" class="text-center">Услуги / Ambserv</th>
            <th rowspan="3" style="background-color:lightgray;" class="text-center">
              Б/Лист <br />
              Ambsheet
            </th>
            <th colspan="2" style="background-color:lightgray;" class="text-center">Дата оказания услуг</th>
          </tr>
          <tr>
            <th rowspan="2" style="background-color:lightgray;" class="text-center">Тип</th>
            <th rowspan="2" style="background-color:lightgray;" class="text-center">
              Кол-во <br />
              Всего
            </th>
            <th colspan="2" style="background-color:lightgray;" class="text-center">из них посещ.</th>
            <th rowspan="2" style="background-color:lightgray;" class="text-center">сумма затрат всего</th>
            <th rowspan="2" style="background-color:lightgray;" class="text-center">С</th>
            <th rowspan="2" style="background-color:lightgray;" class="text-center">По</th>
          </tr>
          <tr>
            <th class="text-center" style="background-color:lightgray;">врачеб</th>
            <th class="text-center" style="background-color:lightgray;">сред</th>
          </tr>
        </thead>
        <tbody style="font-size: 14px">
          <tr v-for="item in filteredDataFirst" :key="item.type">
            <td class="text-center">{{ chief}}</td>
            <td class="text-center">-</td>
            <td class="text-center">-</td>
            <td class="text-center">{{ item.type }}</td>
            <td class="text-center">{{ item.cnt }}</td>
            <td class="text-center">{{ item.v1 }}</td>
            <td class="text-center">{{ item.v2 }}</td>
            <td class="text-center">{{ item.sum }}</td>
            <td class="text-center">-</td>
            <td class="text-center">{{ item.date1 }}</td>
            <td class="text-center">{{ item.date2 }}</td>
          </tr>
        </tbody>
        <tr style="background-color:lightgray;">
            <th class="total text-center">Итого</th>
            <th class="total text-center">{{ totalCards }}</th>
            <th class="total text-center">{{totalDiagnoses}}</th>
            <th class="total text-center">-</th>
            <th class="total text-center">{{ itemWithTypeMinusOne.cnt }}</th>
          <th class="total text-center">{{ itemWithTypeMinusOne.v1 }}</th>
          <th class="total text-center">{{ itemWithTypeMinusOne.v2 }}</th>
          <th class="total text-center">{{ itemWithTypeMinusOne.sum }}</th>
          <th class="total text-center">0</th>
          <th class="total text-center">-</th>
          <th class="total text-center">-</th>
        </tr>
      </table>
    </div>
        <hr>
         <div class="info mt-3">Информация о посещениях:</div>
         <hr>
         <div>
           <table class="table table-bordered" style="border-color: black;">
             <thead style="font-size: 14px">
               <tr>
                 <th class="text-center" style="background-color:lightgray;">С</th>
                 <th class="text-center" style="background-color:lightgray;">По</th>
                 <th class="text-center" style="background-color:lightgray;">Всего посещений</th>
                 <th class="text-center" style="background-color:lightgray;">Из них в полик MESTO=1</th>
                 <th class="text-center" style="background-color:lightgray;">Из них на дому MESTO=2 или MESTO=3</th>
                 <th class="text-center" style="background-color:lightgray;">OMC PAYTYPE=1</th>
                 <th class="text-center" style="background-color:lightgray;">Бюджет PAYTYPE=2</th>
                 <th class="text-center" style="background-color:lightgray;">Другое PAYTYPE>2</th>
                 <th class="text-center" style="background-color:lightgray;">Всего случаев в посещ (цель посещ 1-5)</th>
                 <th class="text-center" style="background-color:lightgray;">Количество посещ на 1 случ.</th>
                 <th class="text-center" style="background-color:lightgray;">Посещ с целью 26-др.</th>
               </tr>
             </thead>
             <tbody style="font-size: 14px">
               <tr v-for="item in visitData" :key="item.datebeg">
                 <td class="text-center">{{ item.datebeg }}</td>
                 <td class="text-center">{{ item.DATEEND }}</td>
                 <td class="text-center">{{ item.POSESCH_VSEGO }}</td>
                 <td class="text-center">{{ item.POSESCH_POLIC }}</td>
                 <td class="text-center">{{ item.POSESCH_POLIC_SELO }}</td>
                 <td class="text-center">{{ item.OMS }}</td>
                 <td class="text-center">{{ item.BUDG }}</td>
                 <td class="text-center">{{ item.DRUGOE }}</td>
                 <td class="text-center">{{ item.SLUCH_S_POSESCH }}</td>
                 <td class="text-center">{{ item.POSESCH_NA_SLUCH }}</td>
                 <td class="text-center">{{ item.POSESCH_CEL_6 }}</td>
               </tr>
             </tbody>
           </table>
         </div>
       </div>
       <hr>
       <div class="info mt-3">Форматно-логический контроль:</div>
       <hr>
       <div>
        
      <table class="table table-bordered" style="border-color: black;">
        <thead>
          <tr>
            <th  class="text-center" style="background-color:lightgray;">№</th>
            <th  class="text-center" style="background-color:lightgray;">Код</th>
            <th  class="text-center" style="background-color:lightgray;">Наименование</th>
            <th  class="text-center" style="background-color:lightgray;">Количество</th>
            <th  class="text-center" style="background-color:lightgray;">Уровень важности</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
          </tr>
        </tbody>
      </table>
       </div>
    </div>
   </template>
   
   <script setup>
import { ref, onMounted, computed } from 'vue';
import { useRoute } from 'vue-router';
import apiService from '@/apiService';

const route = useRoute();
const visitData = ref([]);
const loading = ref(true);
const dataFirst = ref([]); // Добавьте новую переменную для хранения данных новой таблицы
const loadingFirst = ref(true); // Добавьте новую переменную для отслеживания загрузки данных новой таблицы

const chief = ref(null);
const year = ref(route.params.Year);
const yearqr = ref(route.params.Year_qr);

onMounted(async () => {
 chief.value = route.params.chief;
 // Получаем chiefId из параметров маршрута
 try {
    const response = await apiService.getProtocol39AmbResult(chief.value, year.value, yearqr.value);
    console.log('API response:', response); // Добавьте эту строку для отладки
    visitData.value = response.data.Visit; // Обновленные данные о посещениях
    dataFirst.value = response.data.data; // Данные для новой таблицы
    console.log('visitData:', visitData.value); // Добавьте эту строку для отладки
    console.log('dataFirst:', dataFirst.value); // Добавьте эту строку для отладки
 } catch (error) {
    console.error('Error fetching data:', error);
 } finally {
    loading.value = false;
    loadingFirst.value = false; // Установите значение loadingFirst в false после загрузки данных
 }
});

const filteredDataFirst = computed(() => {
 return dataFirst.value.filter(item => item.type !== -4 && item.type !== -3 && item.type !== -2 && item.type !== -1);
});

const totalCards = computed(() => {
 return dataFirst.value.find(item => item.type === -4)?.cnt || 0;
});

const totalDiagnoses = computed(() => {
 return dataFirst.value.find(item => item.type === -3)?.cnt || 0;
});


const itemWithTypeMinusOne = computed(() => {
 return dataFirst.value.find(item => item.type === -1) || {};
});

const downloadProtocolApp = () => {
 // Логика скачивания протокола
};
</script>

<style scoped>
/* Стили, если необходимо */
</style>