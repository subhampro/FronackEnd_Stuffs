export default function Game(){
    let randNum = Math.floor(Math.random() * 6) + 1;
    let randNum2 = Math.floor(Math.random() * 6) + 1;
    return <>
    <h1>Dice Game</h1>
    <h2>Player 1 Dice Numver : {randNum} </h2>
    <h2>Player 2 Dice Numver : {randNum2} </h2>

    { randNum === randNum2 ? <h3>Player Win</h3> : <h3>Computer Win</h3>  }
    </>
}