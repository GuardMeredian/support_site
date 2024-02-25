<template>
  <div class="d-flex justify-content-center align-items-center vh-100">
    <div class="alert alert-info col-md-3" role="alert">
      <form @submit.prevent="login" class="form-group">
        <h1 class="h3 mb-3 fw-normal">Авторизация</h1>

        <div class="form-floating">
          <input v-model="credentials.login" type="text" class="form-control" id="floatingInput" placeholder="Логин" required />
          <label for="floatingInput">Ваш логин</label>
        </div>
        <hr>
        <div class="form-floating">
          <input v-model="credentials.password" type="password" class="form-control" id="floatingPassword" placeholder="Пароль" required />
          <label for="floatingPassword">Пароль</label>
        </div>
        <hr>
        <div class="d-flex justify-content-center mt-3">
          <button class="btn btn-primary py-2 col-md-5" type="submit">Войти</button>
        </div>
        <p class="mt-5 mb-3 text-body-secondary">© ГБУЗ СО МИАЦ 2024</p>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref} from 'vue'
import apiService from '../apiService'
import { useRouter } from 'vue-router'

const credentials = ref({
  login: '',
  password: ''
})

const router = useRouter()


const login = async () => {
  try {
    const response = await apiService.login(credentials.value)
    // Проверяем статус ответа
    if (response.status === 200) {
      // Перенаправляем пользователя на страницу тикетов
      router.push({ name: 'tickets' })
    } else {
      // Обработка ошибок, например, отображение сообщения об ошибке
    }
  } catch (error) {
    // Обработка ошибок, например, отображение сообщения об ошибке
  }
}


</script>
