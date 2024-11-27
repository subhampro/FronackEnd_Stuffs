let express = require('express');
let app = express();
let PORT = 3000;

app.set('view engine', 'ejs')

app.listen(PORT,()=> {
	console.log("Running Server At http://localhost:3000")
})

app.get('/',(req,res)=>{
	console.log(req.perms);
	const name = {first: 'Subham' , last: 'Das'}
	const tests = ['one','two','three','four','five','six','seven']
	res.render('index',{ name , tests })
})

app.get('/:newParams',(req,res)=>{
console.log(req.params);
	const {newParams} = req.params;
		console.log(newParams);
	const name = {first: 'Subham' , last: 'Das'}
	const tests = ['one','two','three','four','five','six','seven']
	res.render('index',{ name , tests })
})