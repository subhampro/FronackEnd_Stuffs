import { useState , useFilter , useRef } from "react";

export default function App_3(){
const [ c , updateC ] = useState(0);    
return    <>
    <h1>Click Counter : {c}</h1>
    <button onClick={ () => updateC(c+1)}>Click Me to Increase Click Count</button>
    </>
}