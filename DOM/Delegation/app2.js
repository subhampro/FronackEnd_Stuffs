const form = document.querySelector("#form");
const ul = document.querySelector("#ul");
const lis = document.querySelectorAll("li"); 

ul.addEventListener('click',(e)=> {   
        e.target.nodeName === "LI" ? e.target.remove() : console.log('Its not an LI!!')
    });

form.addEventListener('submit',(e) => {
e.preventDefault();
const bTag = document.createElement('b');

const finalOutput = `<b>${form.username.value}-</b> ${form.post.value}`;
const lie = document.createElement('li');
lie.innerHTML = finalOutput;

ul.append(lie);
console.log(finalOutput);    
})