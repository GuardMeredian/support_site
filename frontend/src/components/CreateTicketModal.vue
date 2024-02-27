<template>
    <div class="modal fade" id="createTicketModal" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1" aria-labelledby="createTicketModalLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="createTicketModalLabel">Создать заявку</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Закрыть"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="createTicket">
              <div class="mb-3">
                <label for="ticketTitle" class="form-label">Тема</label>
                <input type="text" class="form-control" id="ticketTitle" v-model="newTicket.title" required>
              </div>
              <div class="mb-3">
                <label for="ticketDescription" class="form-label">Описание</label>
                <textarea class="form-control" id="ticketDescription" v-model="newTicket.description" required></textarea>
              </div>
              <div class="mb-3">
                <label for="ticketSystem" class="form-label">Система</label>
                <select class="form-select" id="ticketSystem" v-model="newTicket.system_id">
                    <option v-for="system in systems" :key="system.id" :value="system.id">{{ system.description }}</option>
                </select>
              </div>
              <button type="submit" class="btn btn-primary">Создать</button>
            </form>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted, watch } from 'vue'
  import { Modal } from 'bootstrap';
  import { useRouter } from 'vue-router'

  import apiService from '@/apiService'

  const router = useRouter()
   
  const newTicket = ref({
    title: '',
    description: '',
    status_id:   1, // Статус "Создана"
    system_id:   0, // ID системы, которую нужно установить
    priority:   1, // Приоритет тикета
    creator_id: null, // ID создателя, который нужно установить
    created_at: new Date().toISOString().split('T')[0], // Текущая дата
    organization_id: null // ID организации, который нужно установить
  })
   
  const systems = ref([])
  const bsModal = ref(null); // Создаем реактивную переменную для хранения экземпляра Modal
   
  onMounted(async () => {
    const userResponse = await apiService.getUserData()
    const userData = userResponse.data.User;
    newTicket.value.creator_id = userData.id; // Устанавливаем ID создателя
    newTicket.value.organization_id = userData.organization.id; // Устанавливаем ID организации
   
    const systemsResponse = await apiService.getSystems()
    systems.value = systemsResponse.data

    // Инициализация модального окна после загрузки компонента
    const modalElement = document.getElementById('createTicketModal');
    bsModal.value = new Modal(modalElement, {});
    modalElement.addEventListener('hidden.bs.modal', () => {
      const backdrop = document.querySelector('.modal-backdrop');
      if (backdrop) {
        backdrop.remove();
      }
    });
  });
   
  watch(() => newTicket.value.system_id, (newId) => {
    const selectedSystem = systems.value.find(system => system.id === newId);
    if (selectedSystem) {
      newTicket.value.system_id = newId; // Устанавливаем ID выбранной системы
    }
  });

  // Определяем функцию emit для отправки событий
  const emit = defineEmits(['ticketCreated'])
   
  const createTicket = async () => {
    try {
      // Убедитесь, что вы выбрали систему из списка систем
      if (!newTicket.value.system_id) {
        console.error('System not selected');
        return;
      }
   
      // Убедитесь, что все необходимые поля заполнены
      if (!newTicket.value.title || !newTicket.value.description || !newTicket.value.creator_id || !newTicket.value.organization_id) {
        console.error('All required fields must be filled');
        return;
      }
   
      // Отправляем запрос на создание тикета
      const response = await apiService.createTicket(newTicket.value)
      console.log('Response from server:', response);

      // Обработка успешного создания заявки
      // Закрытие модального окна
      if (bsModal.value) {
        bsModal.value.hide(true);
      }
      // Отправляем событие 'ticketCreated'
        emit('ticketCreated')
    } catch (error) {
      // Обработка ошибок
      console.error('Ошибка при создании тикета:', error);
    }
  }
</script>