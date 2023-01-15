import axios from "axios";
import { dateToString, Item, ItemOwned, Virlog } from "./utils";
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
function make_request(url: string, data: object): object {
  let req = new http_request(url, data);
  let response;
  axios(req).then(
    (res) => {
      response = JSON.parse(res as string);
    },
    (reason) => {
      response = { msg: reason };
    }
  );
  return response;
}
export function login(name: string) {
  make_request("/login", { username: name });
  location.reload()
}

export function insert_item(item: Item[]) {
  /* 
    return json.dumps({'code': 500, 'msg': "添加物品失败"})
    return json.dumps({'code': 500, 'msg': "添加拥有关系失败"})
    return json.dumps({'code': 200, 'msg': "添加成功，已有标签"})
    return json.dumps({'code': 500, 'msg': "新建标签失败"})
    return json.dumps({'code': 200, 'msg': "添加成功，新增标签"})
    */
  let response = make_request("/api/insert-item", { item });
  window.alert(response["msg"] as string);
}

export function virtueQuery() {
  /* 
    return json.dumps({'code': 200, 'virtue': result[1]})

*/
  let response = make_request("/api/virtue-query", {}) as object;
  response = response["virtue"][1];
  if (typeof response === typeof "") {
    response = [];
  }
  return response;
}
export function virlogQuery() {
  /* 
    return json.dumps({'code': 200, 'virtue log': result}) */
  let response = make_request("/api/virlog", {});
}
export function itemsQuery(): ItemOwned[] {
  /* 
    return json.dumps({'code': 200, 'My item': my_item, 'is borrowing': borrowing_item})
    */
  // return json.dumps({'code': 200, 'My item': my_item, 'is borrowing': borrowing_item})
  let response = make_request("/api/items", {});
  if (response === undefined) return [];
  let result: ItemOwned[] = [];
  result = response["My item"] as ItemOwned[];
  for (let res = 0; res < result.length; ++res) {
    result[res]["borrowed"] = response["borrowing"][res];
  }
  return result;
}
export function borrowListQuery() {
  /* 
        return json.dumps({'code': 200, 
                       'msg': "查询成功",
                       'borrow_item_list': item_info, 
                       'owner': owner_info, 
                       'borrow start from':start_time, 
                       'ddl': ddl, 
                       'time remain':time_remain, 
                       'sid list':sid_list})
    */
  make_request("/api/borrow-list", {});
}
export function updateItem(item: Item) {
  /*     return {"code":200}
   */
  make_request("/api/update-item", item);
}
export function searchItem(nm: string) {
  /* 
        return json.dumps({'code': 200, "item info" :result, 'borrow state':is_borrowing})

    */
   // TODO: structuring response into 
  let response = make_request("/api/search-item", { name: nm });
  
}
export function borrowItem(item_id: number, deadline: Date) {
  /* return {"code":200} */
  make_request("/api/search-item", {
    iid: item_id,
    // modi:dateToString(modified),
    ddl: dateToString(deadline),
  });
}
export function returnItem(share_id: number, item_id: number) {
  /* 
    return json.dumps({'code': 200, 'msg': "自己借自己的东西并且成功归还"})
    return json.dumps({'code': 200, 'msg': "成功按时归还"})
    return json.dumps({'code': 200, 'msg': "借用超时，成功归还"})
    */
  let response = make_request("/api/return-item", {
    sid: share_id,
    iid: item_id,
  });
  window.alert(response["msg"]);
  location.reload();
}
export function deleteItem(item_id: number) {
  /* 
    return json.dumps({'code': 500, 'msg': "非物品拥有者，删除失败"})
    return json.dumps({'code': 500, 'msg': "物品正在借出，无法删除"})
    return json.dumps({'code': 200, 'msg': "物品已删除"})
    */
  let response = make_request("/api/delete-item", { iid: item_id });
  window.alert(response['msg'])
  location.reload();
}
export function deleteUser() {
  make_request("/api/delete-user", {});
}
