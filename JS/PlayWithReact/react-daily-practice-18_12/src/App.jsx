import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import NonStringProps from './NonStringProps'

function App() {
  return   <NonStringProps count={[1,2,3,4,5]} />
}

export default App;
