export default function Conditionals({condition}) {
    const num1 = Math.floor(Math.random() * 5);
    const num2 = Math.floor(Math.random() * 5);
    return  <>
        {num1 === num2 ? <h1>Condition Passed</h1> : <h1>Condition Failed</h1>}
    </>
}