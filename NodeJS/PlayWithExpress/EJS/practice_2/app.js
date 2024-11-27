const express = require('express');
const app = express();
const path = require('path');

app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, '/views'))
app.get('/rand',(req,res)=>{
    const randNumGen = Math.floor(Math.random()*1000)+1
    res.render('random',{randNum : randNumGen})
})
app.get('/r/:sub',(req,res)=>{
    const {sub} = req.params;
    res.render('index',{sub:sub})
})

app.get('/cats',(req,res)=>{
    const cats = ['Blue','Rocket','Monty','Stephanie','Winston','Tom']
    res.render('cats',{cats})
})

app.listen(3000,()=> console.log("App is running on Port 3000"))