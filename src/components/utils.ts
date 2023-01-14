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

export interface ShareRelation{
  sid:number
  uid:number
  iid:number 
  modified:Date
  ddl:Date

}
export interface OwnRelation{
  oid:number
  uid:number
  iid:number
}
export interface Tag{
  text:string
  IID: number
}
export interface ItemExt extends Item{
  tag:string[]
}
export interface Virtue{
  uid:number
  virtue:number
}
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