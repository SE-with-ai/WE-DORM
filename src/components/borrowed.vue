<template>

<!-- 借物品form -->
  <el-form :model="borrowForm" label-width="120px" :hidden="!showEditor">

    <el-form-item label="Item Name">
      <el-input v-model="borrowForm.name" required="true" from="" disabled/>
    </el-form-item>
    <el-form-item label="Brand">
      <el-input v-model="borrowForm.brand" disabled/>
    </el-form-item>
    <el-form-item label="Description">
      <el-input v-model="borrowForm.description"  disabled/>
    </el-form-item>
    <el-form-item label="Consumable">
      <el-switch v-model="borrowForm.is_consume"  disabled/>
    </el-form-item>
    <el-form-item label="Date">
      <el-date-picker v-model="borrowForm.ddl" type="date" placeholder="Pick a day" 
        :disabled-date="disabledDate" />
    </el-form-item>
    <el-form-item>

      <el-button type="primary" @click="onBorrowSubmit" >Provide</el-button>
      <el-button @click="showEditor=false">Cancel</el-button>
    </el-form-item>
  </el-form>


  <el-input v-model="search" placeholder="搜索想借的物品" />
  <el-button @click="onSearch()">搜索</el-button>
    
  <el-table ref="tableRef" row-key="iid" :data="tableData" style="width: 100%">
    <el-table-column prop="name" label="Item" width="180" />
    <el-table-column prop="owner" label="Name" width="180" />
    <el-table-column prop="start_time" label="Name" width="180" />
    <el-table-column prop="ddl" label="Name" width="180" />
    <el-table-column prop="time_remained" label="Name" width="180" />

    <el-table-column label="Operations">
      <template #default="scope">
        <el-button
          size="small"
          type="danger"
          @click="handleReturn(scope.$index, scope.row)"
          >归还</el-button
        >
      </template>
    </el-table-column>
  </el-table>
</template>
<script setup lang="ts">
import {ref,computed} from 'vue'
import {Item, ItemOwned} from './utils'
import { ElTable, type TableColumnCtx } from 'element-plus'
import { returnItem, searchItem } from './api'
// import {modal} from 



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


const handleReturn = (index: number, row: ItemOwned) => {
  console.log(index, row)

  let status = returnItem(row.sid,row.iid)
  console.log(status)
  if(typeof status !== typeof {} )window.alert(status?.get('msg'))
}


const search = ref('')
const suggestions = ref([])
const onSearch = ()=>{
  searchItem(search.value)
  // TODO: show suggestion
}
const onSelectSuggestion = ()=>{
  // TODO: turn suggestion into
}

const borrowForm = ref({
      iid: 0,// read from item chosen
  name:'',// read from item chosen
  brand:'',// read from item chosen
  description:'',// read from item chosen
  is_consume:false,// read from item chosen
  owner:'',// read from item chosen
  ddl:new Date(),

})
const disabledDate = (time: Date) => {
  return time.getTime() < Date.now()
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
  if(item.tag)editForm.value.tag = item.tag
}

const handleEditSubmit = (index: number, row: ItemOwned) => {
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