var figlet = require("figlet");
var colors = require('colors');

figlet("I Am SubhaM the Greatest !", function (err, data) {
  if (err) {
    console.log("Something went wrong...");
    console.dir(err);
    return;
  }
  console.log(data.rainbow);
});

//Normal Ver.
figlet("I Am SubhaM the Greatest !", function (err, data) {
  if (err) {
    console.log("Something went wrong...");
    console.dir(err);
    return;
  }
  console.log(data);
});
