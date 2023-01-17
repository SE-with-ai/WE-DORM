<template>
<!-- form to create/edit -->
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
      <el-checkbox v-model="editForm.is_consume" />
    </el-form-item>
    <el-form-item label="Tags（用','分开）">
      <el-input v-model="editForm.tag" />
    </el-form-item>

    <el-form-item>
      <!--TODO:correct function to call-->
      <el-button type="primary" @click="handleEditSubmit" :hidden="isCreate">Edit</el-button>
      <el-button type="primary" @click="handleCreateSubmit" :hidden="!isCreate">Provide</el-button>
      <el-button @click="showEditor=false">Cancel</el-button>
    </el-form-item>
  </el-form>


  <!-- tag control buttons -->
  <!-- <el-button @click="resetTagFilter">reset date filter</el-button> -->
  <el-button @click="handleCreate" :hidden="showEditor">增加物品</el-button>
  
  <!-- owned item list -->
  <el-table ref="tableRef" row-key="iid" :data="tableData" style="width: 100%">
    <el-table-column prop="name" label="Name" width="180" />
    <el-table-column prop="brand" label="Brand" width="180" />
    <el-table-column prop="description" label="Description" width="180" />
    <el-table-column prop="qty" label="Quantity" width="180" />
    <el-table-column prop="is_consume" label="Consumable" width="180" />
    <!--TODO:可以用input简化，改成comma-separated-->
    <el-table-column
      prop="tag"
      label="Tag"
      :filters="tagsRef"
      :filter-method="filterTag"
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
import {ref,computed,onBeforeMount, watchEffect} from 'vue'
import {ItemInserted, ItemOwned} from './utils'
import { ElTable, type TableColumnCtx } from 'element-plus'
import { deleteItem, itemsQuery, searchItem, updateItem,insertItem } from './api'



const tableRef = ref<InstanceType<typeof ElTable>>()
const tableData= ref<ItemOwned[]>([])


const filterTag = (value: string[], row: ItemOwned) => {
  
  return value.length === 0 || row.tag.sort().toString() === value.sort().toString()
}
const tagsRef = ref<string[]>([])
const filterHandler = (
  value: string,
  row: ItemOwned,
  column: TableColumnCtx<ItemOwned>
) => {
  const property = column['property']
  return row[property] === value
}

const handleDelete = (index: number, row: ItemOwned) => {
  console.log(index, row)

  let status = deleteItem(row.iid)
  console.log(status)
  if(typeof status === typeof {} )window.alert(status?.get('msg'))
}



onBeforeMount(()=>{
  itemsQuery().then((res)=>{
    console.info(res)
    tableData.value = res;
    })
})

const showEditor = ref(false)
const isCreate = ref(true)
const editForm = ref({
      iid: 0,
  name:'',
  brand:'',
  description:'',
  qty:0,
  is_consume:false,
  tag:'',
})
const defaultForm = {
      iid: 0,
  name:'',
  brand:'',
  description:'',
  qty:0,
  is_consume:false,
  tag:'',
}

function handleEdit(index:number,row:ItemOwned)
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
  if(item.tag)editForm.value.tag = item.tag.join(', ')
}

const handleEditSubmit = () => {

let item= editForm.value
    console.log(item)
    let itemTags = [] as string[]
    itemTags= item['tag'].split(',')
    itemTags.forEach((tag)=>tag.trim())

  updateItem({
  iid: item['iid'],
  name:item['name'],
  brand:item['brand'],
  description:item['description'],
  qty:item['qty'],
  is_consume:item['is_consume'],
  borrowing:false,
  tag:itemTags
} as ItemOwned)
  showEditor.value = false;
  editForm.value = defaultForm

}
function handleCreate(index:number,row:ItemOwned)
{
  showEditor.value = true;
  // load data into form
  
    let item= tableData.value[index];
  editForm.value.name = ''
  if(item.brand)editForm.value.brand = ''
  if(item.description)editForm.value.description = ''
  editForm.value.qty = 0
  editForm.value.is_consume = false
  if(item.tag)editForm.value.tag = item.tag.join(', ')
}

const handleCreateSubmit = () => {

let item= editForm.value
    console.log(item)
    let itemTags = [] as string[]
    itemTags= item['tag'].split(',')
    itemTags.forEach((tag)=>tag.trim())

    insertItem({
    name:item['name'],
    brand:item['brand'],
    description:item['description'],
    qty:item['qty'],
    is_consume:item['is_consume'],
    tag:itemTags
  } as ItemInserted)
  showEditor.value = false;
  editForm.value = defaultForm


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