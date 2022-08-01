const { wait, printJsonFromAPI } = require("./utils");

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
            await printJsonFromAPI(jsonUrl, jsonPath);
            await wait(+interval);
        }
    } catch (e) {
        console.error(e);
    }
};
