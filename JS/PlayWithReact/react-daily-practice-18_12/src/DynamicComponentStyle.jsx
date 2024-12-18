export default function DynamicComponentStyle() {
  const num1 = Math.floor(Math.random() * 3);
  const num2 = Math.floor(Math.random() * 3);
  
  return <>
  <h1 style={{color : num1 === num2 ? "green" : "red"}}>PAGE Connected !</h1>
  </>
  }