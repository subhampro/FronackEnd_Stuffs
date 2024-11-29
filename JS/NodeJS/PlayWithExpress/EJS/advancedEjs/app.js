const express = require('express');
const path = require('path');
const app = express(); 
const redditData = require('./data.json');
const bootstrap = require('bootstrap');

app.use(express.static(path.join(__dirname,'public')))

app.set('views', path.join(__dirname, '/views'));
app.set('view engine', 'ejs');


app.listen(3000,()=> console.log("App Listening on Port : 3000"))
app.get('/r/:subreddit', (req,res)=>{
    const {subreddit} = req.params;
    // const data = redditData.soccer;
    const data = redditData[subreddit];
    console.log(data) 
    res.render('subnreddit',{data})
})