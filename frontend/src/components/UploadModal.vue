<template>
    <div class="modal fade" id="uploadModal" tabindex="-1" aria-labelledby="uploadModalLabel" aria-hidden="true">
       <div class="modal-dialog">
         <div class="modal-content">
           <div class="modal-header">
             <h5 class="modal-title" id="uploadModalLabel">Загрузка файла</h5>
             <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
           </div>
           <div class="modal-body">
             <form @submit.prevent="uploadFile">
               <div class="mb-3">
                 <label for="fileUpload" class="form-label">Выберите файл</label>
                 <input type="file" class="form-control" id="fileUpload" @change="handleFileChange">
               </div>
               <button type="submit" class="btn btn-primary">Загрузить</button>
             </form>
           </div>
         </div>
       </div>
    </div>
   </template>
   
   <script setup>
   import { ref, defineEmits, onMounted } from 'vue';
   import { useRoute } from 'vue-router';
   import apiService from '@/apiService';
   import { Modal } from 'bootstrap';
   
   const route = useRoute();
   const fileToUpload = ref(null);
   const emit = defineEmits(['refresh-ticket-data']); // Определение пользовательского события
   const bsModal = ref(null); // Создаем реактивную переменную для хранения экземпляра Modal
   
   onMounted(() => {
    // Инициализация модального окна после загрузки компонента
    const modalElement = document.getElementById('uploadModal');
    bsModal.value = new Modal(modalElement, {});
    modalElement.addEventListener('hidden.bs.modal', () => {
       const backdrop = document.querySelector('.modal-backdrop');
       if (backdrop) {
         backdrop.remove();
       }
    });
   });
   
   const handleFileChange = (event) => {
    fileToUpload.value = event.target.files[0];
   };
   
   const uploadFile = async () => {
    if (!fileToUpload.value) {
       alert('Пожалуйста, выберите файл для загрузки');
       return;
    }
   
    const formData = new FormData();
    formData.append('file', fileToUpload.value);
   
    try {
       const response = await apiService.uploadFile(route.params.ticketId, formData);
       // Закрываем модальное окно
       if (bsModal.value) {
         bsModal.value.hide(true);
       }
       // Вызываем событие для обновления данных о заявке
       emit('refresh-ticket-data');
    } catch (error) {
       console.error('Ошибка при загрузке файла:', error);
       alert('Ошибка при загрузке файла');
    }
   };
   
   // В компоненте с <script setup>, emit доступен напрямую
   </script>