<template>

<!-- 借物品form -->
  <el-form :model="borrowForm" :hidden="!showEditor">
    <el-form-item></el-form-item>
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

      <el-button type="primary" @click="onBorrowSubmit" >借！</el-button>
      <el-button @click="showEditor=false">取消</el-button>
    </el-form-item>
  </el-form>


  <el-autocomplete
    id="search-bar"
        v-model="query_string"
        placeholder="搜索想借的物品"
        :fetch-suggestions="onSearch"
        @select="onSelectSuggestion"
      />
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
import {ref,computed, onMounted,watchEffect} from 'vue'
import {BorrowSuggestion, Item, ItemOwned,ItemToBorrow} from './utils'
import { ElTable, type TableColumnCtx } from 'element-plus'
import { returnItem, searchItem,borrowItem,borrowListQuery } from './api'
// import {modal} from 



const tableRef = ref<InstanceType<typeof ElTable>>()
const tableData= ref<ItemOwned[]>([])



const handleReturn = async (index: number, row: ItemToBorrow) => {
  console.log(index, row)

  await returnItem(row.sid,row.iid)
}



onMounted(()=>{
  borrowListQuery().then((res)=>{tableData.value = res;})
  
})

const query_string = ref('')
const options = ref<BorrowSuggestion[]>([])
const selected = ref<BorrowSuggestion>({
  iid:0 ,
  item_name:'',
  brand:'',
  description:'',
  owner_id:0 ,
  owner_name:'' ,
  is_consume:false,
})
const loading = ref(false)

const search = ref('')
const showSuggestions = ref(false)
let timeout=2000
watchEffect(async () => {
  const response = await searchItem(query_string.value)
  options.value = await response
})
const onSearch = (query: string, cb: (arg: any) => void)=>{
    const results = query
    ? options.value
    : []

  clearTimeout(timeout)
  timeout = setTimeout(() => {
    cb(results)
  }, 3000 * Math.random())



  showSuggestions.value = true
}

const showEditor = ref(false)
const borrowForm = ref({
  iid: 0,// read from item chosen
  name:'',// read from item chosen
  brand:'',// read from item chosen
  description:'',// read from item chosen
  is_consume:false,// read from item chosen
  owner:'',// read from item chosen
  ddl:new Date(),

})
const defaultForm = {
  iid: 0,// read from item chosen
  name:'',// read from item chosen
  brand:'',// read from item chosen
  description:'',// read from item chosen
  is_consume:false,// read from item chosen
  owner:'',// read from item chosen
  ddl:new Date(),

}

const disabledDate = (time: Date) => {
  return time.getTime() < Date.now()
}

function onSelectSuggestion(item:BorrowSuggestion)
{
  // load data into form
  borrowForm.value.iid = item.iid
  borrowForm.value.name = item.item_name
  if(item.brand)borrowForm.value.brand = item.brand
  if(item.description)borrowForm.value.description = item.description
  borrowForm.value.is_consume = item.is_consume
  showEditor.value = true;
}

const onBorrowSubmit = () => {
  // 
    let item= borrowForm.value;
  borrowItem(item.iid,item.ddl)
  showEditor.value = false;
  borrowForm.value = defaultForm
}

</script>

<style >

/* Inline #4 | http://127.0.0.1:5173/borrow */

.el-picker-panel.el-date-picker {
  background-color: white;
}

/* Inline #3 | http://127.0.0.1:5173/borrow */

.el-form-item {
  /* margin: 20% 0% auto auto; */
}

/* Inline #4 | http://127.0.0.1:5173/borrow */

.el-form {
  display: grid;
}

/* Inline #4 | http://127.0.0.1:5173/borrow */

i>svg {
  width: 3em;
  display: inline-block;
}

</style>