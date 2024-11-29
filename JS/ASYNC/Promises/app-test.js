const fakeCallBack = (url) => {
	return new Promise ((accept, reject) => {
		const takeRandomNum = Math.ceil(Math.random()*3000)
		console.log(takeRandomNum);
		setTimeout(() => {
			if (takeRandomNum > 500){
			reject('Server Connection Timeout!')} 
			else {accept(`Congratulations you get the data from ${url}`)}
		}, takeRandomNum)
	})
}

fakeCallBack('fakeurl.com')
.then(data => {
	console.log(data);
	console.log('IT WORKED!');
	})

.catch(err => {
	console.log(err);
	console.log('Opps!!');
	})


