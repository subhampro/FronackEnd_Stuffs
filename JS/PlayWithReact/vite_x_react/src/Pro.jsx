export default function Pro() {
    const randNum = Math.floor(Math.random() * 1025 + 1)
    return (
        <>
            <h1 className="PokeHeading">Its Pokemon No : {randNum} </h1>

            <img id="imgID" src={`https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/${randNum}.png`} alt={`Pokemon ${randNum} Not Found!`} />
        </>
    )
}