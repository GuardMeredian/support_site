import { ref } from 'vue';

import apiService from '@/apiService';

export const isAuthenticated = ref(false);
export const user = ref({});


export const updateUser = (newUserData) => {
 user.value = newUserData;
};

export const logout = async (router) => {
 try {
    await apiService.logout();
    router.push('/login'); // Перенаправление на страницу входа после успешного выхода
    user.value = {};
    isAuthenticated.value = false;
 } catch (error) {
    console.error('Ошибка при выходе из системы:', error);
 }
};

export const checkAuthentication = async (router) => {
   try {
      const userData = await apiService.getUserData();
      if (userData && userData.data) {
        updateUser(userData.data);
      } else {
        router.push('/login');
      }
   } catch (error) {
      if (error.response && error.response.status === 401) {
        // Токен истек или недействителен, перенаправляем пользователя на страницу входа
        router.push('/login');
      } else {
        console.error('Ошибка при получении данных пользователя:', error);
      }
   }
  };

  export const login = async (router) => {
   try {
     const response = await apiService.login(credentials.value)
     // Проверяем статус ответа
     if (response.status === 200) {
       updateUser(response.data);
       // Перенаправляем пользователя на страницу тикетов
       router.push({ name: 'tickets' })
     } else {
       // Обработка ошибок, например, отображение сообщения об ошибке
     }
   } catch (error) {
     // Обработка ошибок, например, отображение сообщения об ошибке
   }
 }

/*export const checkAuthentication = () => {
 const currentAuthState = document.cookie.includes('user_access');
 if (currentAuthState !== isAuthenticated.value) {
    isAuthenticated.value = currentAuthState;
    console.log('Authentication state changed:', currentAuthState);
 }
};*/