export default function Game(){
    let randNum = Math.floor(Math.random() * 6) + 1;
    let randNum2 = Math.floor(Math.random() * 6) + 1;
    let styles = {color: randNum === randNum2 ? "green" : "red"}

    return <>
    <h1>Dice Game</h1>
    <div style={styles}>
    { randNum === randNum2 ? <h1>Player Win</h1> : <h1>Computer Win</h1>  }
    <h2>Player 1 Dice Number : {randNum} </h2>
    <h2>Player 2 Dice Number : {randNum2} </h2>

    </div>
    </>
}