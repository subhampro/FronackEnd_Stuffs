export default function RenderArrWidMap({arr}) {
    return <>
        <h2>Rendaring Whole Array !
            So the test array is :   {arr}

<h3>Now The List of array is here !</h3>
            <ul>
{arr.map((num)=><li>Array Item No. {num}</li>)}

            </ul>
        </h2>
    </>
}