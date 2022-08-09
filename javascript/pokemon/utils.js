const fetch = require("node-fetch");

/**
 * Get pokemon data from API
 * 
 * @param {String} pokemon - pokemon name
 * @returns {Object} - pokemon data
 */
async function loadPokemon(pokemon) {
    try {
        const res = await fetch(`https://pokeapi.co/api/v2/pokemon/${pokemon}`);
        const data = await res.json();
        return data;
    } catch (e) {
        console.log(e);
        return { error: true }
    }
}

module.exports = { loadPokemon };

