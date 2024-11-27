let input = prompt("What would you like to do ?");
let todos = ["help","me","please","sir"];
let index = 0;
let splice = [];
while(input.toLowerCase() !== "quit" && input.toLowerCase() !== "q") {

	if(input.toLowerCase() === "new"){
		todos.push(prompt("Enter New Todo!"));
		console.log(`New Todo Added Here is a updated Todo List array ${todos}`)
	} else if(input.toLowerCase() === "list"){
			console.log("**********")
			for (let i = 0; i < todos.length; i++){
				console.log(`${i}: ${todos[i]}`);
			}
			console.log("**********")

	} else if(input.toLowerCase() === "delete"){
			index = parseInt(prompt("Please Enter the Correct Number to Delete Todos!"));
				splice = todos[index];
				todos.splice(index,1);
				console.log(`Congratulations The Todo on Index: ${index} is Deleted! The ToDo Was: ${splice}`);
	}

		input = prompt("What would you like to do ?");
}

if (input.toLowerCase() === "list" || input.toLowerCase() === "new" || input.toLowerCase() === "delete"){
	console.log("Operation Sucessful.");
	}	else if(input.toLowerCase() === "quit" || input.toLowerCase() === "q"){
			console.log("Ok! You Turned Off the Application.");
	} 	else {console.log("Invalid Input Please Refresh the Page And Try Again!");}