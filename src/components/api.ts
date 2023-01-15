import axios from "axios";
import { dateToString, Item, ItemOwned, ItemToBorrow, BorrowSuggestion } from "./utils";
class http_request {
  method = "POST";
  baseURL = "https://localhost:15000";// 修改成后端的地址
  url: string;
  data: object;
  constructor(url: string, data: object) {
    this.url = url;
    this.data = data;
  }
}
async function make_request(url: string, data: object) {
  let req = new http_request(url, data);
  let response = await axios(req)
  return response;
}


export async function insert_item(item: Item[]) {
  /* 
    return json.dumps({'code': 500, 'msg': "添加物品失败"})
    return json.dumps({'code': 500, 'msg': "添加拥有关系失败"})
    return json.dumps({'code': 200, 'msg': "添加成功，已有标签"})
    return json.dumps({'code': 500, 'msg': "新建标签失败"})
    return json.dumps({'code': 200, 'msg': "添加成功，新增标签"})
    */
  let response = await make_request("/api/insert-item", { item });
  if(response === undefined)window.alert('响应超时')
  else{
    if (response['code'] !== 200) window.alert(response["msg"] as string);
    location.reload()
  }
}

export async function virtueQuery() {
  /* 
    return json.dumps({'code': 200, 'virtue': result[1]})

*/
  let response:number =  await make_request("/api/virtue-query", {});
  if(response === undefined)response = 0;
  return response
}
export async function virlogQuery() {
  /* 
    return json.dumps({'code': 200, 'virtue log': result}) */
  let response = await make_request("/api/virlog", {});
  if (typeof response === typeof "") {
    response = []
  }
  return response
}
export async function itemsQuery(){
  /* 
    return json.dumps({'code': 200, 'My item': my_item, 'is borrowing': borrowing_item})
    */
  // return json.dumps({'code': 200, 'My item': my_item, 'is borrowing': borrowing_item})
  let response = await make_request("/api/items", {});
  if (response === undefined) return [];
  return response;
}
export async function borrowListQuery() {

  let response = make_request("/api/borrow-list", {})
  if (response === undefined) return [];
  return response as ItemToBorrow[]
}
export async function updateItem(item: Item) {
  /*     return {"code":200}
   */
  let response = await make_request("/api/update-item", item);
  if(response === undefined)window.alert('响应超时')
  else{
    if (response['code'] !== 200) window.alert(response["msg"] as string);
    location.reload()
  }
}
export async function searchItem(nm: string) {

  return await make_request("/api/search-item", { name: nm }) as BorrowSuggestion[]
  
}
export async function borrowItem(item_id: number, deadline: Date) {
  /* return {"code":200} */
  let response = await make_request("/api/search-item", {
    iid: item_id,
    // modi:dateToString(modified),
    ddl: dateToString(deadline),
  });
  if(response === undefined)window.alert('响应超时')
  else{
    if (response['code'] !== 200) window.alert(response["msg"] as string);
    location.reload()
  }
}
export async function returnItem(share_id: number, item_id: number) {
  /* 
    return json.dumps({'code': 200, 'msg': "自己借自己的东西并且成功归还"})
    return json.dumps({'code': 200, 'msg': "成功按时归还"})
    return json.dumps({'code': 200, 'msg': "借用超时，成功归还"})
    */
  let response = await make_request("/api/return-item", {
    sid: share_id,
    iid: item_id,
  });
  if(response === undefined)window.alert('响应超时')
  else{
    if (response['code'] !== 200) window.alert(response["msg"] as string);
    location.reload()
  }
}
export async function deleteItem(item_id: number) {
  /* 
    return json.dumps({'code': 500, 'msg': "非物品拥有者，删除失败"})
    return json.dumps({'code': 500, 'msg': "物品正在借出，无法删除"})
    return json.dumps({'code': 200, 'msg': "物品已删除"})
    */
  let response = await make_request("/api/delete-item", { iid: item_id });
  if (response['code'] !== 200) window.alert(response["msg"] as string);
  location.reload()
}
export async function deleteUser() {
  make_request("/api/delete-user", {});
}
