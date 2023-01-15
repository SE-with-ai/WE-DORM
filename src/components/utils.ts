export interface User{
  uid:number 
  name:string
  dorm:string
  email?:string
}
export interface Item {
  iid: number
  name:string
  brand?:string
  description?:string
  qty:number
  is_consume:boolean
  
}

// interface ShareRelation{
//   sid:number
//   uid:number
//   iid:number 
//   modified:Date
//   ddl:Date
  
// }
// interface OwnRelation{
//   oid:number
//   uid:number
//   iid:number
// }
// interface Tag{
//   text:string
//   IID: number
// }
// to show in holding table
export interface ItemOwned extends Item{
  borrowing:boolean
  tag:string[]
}
// TODO: item format to show in borrowing table
export interface ItemToBorrow{
  sid:number
  iid: number
  name:string
  owner_uid:number 
  owner_name:string
  modified:Date
  ddl:Date
}

export interface BorrowSuggestion{
  iid:number 
  item_name:string
  owner_id:number 
  owner_name:string 
}

// export interface Virtue{
//   uid:number
//   virtue:number
// }
export interface Virlog{
  uid:number 
  virlog:string
}

export function dateToString(date: Date) {
  const padTo2Digits = (num: number) => num.toString().padStart(2, '0');
    return (
      [
        date.getFullYear(),
        padTo2Digits(date.getMonth() + 1),
        padTo2Digits(date.getDate()),
      ].join('-')
    );
  }
