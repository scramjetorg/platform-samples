const https = require("https");

/**
 * The wait() function is to delay a function call after the specified number of time.
 *
 * @param timeInMs - time given in milliseconds
 */
async function wait(timeInMs) {
    await new Promise(res => setTimeout(res, timeInMs));
}

/**
 * The getJsonFromAPI() function is to send a request to API.
 * It writes json body to stdout.
 *
 * @param jsonUrl - a url API address
 */
async function getJsonFromAPI(jsonUrl) {
        const url = new URL(jsonUrl.trim());
        const req = https.request(url, function(res) {
            let chunks = "";

            res.on("data", function(chunk) {
                chunks += chunk;
            });

            res.on("end", function() {
                const json = JSON.parse(chunks);
                    // console.log() writes to stdout endpoint
                    console.log(json)
            });
        });

        req.on("error", (e) => {
            console.error(e);
        });

        req.end();
};

/**
 * Requests external API every x seconds.
 * Returns a json and writes it to stdout stream.
 *
 * @param _stream - dummy input stream
 * @param jsonUrl - json url address
 * @param interval - how often to send a request
 */
module.exports = async function app (_stream, jsonUrl, interval) {
    try {
        while (true) {
            await getJsonFromAPI(jsonUrl);
            await wait(+interval);
        }
    } catch (e) {
        console.error(e);
    }
};