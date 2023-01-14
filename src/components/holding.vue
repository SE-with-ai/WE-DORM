<template>
<!-- form to edit -->
  <el-form :model="editForm" label-width="120px" :hidden="!showEditor">

    <el-form-item label="Item Name">
      <el-input v-model="editForm.name" required="true"/>
    </el-form-item>
    <el-form-item label="Brand">
      <el-input v-model="editForm.brand" />
    </el-form-item>
    <el-form-item label="Description">
      <el-input v-model="editForm.description" />
    </el-form-item>
    <el-form-item label="Consumable">
      <el-switch v-model="editForm.is_consume" />
    </el-form-item>
    <el-form-item label="Activity type">
      <el-checkbox-group v-model="editForm.type">
        <el-checkbox label="Online activities" name="type" />
        <el-checkbox label="Promotion activities" name="type" />
        <el-checkbox label="Offline activities" name="type" />
        <el-checkbox label="Simple brand exposure" name="type" />
      </el-checkbox-group>
    </el-form-item>
    <el-form-item>
      <el-button type="primary" @click="onSubmit">Create</el-button>
      <el-button>Cancel</el-button>
    </el-form-item>
  </el-form>


  <!-- tag control buttons -->
  <el-button @click="resetTagFilter">reset date filter</el-button>
  <el-input v-model="search" placeholder="搜索想借的物品" />
  
  
  <!-- owned item list -->
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

const showEditor = ref(false)
const editForm = ref({
      iid: 0,
  name:'',
  brand:'',
  description:'',
  qty:0,
  is_consume:false,
  tag:[] as string[],
})

function handleEdit(index:number,row:ItemExt)
{
  showEditor.value = true;
  // load data into form
  let item = tableData.value[index]
  editForm.value.iid = item.iid
  editForm.value.name = item.name
  if(item.brand)editForm.value.brand = item.brand
  if(item.description)editForm.value.description = item.description
  editForm.value.qty = item.qty
  editForm.value.is_consume = item.is_consume
  if(item.tag)editForm.value.tag = item.tag
}

const handleEditSubmit = (index: number, row: ItemExt) => {
  // 
    let item= tableData.value[index];
    let itemTags = {tag:[] as string[]}
    if(item.tag)delete item['tag']
    itemTags['tag'] = tableData.value[index]['tag']
  updateItem([item])
  console.log(index, row)
  showEditor.value = false;

}


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