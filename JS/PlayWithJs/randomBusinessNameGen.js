let adj1 = "Crezy";
let adj2 = "Fancy";
let adj3 = "Kudos";
let names1 = "Engine";
let names2 = "Foods";
let names3 = "Garments";
let aw1 = "Bros";
let aw2 = "Limited";
let aw3 = "Hub";

let randomBusinessNamegen = () => {
    let i = Math.floor(Math.random()*3+1);
    let adj = eval('adj'+i);
    let names = eval('names'+i);
    let aw = eval('aw'+i);
    console.log(adj, names, aw)
}

randomBusinessNamegen();