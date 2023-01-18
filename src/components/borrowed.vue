<template>

<!-- 借物品form -->
  <el-form :model="borrowForm" v-if="!showEditor">
    <el-form-item label="Item Name">
      <el-input v-model="borrowForm.name" required="true" disabled/>
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
      <el-date-picker v-model="borrowForm.ddl" placeholder="Pick a day" 
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
        :debounce="300"
        placement="bottom"
        popper-class="el-popper"
        :teleported="false"
        @select="onSelectSuggestion"
      >
      </el-autocomplete>
  <el-table ref="tableRef" row-key="iid" :data="tableData" style="width: 100%">
    <el-table-column prop="name" label="Item" width="180" />
    <el-table-column prop="owner" label="Owner" width="180" />
    <el-table-column prop="start_time" label="Date borrowed" width="180" />
    <el-table-column prop="ddl" label="deadline" width="180" />
    <el-table-column prop="time_remained" label="time remained" width="180" />

    <el-table-column label="Operations">
      <template #default="scope">
        <el-button
          size="small"
          type="danger"
          @click="handleReturn(scope.$index, scope.row)"
          >归还</el-button>
      </template>
    </el-table-column>
  </el-table>
</template>
<script setup lang="ts">
import {ref,computed, onMounted,watchEffect} from 'vue'
import {BorrowSuggestion, Item, ItemOwned,ItemToBorrow} from './utils'
import { ElTable, type TableColumnCtx } from 'element-plus'
import { returnItem, searchItem,borrowItem,borrowListQuery } from './api'
import { toNumber } from 'lodash';
// import {modal} from 



const tableRef = ref<InstanceType<typeof ElTable>>()
const tableData= ref<ItemToBorrow[]>([])



const handleReturn = async (index: number, row: ItemToBorrow) => {
  console.log(index, row)

  await returnItem(row.sid,row.iid)
}



onMounted(()=>{
  borrowListQuery().then((res)=>{tableData.value = res;})
  
})

const query_string = ref('')
const options = ref<{name:string,value:string}[]>([])
const options_list = ref<BorrowSuggestion[]>([])
const selected = ref<BorrowSuggestion>({
  iid:0 ,
  item_name:'',
  brand:'',
  description:'',
  owner_id:0 ,
  owner_name:'' ,
  is_consume:false,
})
let timeout=2000
watchEffect(async () => {
  // await searchItem(query_string.value).then((res)=>{options.value=res})

})
const onSearch = (query: string, cb: (arg: any) => void)=>{
   searchItem(query).then((res)=>{
    console.log('searchItem returns',res)

  console.log('search',query,res)
  // searchItem(query_string.value).then((res)=>{
  // console.log('search',query_string.value,res)
  options_list.value = [];
  for (let i = 0; i < res.length;++i)
  {
    let ress = res[i]
    console.log('onSearch:parse',ress)
    options_list.value.push({
      "iid": toNumber(ress['iid']),
  "item_name":ress['name'],
  "brand":ress[2],
  "description":ress[3],
  "owner_id": toNumber(ress['owner_id']),
  "owner_name":ress['owner_name'], 
  "is_consume":false,
  
    })
  }
   })

  

  options.value = options_list.value.filter(
    (item)=>{
      return (item['item_name']!= undefined)
    }).map((item)=>{
      console.log('filter',item);
      return({
        name:item['iid'].toString(),
      value:item['item_name']+'('+item['owner_name']+')'
    })
  })
    const results = options.value
    ? options.value
    : []
  clearTimeout(timeout)
  timeout = setTimeout(() => {
    console.log('results:',results,options.value,query)
    cb(results)
  }, 3000 * Math.random())

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

function onSelectSuggestion(item_selected:{name:string,value:string})
{
  // load data into form
  console.log('onselectsuggestion',item_selected)
  let item = options_list.value.filter((it)=>(it['iid'] === toNumber(item_selected.name)))
  if(item.length===0 || item[0].iid == 0)return;
  console.log(item[0])
  window.alert(item[0])
  borrowForm.value.iid = item[0]['iid']
  borrowForm.value.name = item[0].item_name
  if(item[0].brand)borrowForm.value.brand = item[0].brand
  if(item[0].description)borrowForm.value.description = item[0].description
  borrowForm.value.is_consume = item[0].is_consume
  // showEditor.value = true;
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

.el-autocomplete-suggestion,.el-popper{
  background-color: white;
}
.el-picker-panel.el-date-picker{
  background-color: white;
}



/* Inline #4 | http://127.0.0.1:5173/borrow */

.el-form {
  display: grid;
}
el-form-item{
  width:50%;
}

/* Inline #4 | http://127.0.0.1:5173/borrow */

i>svg {
  width: 3em;
  /* display: inline-block; */
}

</style>