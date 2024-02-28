<script setup>
import { ref, onUnmounted, onMounted } from 'vue';
import { RouterLink, RouterView } from 'vue-router';
import { useRouter } from 'vue-router';
import apiService from '@/apiService';

const router = useRouter();
const isAuthenticated = ref(false);

let lastAuthState = false;

const checkAuthentication = () => {
 const currentAuthState = document.cookie.includes('user_access');
 if (currentAuthState !== lastAuthState) {
    isAuthenticated.value = currentAuthState;
    lastAuthState = currentAuthState;
    console.log('Authentication state changed:', currentAuthState);
 }
};

// Удалите setInterval, так как он не нужен для постоянной проверки

const logout = async () => {
 try {
    await apiService.logout();
    router.push('/login'); // Перенаправление на страницу входа после успешного выхода
    //checkAuthentication(); // Проверяем аутентификацию после успешного выхода
 } catch (error) {
    console.error('Ошибка при выходе из системы:', error);
 }
};

onMounted(() => {
 checkAuthentication(); // Проверяем аутентификацию при загрузке страницы
});

onUnmounted(() => {
 // Очистите таймер, если он был установлен с помощью setTimeout
 clearTimeout(checkAuthentication);
});
</script>

<template>
  <header>
    <div>
      <nav class="navbar navbar-expand-lg" style="background-color: #a1d1f3;">
        <div class="container collapse navbar-collapse">
          <ul class="navbar-nav">
            <li class="nav-item">
              <RouterLink v-if="isAuthenticated" class="nav-link" to="/tickets">Заявки</RouterLink>
            </li>
            <li class="nav-item">
              <RouterLink v-if="isAuthenticated" class="nav-link" to="/orgs">Организации</RouterLink>
            </li>
            <li class="nav-item">
              <RouterLink v-if="isAuthenticated" class="nav-link" to="/news">Новости</RouterLink>
            </li>
            <li class="nav-item">
              <button v-if="isAuthenticated" @click="logout" class="btn btn-secondary">Выйти</button>
            </li>
          </ul>
        </div>
      </nav>
    </div>
  </header>
  <RouterView />
</template>

<style scoped>

</style>
