<script setup>
import { ref, onMounted } from 'vue'
import { RouterLink, RouterView } from 'vue-router'
import { useRouter } from 'vue-router'
import apiService from '@/apiService'
import { isAuthenticated, checkAuthentication, user } from '@/utils/authHelper'

const router = useRouter()

const logout = async () => {
  try {
    await apiService.logout()
    router.push('/login')
    isAuthenticated.value = false; // Перенаправление на страницу входа после успешного выхода
    user.value = {}
  } catch (error) {
    console.error('Ошибка при выходе из системы:', error)
  }
}

onMounted(async () => {
  checkAuthentication()
  try {
    const userData = await apiService.getUserData()
    if (userData && userData.data) {
      user.value = userData.data
    }
  } catch (error) {
    if (error.response && error.response.status === 401) {
      // Токен истек или недействителен, перенаправляем пользователя на страницу входа
      router.push('/login')
    } else {
      console.error('Ошибка при получении данных пользователя:', error)
    }
  }
})

const goToOrgDetail = () => {
  if (user.value.User && user.value.User.organization && user.value.User.organization.id) {
    router.push({ name: 'OrgDetail', params: { orgid: user.value.User.organization.id } })
  } else {
    console.error('Не удалось получить идентификатор организации пользователя')
  }
}
</script>

<template>
  <header>
    <div>
      <nav class="navbar navbar-expand-lg">
        <div class="container collapse navbar-collapse">
          <ul class="navbar-nav">
            <li class="nav-item" style="margin-right: 10px">
              <RouterLink v-if="isAuthenticated" class="btn btn-outline-success" to="/tickets"
                >Заявки</RouterLink
              >
            </li>
            <li class="nav-item" style="margin-right: 10px;">
    <RouterLink v-if="isAuthenticated && user.User.role.id !==2" class="btn btn-outline-success" to="/orgs">Организации</RouterLink>
    <button v-else-if="isAuthenticated  && user.User.role.id ==2" class="btn btn-outline-success" @click="goToOrgDetail">Организация</button>
</li>
            <li class="nav-item" style="margin-right: 10px">
              <RouterLink v-if="isAuthenticated" class="btn btn-outline-success" to="/news"
                >Новости</RouterLink
              >
            </li>
          </ul>
          <ul class="navbar-nav ms-auto">
            <!-- Добавьте ms-auto к ul, чтобы выровнять элементы по правому краю в Bootstrap 5 -->
            <li class="nav-item">
              <label class="nav-link" v-if="isAuthenticated && user && user.User"
                >Здравствуйте, <i>{{ user.User.surname }} {{ user.User.name.substring(0, 1) }}.{{user.User.secname.substring(0, 1)}}({{ user.User.role.description }})</i></label>
            </li>
            <li class="nav-item">
              <button v-if="isAuthenticated" @click="logout" class="btn btn-outline-secondary">
                Выйти
              </button>
            </li>
          </ul>
        </div>
      </nav>
    </div>
  </header>
  <RouterView />
</template>

<style scoped></style>
