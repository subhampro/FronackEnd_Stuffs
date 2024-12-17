import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'

function App({numbers = 0}) {
  const count = Math.floor(Math.random() * 6) + 1;
  const count2 = Math.floor(Math.random() * 6) + 1;
  let [gameCount, updateGame ]= useState(0);
  return (
    <>
      <h2>Player 1</h2>
      <h3>Dice : {count}</h3>
      <h2>Com 1</h2>
      <h3>Dice : {count2}</h3>

      <h1 style = {count === count2 ?  { color: "green"}:  { color: "red"} }>{count === count2 ? "Player Win" : "Computer Win"}</h1>

      <button onClick={()=>updateGame((Game)=> Game+1)}>Game Count : {gameCount}</button>

    <ul>
      {numbers.map(num => <li>{num}</li>)}
    </ul>
    </>
  )
}

export default App
