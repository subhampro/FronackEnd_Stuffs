const changeColor = (color,delay) => {
	return new Promise((accept,reject)=>{
		setTimeout(()=>{
			document.body.style.backgroundColor = color;
					accept();
			},delay)
	})
}

changeColor('red',2000)
// .then(() => changeColor('green',3000))
// .then(() => changeColor('blue',3000))
// .then(() => changeColor('orange',3000))
// .then(() => changeColor('pink',3000))
// .then(() => changeColor('black',3000))

.then(() => changeColor('green',3000)
		.then(() => changeColor('blue',3000)
			.then(() => changeColor('orange',3000)
				.then(() => changeColor('pink',3000)
					.then(() => changeColor('black',3000)
	)))))	