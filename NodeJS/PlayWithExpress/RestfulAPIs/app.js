const express = require('express');
const app = express();
const path = require('path');
const { v4: uuidv4 } = require('uuid');
const methodOverride = require('method-override');

app.set('view engine','ejs')
app.set('views',path.join(__dirname,'views'))
app.use(express.static(path.join(__dirname,'public')))
app.use(express.json())
app.use(express.urlencoded({ extended: true })) 
app.use(methodOverride('_method'));
app.listen(3000,()=>{
    console.log('Listening on Port : 3000')
})

let comments = [
    {
        id: uuidv4(),
        username: 'Todd',
        comment: 'lol that is so funny!'
    },
    {
        id: uuidv4(),
        username: 'Skyler',
        comment: 'I like to go birdwatching with my dog'
    },
    {
        id: uuidv4(),
        username: 'SkerBoi',
        comment: 'Plz delete your account, Tods!'
    },
    {
        id: uuidv4(),
        username: 'Onlysayswoof',
        comment: 'woof woof woof'
    }
]
app.post('/comments',(req,res)=>{
    const id = uuidv4();
    const {username,comment} = req.body;
    if(!username && !comment ){
        return res.status(400).send("Invalid data: 'username' and 'comment' are required.");
    } else {
    comments.push({username,comment,id});
    res.redirect('comments');
}})
app.get('/comments',(req,res)=>{
    res.render('comments',{comments})
})
app.get('/comments/new',(req,res)=>{
    res.render('newComment',{})
})
app.get('/comments/:id',(req,res)=>{
    const {id} = req.params;
    const comment = comments.find( com => com.id === id);
    res.render('detailed',{comment})
})

// app.get('/comments/:id/edit',(req,res)=>{
//     const {id} = req.params;
//     res.render('edit',{id});
// })
app.get('/comments/:id/edit', (req, res) => {
    const { id } = req.params;
    const comment = comments.find(com => com.id === id);
    if (comment) {
        res.render('edit', { id: comment.id });
    } else {
        res.status(404).send('Comment not found');
    }
});

app.patch('/comments/:id',(req,res)=>{
    const {id} = req.params;
    const filteredComment = comments.find(comment => comment.id === id);
    filteredComment.comment = req.body.comment ;
    console.log(filteredComment)
    res.redirect('/comments')
})
app.get('*',(req,res)=>{
    res.redirect('/comments');
})
