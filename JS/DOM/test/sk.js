const button1 = document.querySelector('#button1');
const button2 = document.querySelector('#button2');
const button3 = document.querySelector('#button3');
const team1Score = document.querySelector('#displayScore1');
const team2Score = document.querySelector('#displayScore2');
const select = document.querySelector('#playOptions')

let gameOver = false;
let count = 0;
let countp2 = 0;
let finalScore = 4;

function reset(){
	team1Score.innerText = 0;
	team2Score.innerText = 0;
	count = 0;
	countp2 = 0;
	gameOver = false;
	// team2Score.classList.remove('loose');
	team2Score.classList.remove('win', 'loose');
	team1Score.classList.remove('win', 'loose');
	// team1Score.classList.remove('win');
}

select.addEventListener('change',(e)=>{
	finalScore = parseInt(select.value);
	reset();
})

button1.addEventListener('click',(e)=>{
	if(!gameOver){
			count += 1;
			team1Score.innerText = count;
		if (count === finalScore){
			gameOver = true;
			team1Score.classList.add('win')
			team2Score.classList.add('loose');
			console.log("Game Over ! Player 1 Win!")
			}
		}			
		else {console.log("Game Already Over! Try Reset the Score!")}
})

button2.addEventListener('click',(e)=>{
	if(!gameOver){
			countp2 += 1;
			team2Score.innerText = countp2;
		if (countp2 === finalScore){
			gameOver = true;
			team2Score.classList.add('win');
			team1Score.classList.add('loose');
			console.log("Game Over ! Player 2 Win!")
			}
		}		
		else {console.log("Game Already Over! Try Reset the Score!")}
})

button3.addEventListener('click',reset)