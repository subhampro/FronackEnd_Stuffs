import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import NonStringProps from './NonStringProps'
import DefaultPropValue from './DefaultPropValue'

function App() {
  return <DefaultPropValue color={"Green"}/>
  // return   <NonStringProps count={[1,2,3,4,5]} />
}

export default App;
