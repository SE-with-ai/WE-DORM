<script setup >
import Holding from './components/Holding.vue'
import Borrowed from './components/Borrowed.vue'
import Virtue from './components/Virtue.vue'

</script>

<template> <!--TODO:root page,with sidebar and page header only-->
  <el-page-header :icon="ArrowLeft">
    <template #content>
      <span class="text-large font-600 mr-3"> 无用物品系统 </span>
    </template>
  </el-page-header>

  <Holding/>

  <Borrowed/>
  <Virtue/>

</template>

<style scoped>


</style>
