<template>
<form action="action_page.php" method="post">
  <div class="imgcontainer">
    <img src="img_avatar2.png" alt="Avatar" class="avatar">
  </div>

  <div class="container">
    <label for="uname"><b>Username</b></label>
    <input type="text" placeholder="Enter Username" name="uname" required>

    <label for="psw"><b>Password</b></label>
    <input type="password" placeholder="Enter Password" name="psw" required>

    <button type="submit">Login</button>
    <label>
      <input type="checkbox" checked="checked" name="remember"> Remember me
    </label>
  </div>

  <div class="container" style="background-color:#f1f1f1">
    <button type="button" class="cancelbtn">Cancel</button>
    <span class="psw">Forgot <a href="#">password?</a></span>
  </div>
</form>
  <el-input v-model="search" placeholder="搜索想借的物品" />
  <el-button @click="onSearch()">搜索</el-button>
    r
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
import {Item, ItemExt} from './utils'
import { ElTable, type TableColumnCtx } from 'element-plus'
import { returnItem, searchItem } from './api'



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


const handleReturn = (index: number, row: ItemExt) => {
  console.log(index, row)

  let status = returnItem(row.sid,row.iid)
  console.log(status)
  if(typeof status !== typeof {} )window.alert(status?.get('msg'))
}


const search = ref('')
const onSearch = ()=>{
  searchItem(search.value)
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