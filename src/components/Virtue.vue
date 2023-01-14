<template>

<el-row :gutter="20">
    <el-col :span="16">
    <div>
        功德值={{virtueRef}}
    </div>
    </el-col>
    <el-col :span="8">
        <el-button type="Primary" href="https://www.bilibili.com/video/BV1GJ411x7h7">
            支付宝充值</el-button>
    </el-col>
  </el-row>
  <el-table ref="tableRef" row-key="iid" :data="tableData" style="width: 100%">
    <el-table-column prop="name" label="Name" width="180" />
    <el-table-column prop="brand" label="Brand" width="180" />
    <el-table-column prop="description" label="Description" width="180" />
    <el-table-column prop="qty" label="Quantity" width="180" />
    <el-table-column prop="is_consume" label="Consumable" width="180" />

    <el-table-column
      prop="tag"
      label="Tag"
      width="100"
      :filters="tagsRef"
      :filter-method="filterTag"
      filter-placement="bottom-end"
    >
      <template #default="scope">
        <el-tag
          v-for="tg in scope.row.tag"
          type="success"
          disable-transitions
          >{{ tg }}</el-tag>
      </template>
    </el-table-column>
    <el-table-column label="Operations">
      <template #default="scope">
        <el-button size="small" @click="handleEdit(scope.$index, scope.row)"
          >Edit</el-button
        >
        <el-button
          size="small"
          type="danger"
          @click="handleDelete(scope.$index, scope.row)"
          >Delete</el-button
        >
      </template>
    </el-table-column>
  </el-table>

<!--TODO:功德录-->
</template>
<script setup lang="ts">


import axios from 'axios'
import {ref,computed,onMounted} from 'vue'
import {Item, ItemExt} from './utils'
import { ElTable, type TableColumnCtx } from 'element-plus'
import { deleteItem, itemsQuery, searchItem } from './api'
import { offset } from '@floating-ui/core'



const virtueRef = ref()
const tableRef = ref<InstanceType<typeof ElTable>>()
const tableData= ref<ItemExt[]>([])


const filterTag = (value: string[], row: ItemExt) => {
  
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


const handleDelete = (index: number, row: ItemExt) => {
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
