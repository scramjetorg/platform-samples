const { wait, getJsonFromAPI } = require("./utils");

/**
 * Requests external API every x seconds.
 * Returns a json and writes it to stdout stream.
 *
 * @param _stream - dummy input stream
 * @param jsonUrl - json url address
 * @param interval - how often to send a request
 */
module.exports = async function* app (_stream, jsonUrl, interval) {
    try {
        while (true) {
            yield await getJsonFromAPI(jsonUrl);
            await wait(+interval);
        }
    } catch (e) {
            console.error(e);
        }
};
