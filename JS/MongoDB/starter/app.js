const mongoose = require('mongoose');
mongoose.connect('mongodb://127.0.0.1:27017/test');

//           C

const playerSchema = new mongoose.Schema({
    name: String,
    age: Number,
    sex: String
});

const playerModel = mongoose.model('playerModel',playerSchema);
// function getRandomAge(min, max) {
//     return Math.floor(Math.random() * (max - min + 1)) + min;
// }

// function getRandomSex() {
//     return Math.random() < 0.5 ? 'M' : 'F';
// }
// const player = playerModel.insertMany([
//     { name: 'Zara', age: getRandomAge(1, 100), sex: getRandomSex() },
//     { name: 'Liam', age: getRandomAge(1, 100), sex: getRandomSex() },
//     { name: 'Aisha', age: getRandomAge(1, 100), sex: getRandomSex() },
//     { name: 'Kai', age: getRandomAge(1, 100), sex: getRandomSex() },
//     { name: 'Nora', age: getRandomAge(1, 100), sex: getRandomSex() },
//     { name: 'Finn', age: getRandomAge(1, 100), sex: getRandomSex() },
//     { name: 'Yuki', age: getRandomAge(1, 100), sex: getRandomSex() },
//     { name: 'Omar', age: getRandomAge(1, 100), sex: getRandomSex() },
//     { name: 'Ava', age: getRandomAge(1, 100), sex: getRandomSex() },
//     { name: 'Leo', age: getRandomAge(1, 100), sex: getRandomSex() }
// ]).then(res =>console.log('Players inserted successfully:',res))


//              R 

// const playerFound = playerModel.find({age : {$gte : 26}}).then(res => console.log(res));
// const playerFound2 = playerModel.findById({age : {$gt : 69 }}).then(res => console.log(res));
const playerById = playerModel.findById('6749865e67ceb07d4b7d7b11').then(e=>console.log(e));
