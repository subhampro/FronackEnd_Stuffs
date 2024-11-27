document.querySelector('img').style.width = '25%'
document.querySelector('img:nth-of-type(3)').setAttribute('src','https://upload.wikimedia.org/wikipedia/commons/thumb/2/26/Red_Junglefowl.jpg/1280px-Red_Junglefowl.jpg')

// const allLinks = document.querySelectorAll('a');

// for (let link of allLinks) {
//     link.innerText = 'I AM A LINK!!!!'
// }


// for (let link of allLinks) {
//     link.style.color = 'rgb(0, 108, 134)';
//     link.style.textDecorationColor = 'magenta';
//     link.style.textDecorationStyle = 'wavy'
// }

// document.querySelector('h2').style.color = "red";
// document.querySelector('h2').setAttribute('class','border purple')

// let h2 = document.querySelector('h2')

// h2.setAttribute('class','purple border')

// h2.classList.add('purple')
// h2.classList.add('border')

// document.querySelector('.toctitle').innerHTML = '<h2 class="purple border" id="mw-toc-heading">Contents</h2><span class="toctogglespan"><label class="toctogglelabel" for="toctogglecheckbox"></label></span>'

const imgNew = document.createElement('img')

imgNew.src = 'https://gratisography.com/wp-content/uploads/2024/01/gratisography-cyber-kitty-800x525.jpg'

document.body.appendChild(imgNew)

imgNew.classList.add('square')