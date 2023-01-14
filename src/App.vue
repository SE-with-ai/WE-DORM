<script setup >
import Home from './components/Home.vue'
import Borrowed from './components/Borrowed.vue'


// TODO: fetch user id via login/register; store user id in sessionStorage

const currentPath = ref(window.location.hash)

window.addEventListener('hashchange', () => {
  currentPath.value = window.location.hash
})

const currentView = computed(() => {
  return routes[currentPath.value.slice(1) || '/'] || NotFound
})

</script>

<template> <!--TODO:root page,with sidebar and page header only-->
  <el-page-header :icon="ArrowLeft">
    <template #content>
      <span class="text-large font-600 mr-3"> 无用物品系统 </span>
    </template>
  </el-page-header>
  <Home/>

  <Borrowed/>
  

</template>

<style scoped>


</style>
