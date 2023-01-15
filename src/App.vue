
<template class="common-layout"> 
<!-- <widget-container-modal /> -->
    <el-container>
      <el-header><h1>WEDORM</h1>
        <el-dropdown-menu>
          <el-dropdown-item @click="deleteUserConfirm=!deleteUserConfirm">删除账号</el-dropdown-item>
          <el-dropdown-item @click="trick=!trick" :hidden="!deleteUserConfirm">确定？</el-dropdown-item>
          <el-dropdown-item :hidden="!trick">不让你删</el-dropdown-item>
        </el-dropdown-menu>
      </el-header>
      <el-main>
  <Holding/>
  <Borrowed/>
  <Virtue/>
    </el-main>
  </el-container>

</template>
<script setup >
import Holding from './components/Holding.vue'
import Borrowed from './components/Borrowed.vue'
import Virtue from './components/Virtue.vue'
import {ref} from 'vue'
// import {container as WidgetContainerModal} from 'jenesius-vue-modal'

  const deleteUserConfirm = ref(false)
  const trick = ref(false)
</script>
<style scoped>


</style>
