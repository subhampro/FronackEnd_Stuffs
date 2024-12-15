export default function Map({colorss}){
    
    return <>
    <h1>All Colors Function</h1>
    <ul>
    {colorss.map((color) => <li style={{color: color}}>{color}</li>)}     
    </ul>
    </> 
}