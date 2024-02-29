<script setup>
import { ref, onMounted} from 'vue';
import { RouterLink, RouterView } from 'vue-router';
import { useRouter } from 'vue-router';
import apiService from '@/apiService';
import { isAuthenticated, checkAuthentication, logout, user } from '@/utils/authHelper'; 

const router = useRouter();



onMounted(async () => {
await checkAuthentication(router);

});

const handleLogout = async () => {
 await logout(router);
};

const goToOrgDetail = () => {
 if (user.value.User && user.value.User.organization && user.value.User.organization.id) {
    router.push({ name: 'OrgDetail', params: { orgid: user.value.User.organization.id } });
 } else {
    console.error('Не удалось получить идентификатор организации пользователя');
 }
};



</script>

<template>
  <header>
    <div>
      <nav class="navbar navbar-expand-lg" >
        <div class="container collapse navbar-collapse">
          <ul class="navbar-nav">
            <li class="nav-item" style="margin-right: 10px;">
              <RouterLink v-if="isAuthenticated" class="btn btn-outline-success" to="/tickets">Заявки</RouterLink>
            </li>
            <li class="nav-item" style="margin-right: 10px;">
        <RouterLink v-if="isAuthenticated && user.User && user.User.role && user.User.role.id !== 2" class="btn btn-outline-success" to="/orgs">Организации</RouterLink>
        <button v-else-if="isAuthenticated && user.User && user.User.role && user.User.role.id === 2" class="btn btn-outline-success" @click="goToOrgDetail">Организация</button>
      </li>
            <li class="nav-item" style="margin-right: 10px;">
              <RouterLink v-if="isAuthenticated" class="btn btn-outline-success" to="/news">Новости</RouterLink>
            </li>
          </ul>
          <ul class="navbar-nav ms-auto"> <!-- Добавьте ms-auto к ul, чтобы выровнять элементы по правому краю в Bootstrap 5 -->
            <li class="nav-item">
              <label class="nav-link" v-if="isAuthenticated && user && user.User">Здравствуйте, {{ user.User.surname }} {{ user.User.name.substring(0,1) }}.{{ user.User.secname.substring(0,1) }}<i>({{ user.User.role.description }})</i></label>
            </li>
            <li class="nav-item">
              <button v-if="isAuthenticated" @click="handleLogout" class="btn btn-outline-secondary">Выйти</button>
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
