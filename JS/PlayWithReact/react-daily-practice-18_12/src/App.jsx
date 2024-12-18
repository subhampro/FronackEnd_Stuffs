import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import NonStringProps from './NonStringProps'
import DefaultPropValue from './DefaultPropValue'
import PassingArrays_Obj from './PassingArrays_Obj'
import Conditionals from './Conditionals'
import DynamicComponentStyle from './DynamicComponentStyle'
import RenderArrWidMap from './RenderArrWidMap'

function App() {
//  return <DynamicComponentStyle />
  return <RenderArrWidMap arr = {[1,2,3,4,5,6,7,8,9,10]}/>
  // return <Conditionals condition={true}/>
  // return <PassingArrays_Obj props={{obj : "value", arr: [1,2,3,4]}}/>
  // return <DefaultPropValue color={"Green"}/>
  // return   <NonStringProps count={[1,2,3,4,5]} />
}

export default App;
