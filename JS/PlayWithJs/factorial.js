const num = prompt("Enter a number:");
let count = 1;

for(let i = parseInt(num); i >= 1 ; i --){
    count *= i
}
console.log(count);

let countArr = [1,2,3,4,5].reduce((a,b)=>a*b ,1)
console.log(countArr)