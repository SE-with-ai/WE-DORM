<template>
   <div class="container">
          <h1 >登入</h1>
    <el-form :model="loginForm">
        <el-form-item label="输入用户名：">
        <el-input class="form-control" v-model="loginForm.username" placeholder="username" size="45"  required/>
        </el-form-item>
        <el-form-item>

            <el-button @click="onLogin">Login</el-button>
        </el-form-item>
    </el-form>
    </div>
 
</template>

<script setup lang="ts">

import {ref} from 'vue'
import { useRouter } from 'vue-router';
import { loginFunc } from './api';

const loginForm = ref({
    username:''
})
const router = useRouter()
function onLogin(){
    // window.alert('onlogin')
    loginFunc(loginForm.value.username)
    router.push('/')
}
</script>

<style>
        .size-color{
            color: blue;
            font-size: 25px;
        }
       .textbox {
             height: 25px !important;

             width: 2200px !important;

             font-size: 14px !important;

                } 

</style>