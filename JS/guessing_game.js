let maxNum = parseInt(prompt("Please Enter Maximum Number to Start The Game!"));
console.log("Please Enter Maximum Number to Start The Game!");
console.log(`User Choose ${maxNum} As Maximum Number`);

while(!maxNum){
	maxNum = parseInt(prompt("Please Enter A Valid Number to Start The Game!"));
	console.log("Please Enter A Valid Number to Start The Game!");
console.log(`User Choose ${maxNum} As Maximum Number`);
}

const rand = Math.floor(Math.random()*maxNum + 1);
console.log(`This is the secret Number : ${rand}`);

let guess = prompt("Please Enter Your 1st Number Guess!");



let count = 1;

while (parseInt(guess) !== rand) {

	if (guess === "y") {
		break;
		console.log("Ok ! You Quit That Early Sad :(")
	} else { guess = parseInt(guess)}
		console.log("parseInt(guess) done!")
	if ( guess > rand ) {
		guess = parseInt(prompt("Your Guess is too High Try Smaller Number!"));
		count ++;
		console.log(`Count Increased to :${count}`);
	} else if ( guess < rand ) {
		guess = parseInt(prompt("Your Guess is too Low Try Higher Number!"));
		count ++;
		console.log(`Count Increased to :${count}`);
	} else { guess= parseInt(prompt("Please Enter a Valid Number to continue the Game!")); }
};

if (guess === "y") {
		console.log("Ok ! You Quit That Early Sad :(")
	} else { console.log(`Congratulations You win the game with : ${count} Count Of Guesses`); }