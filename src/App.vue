<script setup lang="ts">
import HelloWorld from './components/HelloWorld.vue'

// TODO: fetch user id via login/register; store user id in sessionStorage
</script>

<template> <!--TODO:root page,with sidebar and page header only-->
<el-menu
default-active="2"
@select="routed"

>
<el-menu-item>
<router-link-to>
  
</router-link-to>
</el-menu-item>
</el-menu>
  <div>
    <a href="https://vitejs.dev" target="_blank">
      <img src="/vite.svg" class="logo" alt="Vite logo" />
    </a>
    <a href="https://vuejs.org/" target="_blank">
      <img src="./assets/vue.svg" class="logo vue" alt="Vue logo" />
    </a>
    
  </div>
  <HelloWorld msg="Vite + Vue" />
</template>

<style scoped>
.logo {
  height: 6em;
  padding: 1.5em;
  will-change: filter;
}
.logo:hover {
  filter: drop-shadow(0 0 2em #646cffaa);
}
.logo.vue:hover {
  filter: drop-shadow(0 0 2em #42b883aa);
}
</style>
