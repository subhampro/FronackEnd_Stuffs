const containEr = document.querySelector('#container')



for (let i=100 ; i > 0; i--){
const button = document.createElement('button')
button.textContent = 'Hey!';    
containEr.append(button)
}

function yoo() {
    console.log('Yoo!');
}

function yo() {
    console.log('Yo!');
}

const btn = document.querySelector('#btn');

btn.onclick = () => {
    console.log("Yoo!"); 
    console.log("Yo!");
};

btn.addEventListener('click', yoo)
btn.addEventListener('click', yo)

let btn2 = document.querySelector('#btn');
let titleCon = document.querySelector('#titleCon');

function changeColor(){
    document.body.style.backgroundColor = `rgb(${Math.floor(Math.random()*255 + 1)},${Math.floor(Math.random()*255 + 1)},${Math.floor(Math.random()*255 + 1)})`;
}

function changeH2(){
    titleCon.innerText = document.body.style.backgroundColor;
}

btn2.addEventListener('click',changeColor)
btn2.addEventListener('click',changeH2)

document.querySelector('button:nth-of-type(2)').addEventListener("click",function(evt){console.log(evt)})

document.querySelector('input').addEventListener('keyup',function(cc){console.log(cc)})
document.querySelector('input').addEventListener('keydown',function(ccc){console.log(ccc)})


const form = document.querySelector('#form')
const input = document.querySelector('#input')
const ul = document.querySelector('ul');

form.addEventListener('submit',function(inpu){
    inpu.preventDefault()
    console.log(input.value);
    let newLi = document.createElement('li');
    newLi.innerText = input.value;
    ul.appendChild(newLi);
    input.value = '';
})

// NEW 269 No Video Task Form Events

const form269 = document.querySelector('#form269')
const userName269 = document.querySelector('#username269');
const tweet269 = document.querySelector('#tweet');
const ul269 = document.querySelector('#ul269');

const emptyValues269 = () => {
    userName269.value = '';
    tweet269.value = '';
    }

form269.addEventListener('submit',(stop269) => {

    stop269.preventDefault();

    const finalOutput = document.createElement('li');
    finalOutput.innerHTML = `<b>${userName269.value}-</b> ${tweet269.value}`
    ul269.appendChild(finalOutput);
    
    emptyValues269();
})

//////////////////// NEW 269 No Video Task Form Events CODE EXERCISE ////////////////////////////////




 
















