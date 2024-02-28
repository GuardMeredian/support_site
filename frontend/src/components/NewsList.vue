<template>
    <div class="container">
       <h2>Список новостей</h2>
       <table class="table table-hover">
         <thead>
           <tr>
             <th>Тема</th>
             <th>Дата публикации</th>
             <!-- Добавьте здесь другие заголовки столбцов, если они вам нужны -->
           </tr>
         </thead>
         <tbody>
        <tr v-for="newsItem in sortedNewsList" :key="newsItem.id">
          <td class="col-md-8">
            <strong>{{ newsItem.title }}</strong>
            <br>
            <div @click="toggleExpand(newsItem)">
              <span v-if="!newsItem.isExpanded">{{ newsItem.content.substring(0, 200) }} <br><i style="color: rgb(23, 163, 4);">(Читать далее)</i></span>
              <span v-else v-html="newsItem.content"></span>
            </div>
          </td>
          <td>{{ newsItem.created_at.split('T')[0] }}</td>
          <td>

          </td> <!-- Выводим первые 100 символов содержимого -->
          <!-- Добавьте здесь ячейки для других данных новости -->
        </tr>
      </tbody>
       </table>
    </div>
   </template>
   
   <script setup>
   import { ref, onMounted, computed } from 'vue';
   import apiService from '@/apiService'; // Путь к вашему сервису API
   
   const newsList = ref([]);
   
   onMounted(async () => {
    try {
       const response = await apiService.getNews(); // Предполагается, что у вас есть метод getNews в вашем сервисе API
       newsList.value = response.data.map(news => ({
         ...news,
         isExpanded: false // Добавляем свойство isExpanded для каждой новости
       }));
    } catch (error) {
       console.error('Ошибка при загрузке новостей:', error);
    }
   });
   
   // Сортировка новостей по дате публикации в порядке убывания
   const sortedNewsList = computed(() => {
    return newsList.value.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
   });

   const toggleExpand = (newsItem) => {
    newsItem.isExpanded = !newsItem.isExpanded; // Переключаем состояние раскрытия для конкретной новости
   };
   </script>
   
   <style scoped>
   /* Добавьте здесь стили для таблицы, если они вам нужны */
   </style>