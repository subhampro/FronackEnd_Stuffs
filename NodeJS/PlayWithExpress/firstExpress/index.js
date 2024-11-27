const express = require('express');
const app = express();
const port = 3000;

// app.use((req,res)=>{
//     res.send("Welcome BC to Homepage!!")
//     console.dir("Someone Send the Request!");
// })

app.get('/',(req,res)=>{
    res.send("Welcome BC to Homepage!!")
    console.dir("Someone Send the Request!");
})
app.get('/gym',(req,res)=>{
    res.send("Welcome BC to Gym!")
    console.dir("Someone Send the Request To Gym!");
})

app.get('/gay',(req,res)=>{
    res.send("You are GAY ! Noob.... Just Die....")
    console.dir("Someone Send the Request!");
})

app.get('/gandu/:subUrl',(req,res)=>{
    res.send("You are GAY ! Noob.... Just Die....", ...(req.params.subUrl).toUpperCase())
    console.dir("Someone Send the Request!");
})

app.get('/:sub/:subId',(req,res)=>{
    let {sub , subId } = req.params;
    res.send(`Hello ! Its Subreddit of ${sub} with an ID ${subId}`);
})

app.get('/search',(req,res)=>{
    // res.send(`Please add Query String On Url to Get Proper Request On postman !`)
    // console.log(req.query)
    const {color , nud , fek} = req.query;
    if(color && nud && fek){
    res.send(`You are searching for Color: ${color}, Nud Quality: ${nud}, Feking: ${fek}`)
    } else if(color && nud){
        res.send(`You are searching for Color: ${color}, Nud Quality: ${nud}`)
    } else if(color && fek){
        res.send(`You are searching for Color: ${color} Feking: ${fek}`)
    } else if(nud && fek){
        res.send(`You are searching for Nud Quality: ${nud}, Feking: ${fek}`)
    } else if(nud && fek){
        res.send(`You are searching for Nud Quality: ${nud}, Feking: ${fek}`)
    } else if (color && !nud && !fek){
        res.send(`You are searching for Color: ${color}`)
    } else if (!color && nud && !fek){
        res.send(`You are searching for Nud Quality: ${nud}`)
    } else if (!color && !nud && fek){
        res.send(`You are searching for Feking: ${fek}`)
    } else {
        res.send("<h1>If Nothing Search ! Nothing Found XD !</h1><hr><h2>Please add Query String On Url to Get Proper Request</h2>")
    }
})
app.get('*',(req,res)=> {
    res.send("<h1>ERROR 404 PAGE NOT FOUND</h1>")
})

app.post('/test',(req,res)=> {
    res.send({
        post1 : "Archite",
        post2 : "Test 2",
        post3 : "Yes Postman working fine!"
    })
})
app.post('*',(req,res)=> {
    res.send("<h1>ERROR 404 PAGE NOT FOUND</h1>")
})


app.listen(port,()=>console.log("App lisening on port no : 3000"))



