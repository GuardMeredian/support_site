<script setup>
import { ref, onUnmounted, onMounted} from 'vue'
import { RouterLink, RouterView } from 'vue-router'// Импортируйте глобальное состояние
import { useRouter } from 'vue-router'
import apiService from '@/apiService'

const router = useRouter()
const isAuthenticated = ref(false)

let lastAuthState = false

const checkAuthentication = () => {
  const currentAuthState = document.cookie.includes('user_access')
  if (currentAuthState !== lastAuthState) {
    isAuthenticated.value = currentAuthState
    lastAuthState = currentAuthState
    console.log('Authentication state changed:', currentAuthState)
  }
}


const intervalId = setInterval(checkAuthentication,  100)

// Глобальный обработчик событий для отслеживания изменений куки

const logout = async () => {
  try {
    await apiService.logout()
    router.push('/login') // Перенаправление на страницу входа после успешного выхода
  } catch (error) {
    console.error('Ошибка при выходе из системы:', error)
  }
}
onMounted(() => {
  checkAuthentication()
})


onUnmounted(() => {
  clearInterval(intervalId)
})
</script>

<template>
  <header>
    <div class="container">
      <nav class="navbar navbar-expand-lg navbar-light bg-light">
        <div class="collapse navbar-collapse">
          <ul class="navbar-nav">
            <li class="nav-item">
              <button v-if="isAuthenticated" @click="logout" class="btn btn-secondary">Выйти</button>
            </li>
            <li class="nav-item">
              <RouterLink v-if="isAuthenticated" class="nav-link" to="/tickets">Заявки</RouterLink>
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
