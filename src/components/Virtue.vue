<template>

<el-row :gutter="20">
    <el-col :span="16">
    <div>
        功德值={{virtueRef}}
    </div>
    </el-col>
    <el-col :span="8">
        <a href="https://www.bilibili.com/video/BV1GJ411x7h7">
          <el-button type="Primary" >
            支付宝充值</el-button></a>
    </el-col>
  </el-row>
  <el-table ref="tableRef" row-key="iid" :data="tableData" style="width: 100%">
    <el-table-column prop="text" label="Log" width="100%" />
  </el-table>

</template>
<script setup lang="ts">


import axios from 'axios'
import {ref,computed,onMounted, onBeforeMount} from 'vue'
import {ItemOwned} from './utils'
import { ElTable } from 'element-plus'
import { virlogQuery,virtueQuery} from './api'
import { beforeMain } from '@popperjs/core'



const virtueRef = ref()
const tableRef = ref<InstanceType<typeof ElTable>>()
const tableData= ref([] as {
  text:string
}[])
onBeforeMount(()=>{
  virtueQuery().then((res)=>{virtueRef.value = res})
  virlogQuery().then((res)=>{
    let ress = [] as {
  text:string
}[]
  for (let t =0;t< res.length;++t){
    let st = res[t]
    ress.push({text:st})
  }
  tableData.value = ress;
    })
})


</script>
