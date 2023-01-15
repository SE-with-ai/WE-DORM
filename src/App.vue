<script setup >
import Holding from './components/Holding.vue'
import Borrowed from './components/Borrowed.vue'
import Virtue from './components/Virtue.vue'
// import {container as WidgetContainerModal} from 'jenesius-vue-modal'

</script>

<template class="common-layout"> 
<!-- <widget-container-modal /> -->
    <el-container>
      <el-header><h1>WEDORM</h1></el-header>
      <el-main>
  <Holding/>
  <Borrowed/>
  <Virtue/>
    </el-main>
  </el-container>

</template>

<style scoped>


</style>
