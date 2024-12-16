import { useState, useEffect } from 'react';
import './Hooks.css';

export default Hooks;

function Hooks(){
    let [state , setState] = useState(0);
    useEffect(() => {
        alert("Page Refreshed!")
        return () => {
            alert("Hooks Unmounted From Main Page !") 
        }
    },[])
   return <>
     <h1>React Hooks</h1> 

       <div>
          <h2> Count  : {state}</h2>  
          <button onClick={()=>setState(state => state + 1)}>Functional Update Count</button>
            <button onClick={()=>setState(state+1)}>Direct Update Count</button>
            <button onClick={()=> setState(0)}> Reset Counter</button>
        </div>
    </>
}