const dogs = require('./dog')
const cats = require('./cat')
const allPets = [dogs , cats];
const multi = (x,y) => x*y;
module.exports = allPets;
module.exports = {
    multi: multi,
}