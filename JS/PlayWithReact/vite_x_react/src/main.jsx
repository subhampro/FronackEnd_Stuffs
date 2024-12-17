import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'
import Pro from './Pro.jsx'
import Game from './Game.jsx'
import Map from './Map.jsx'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    {/* <App /> */}
    {/* <Pro /> */}
    {/* <Game /> */}
    <Map colorss={["red","green","yellow","blue","white","violet"]}/>
  </StrictMode>,
)
