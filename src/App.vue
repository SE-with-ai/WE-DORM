
<template class="common-layout"> 
<!-- <widget-container-modal /> -->
    <el-container>
      <el-header>
        <h1>WEDORM</h1>
        <!--TODO:use vue-router to go open login page-->
        <el-dropdown-menu  trigger="click">
          <span class="el-dropdown-link"><el-icon class="el-icon--right"><arrow-down /></el-icon>
          </span>
          <template #dropdown>
            <el-dropdown-item @click="deleteUserConfirm=!deleteUserConfirm">删除账号</el-dropdown-item>
          <el-dropdown-item @click="trick=!trick" :hidden="!deleteUserConfirm">确定？</el-dropdown-item>
          <el-dropdown-item :hidden="!trick">不让你删</el-dropdown-item>
          </template>
        </el-dropdown-menu>
      </el-header>
      <el-main>
        <router-view/>
    </el-main>
  </el-container>

</template>
<script setup >
import Holding from './components/Holding.vue'
import Borrowed from './components/Borrowed.vue'
import Virtue from './components/Virtue.vue'
import {ref} from 'vue'
import {container as WidgetContainerModal} from 'jenesius-vue-modal'

  const deleteUserConfirm = ref(false)
  const trick = ref(false)
  const loggedin = ref(false)
</script>
<style scoped>


</style>
