<template>

<!-- 借物品form -->
  <el-form :model="borrowForm" label-width="120px" :hidden="!showEditor">
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

      <el-button type="primary" @click="onBorrowSubmit" >开借</el-button>
      <el-button @click="showEditor=false">Cancel</el-button>
    </el-form-item>
  </el-form>


  <el-autocomplete
    id="search-bar"
        v-model="selected"
        placeholder="搜索想借的物品"
        remote
        filterable
        :fetch-suggestion="onSearch"
        :loading="loading"
        @select="onSelectSuggestion"
      >
        <el-option
          v-for="item in options"
          :key="item.iid"
          :label="item.item_name+'（'+item.owner_name+'）'"
          :value="item.iid"
        />
  </el-autocomplete>
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
import {ref,computed, onMounted} from 'vue'
import {BorrowSuggestion, Item, ItemOwned,ItemToBorrow} from './utils'
import { ElTable, type TableColumnCtx } from 'element-plus'
import { returnItem, searchItem,borrowItem,borrowListQuery } from './api'
// import {modal} from 



const tableRef = ref<InstanceType<typeof ElTable>>()
const tableData= ref<ItemOwned[]>([])


const filterTag = (value: string[], row: ItemOwned) => {
  
  return value.length === 0 || row.tag.sort().toString() === value.sort().toString()
}
const tagsRef = ref<string[]>([])
const filterHandler = (
  value: string,
  row: ItemToBorrow,
  column: TableColumnCtx<ItemOwned>
) => {
  const property = column['property']
  return row[property] === value
}


const handleReturn = async (index: number, row: ItemToBorrow) => {
  console.log(index, row)

  await returnItem(row.sid,row.iid).then(
        ()=>{
      tableData.value = borrowListQuery()
        }
  )
}



onMounted(()=>{
  borrowListQuery().then((res)=>{tableData.value = res;})
  
})


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
const onSearch = (query: string)=>{
  if (query) {
    loading.value = true
    setTimeout(() => {
      searchItem(query).then((res)=>{
        
        options.value = res

        })
      loading.value = false
    }, 200)
  } else {
    options.value = []
  }
  searchItem(search.value).then((res)=>{
    options.value = res
  })
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

const disabledDate = (time: Date) => {
  return time.getTime() < Date.now()
}

function onSelectSuggestion()
{
  // load data into form
  let item = selected.value
  borrowForm.value.iid = item.iid
  borrowForm.value.name = item.name
  if(item.brand)borrowForm.value.brand = item.brand
  if(item.description)borrowForm.value.description = item.description
  borrowForm.value.qty = item.qty
  borrowForm.value.is_consume = item.is_consume
  if(item.tag)borrowForm.value.tag = item.tag
  showEditor.value = true;
}

const onBorrowSubmit = () => {
  // 
    let item= tableData.value[index];
    let itemTags = {tag:[] as string[]}
    if(item.tag)delete item['tag']
    itemTags['tag'] = tableData.value[index]['tag']
  borrowItem().then(()=>{
  tableData.value = borrowListQuery()
  })
  console.log(index, row)
  showEditor.value = false;

}

</script>

<style>
</style>