<template>
  <el-form :model="form" label-width="120px" :hidden="!showEditor">
    <el-form-item label="Item Name">
      <el-input v-model="form.name" />
    </el-form-item>
    <el-form-item label="Activity time">
      <el-col :span="11">
        <el-date-picker
          v-model="form.date1"
          type="date"
          placeholder="Pick a date"
          style="width: 100%"
        />
      </el-col>
      <el-col :span="2" class="text-center">
        <span class="text-gray-500">-</span>
      </el-col>
      <el-col :span="11">
        <el-time-picker
          v-model="form.date2"
          placeholder="Pick a time"
          style="width: 100%"
        />
      </el-col>
    </el-form-item>
    <el-form-item label="Instant delivery">
      <el-switch v-model="form.delivery" />
    </el-form-item>
    <el-form-item label="Activity type">
      <el-checkbox-group v-model="form.type">
        <el-checkbox label="Online activities" name="type" />
        <el-checkbox label="Promotion activities" name="type" />
        <el-checkbox label="Offline activities" name="type" />
        <el-checkbox label="Simple brand exposure" name="type" />
      </el-checkbox-group>
    </el-form-item>
    <el-form-item label="Resources">
      <el-radio-group v-model="form.resource">
        <el-radio label="Sponsor" />
        <el-radio label="Venue" />
      </el-radio-group>
    </el-form-item>
    <el-form-item label="Activity form">
      <el-input v-model="form.desc" type="textarea" />
    </el-form-item>
    <el-form-item>
      <el-button type="primary" @click="onSubmit">Create</el-button>
      <el-button>Cancel</el-button>
    </el-form-item>
  </el-form>
  <el-button @click="resetTagFilter">reset date filter</el-button>
  <el-input v-model="search" placeholder="搜索想借的物品" />
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
          >Delete</el-button>
      </template>
    </el-table-column>
  </el-table>
</template>
<script setup lang="ts">
import axios from 'axios'
import {ref,computed,onMounted, watchEffect} from 'vue'
import {Item, ItemExt} from './utils'
import { ElTable, type TableColumnCtx } from 'element-plus'
import { deleteItem, itemsQuery, searchItem, updateItem } from './api'
import { offset } from '@floating-ui/core'



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
  if(typeof status === typeof {} )window.alert(status?.get('msg'))
}


const search = ref('')
const onSearch = ()=>{
  searchItem(search.value)
}
onMounted(()=>{
  tableData.value = itemsQuery()
})
watchEffect(async () => {
  const response = await fetch(
    `https://jsonplaceholder.typicode.com/todos/${todoId.value}`
  )
  data.value = await response.json()
})

const showEditor = ref(false)
const form = ref({
      iid: 0,
  name:'',
  brand:'',
  description:'',
  qty:0,
  is_consume:false,
  tag:[],
})

function handleEdit(row:ItemExt)
{
  showEditor.value = true;
}

const handleEditSubmit = (index: number, row: ItemExt) => {
  // 
    let item= row;
    if(item.tag)delete item['tag']
  updateItem(item)
  console.log(index, row)
  showEditor.value = false;

}

// TODO: parse data returned by backend

</script>

<style>
/* Style the search field */
form.example input[type=text] {
  padding: 10px;
  font-size: 17px;
  border: 1px solid grey;
  float: left;
  width: 80%;
  background: #f1f1f1;
}

/* Style the submit button */
form.example button {
  float: left;
  width: 20%;
  padding: 10px;
  background: #2196F3;
  color: white;
  font-size: 17px;
  border: 1px solid grey;
  border-left: none; /* Prevent double borders */
  cursor: pointer;
}

form.example button:hover {
  background: #0b7dda;
}

/* Clear floats */
form.example::after {
  content: "";
  clear: both;
  display: table;
}
</style>