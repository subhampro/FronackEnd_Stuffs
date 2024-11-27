let frstInc = prompt("Enter the first Number:");
let scndInc = prompt("Enter the second Number:");
let oporators = prompt("Enter the operator (+, -, *, /):");
let randomNum = Math.ceil(Math.random() * 100);
console.log("Random Number:", randomNum);

if (  randomNum < 90 ){
    if (oporators === "+") {
        console.log(parseInt(frstInc) + parseInt(scndInc));
    } else if (oporators === "-") {
        console.log(parseInt(frstInc) - parseInt(scndInc));
    } else if (oporators === "*") {
        console.log(parseInt(frstInc) * parseInt(scndInc));
    } else if (oporators === "/") {
        console.log(parseInt(frstInc) / parseInt(scndInc));
    }
} else {
    if (oporators === "+") {
        console.log(parseInt(frstInc) - parseInt(scndInc));
    } else if (oporators === "-") {
        console.log(parseInt(frstInc) / parseInt(scndInc));
    } else if (oporators === "*") {
        console.log(parseInt(frstInc) + parseInt(scndInc));
    } else if (oporators === "/") {
        console.log(parseInt(frstInc) ** parseInt(scndInc));
    }
}