import { ref } from 'vue'

export const isAuthenticated = ref(false)
export const user = ref({}) // Инициализация объекта user

export const updateUser = (newUserData) => {
  user.value = newUserData // Обновление объекта user с новыми данными
}

export const checkAuthentication = () => {
  const currentAuthState = document.cookie.includes('user_access')
  if (currentAuthState !== isAuthenticated.value) {
    isAuthenticated.value = currentAuthState
    console.log('Authentication state changed:', currentAuthState)
  }
}
