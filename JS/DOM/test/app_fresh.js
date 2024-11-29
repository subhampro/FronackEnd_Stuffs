const h1 = document.querySelector('h1');
const username = document.querySelector('#username');

console.log('Test')

username.addEventListener('input',(e)=>{
    h1.innerText = `Welcome, ${username.value}`
})

const randColor = () => `rgb(${Math.floor(Math.random()*255)+ 1},${Math.floor(Math.random()*255)+ 1},${Math.floor(Math.random()*255)+ 1})`;

const btn1 = document.querySelector('#chnGcOl');
const h2 = document.querySelector('#h2_hain_bhai');
const para = document.querySelector('#paragraph');

btn1.addEventListener('click',(e) => {
    document.body.style.backgroundColor = `${randColor()}`
    e.stopPropagation()
});

h2.addEventListener('click',() => console.log(`${randColor()}`));
para.addEventListener('click',() => para.classList.toggle('disapp'));