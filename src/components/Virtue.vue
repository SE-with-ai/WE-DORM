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
    <el-table-column prop="text" label="Log" width="180" />
  </el-table>

</template>
<script setup lang="ts">


import axios from 'axios'
import {ref,computed,onMounted} from 'vue'
import {Item, ItemOwned, Virlog} from './utils'
import { ElTable, type TableColumnCtx } from 'element-plus'
import { deleteItem, itemsQuery, searchItem } from './api'



const virtueRef = ref()
const tableRef = ref<InstanceType<typeof ElTable>>()
const tableData= ref<Virlog[]>([])


const filterTag = (value: string[], row: ItemOwned) => {
  
  return value.length === 0 || row.tag.sort().toString() === value.sort().toString()
}
const tagsRef = ref<string[]>([])
const filterHandler = (
  value: string,
  row: Item,
  column: TableColumnCtx<Item>
) => {
  const property = column['property']
  return row[property] === value
}


const handleDelete = (index: number, row: ItemOwned) => {
  console.log(index, row)

  let status = deleteItem(row.iid)
  console.log(status)
  location.reload()
}


const search = ref('')
const onSearch = ()=>{
  searchItem(search.value)
}
onMounted(()=>{
  tableData.value = itemsQuery()
})


</script>
