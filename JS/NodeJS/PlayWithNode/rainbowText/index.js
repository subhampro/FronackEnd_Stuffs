var giveMeAJoke = require('give-me-a-joke');
var colors = require('colors');
const punycode = require('punycode');


giveMeAJoke.getRandomDadJoke (function(joke) {
    return console.log(joke.rainbow);
});