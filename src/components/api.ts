import axios from "axios"
import { dateToString, Item } from "./utils";
class http_request{
    method='POST';
    baseURL="https://localhost:15000";
    url:string;
    data:object;
    constructor(url:string,data:object){
        this.url = url;
        this.data = data;
    }
}
function make_request(url:string,data:object){
    let req= new http_request(url,data)
    let response;
    axios(req).then((res)=>{
        response = res;
    })
    return response;
}
export function login(name:string){
    return make_request('/login',{username:name});
}

export function insert_item(item:Item[]){
    return make_request('/api/insert-item',{item});
}

export function virtueQuery(){
    return make_request('/api/virtue-query',{});
}
export function virlogQuery(){
    return make_request('/api/virlog',{});
}
export function itemsQuery(){
    return make_request('/api/items',{});
}
export function borrowListQuery(){
    return make_request('/api/borrow-list',{});
}
export function updateItem(item:Item[]){
    return make_request('/api/update-item',{item});
}
export function searchItem(nm:string){
    return make_request('/api/search-item',{name:nm});
}
export function borrowItem(item_id:number,deadline:Date){
    return make_request('/api/search-item',{
        iid:item_id,
        // modi:dateToString(modified),
        ddl:dateToString(deadline)
    });
}
export function returnItem(share_id:number,item_id:number){
    return make_request('/api/return-item',{
        sid:share_id,
        iid:item_id
    })
}
export function deleteItem(item_id:number){
    return make_request('/api/delete-item',{iid:item_id})
}