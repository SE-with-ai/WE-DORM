
<template class="common-layout"> 
<!-- <widget-container-modal /> -->
    <el-container>
      <el-header>
        <h1>WEDORM</h1>
        <!--TODO:use vue-router to go open login page-->
        <router-link to="/">
          <el-button>自己的物品</el-button>
        </router-link>
        <router-link to="/borrow">
          <el-button>借用物品</el-button>
        </router-link>
        <router-link to="/virtue">
          <el-button>功德录</el-button>
        </router-link>
            <el-button @click="deleteUserConfirm=!deleteUserConfirm" :if="loggedin">删除账号</el-button>
          <el-button @click="trick=!trick" :hidden="!deleteUserConfirm">确定？</el-button>
          <el-button :hidden="!trick">不让你删</el-button>
      </el-header>
      <el-main>
        <router-view/>
    </el-main>
  </el-container>

</template>
<script setup lang="ts">
import Holding from './components/Holding.vue'
import Borrowed from './components/Borrowed.vue'
import Virtue from './components/Virtue.vue'
import {ref,computed} from 'vue'
import {container as WidgetContainerModal} from 'jenesius-vue-modal'
import { useRouter } from 'vue-router'
  const router = useRouter()
  const deleteUserConfirm = ref(false)
  const trick = ref(false)
  const loggedin = computed(()=>{window.sessionStorage.getItem('WEDORM-uid') !== undefined;})
</script>
<style scoped>


</style>
