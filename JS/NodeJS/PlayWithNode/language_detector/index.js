import {franc, francAll} from 'franc';
const userInput = process.argv.slice(2);
const langCode = franc(...userInput)
import langs from 'langs';
import colors from 'colors';

const langObj = langs.where("3", langCode);

if (langCode === 'und') {
    console.log('Unsupported language! Please try again with Larger Sentence!'.red);
} else {
    console.log(langObj.name.green);
}

//Code Debug Mode

// const test = franc('Alle menslike wesens word vry')
// console.log(test);
// console.log(...userInput);
// const la = langs.all();
// console.log(la);
// console.log(langCode);