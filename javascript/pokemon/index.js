const { Transform, Stream } = require("stream");
const { loadPokemon } = require("./utils");

/**
 * Sequence that transforms each pokemon name into a pokemon data
 *
 * @param {Stream} input - pokemon name passed as an input stream
 * @returns {String} - pokemon weight on output, pokemon data on stdout
 */
module.exports = async function(input) {
    return input.pipe(new Transform({
        encoding: "utf-8",
        transform: async (chunk, _encoding, callback) => {
            const pokemon = await loadPokemon(chunk);
            console.log(inspect(pokemon, false, 4));
            const weight = pokemon.weight/10;
            callback(null, `${weight.toString()}\n`);
        }
    }));
};
