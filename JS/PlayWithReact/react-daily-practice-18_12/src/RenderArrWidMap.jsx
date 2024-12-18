export default function RenderArrWidMap({arr}) {
    const num = Math.floor(Math.random()*1000); // Random Number for Key
    return <>
        <h2>Rendaring Whole Array !</h2>
            So the test array is :   {arr}

<h3>Now The List of array is here !</h3>
            <ul>
{arr.map((num)=><li key={num}>Array Item No. {num}</li>)}

            </ul>
        
    </>
}