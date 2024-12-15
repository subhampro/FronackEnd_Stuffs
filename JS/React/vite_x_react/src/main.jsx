import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'
import Pro from './Pro.jsx'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <Pro />
  </StrictMode>,
)
