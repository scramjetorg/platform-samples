const util = require("./utils")

/**
 * Requests external API every x seconds.
 * Returns a json element and writes it to stdout stream.
 *
 * @param _stream - dummy input stream
 * @param jsonUrl - json url address
 * @param interval - how often to send a request
 * @param jsonPath - a json path to a desired element in the json structure
 */
module.exports = async function app (_stream, jsonUrl, interval, jsonPath) {
    try {
        while (true) {
            await util.getJsonFromAPI(jsonUrl, jsonPath);
            await util.wait(+interval);
        }
    } catch (e) {
        console.error(e);
    }
};
