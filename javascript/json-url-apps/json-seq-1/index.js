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
    return new Promise((resolve, reject) => {
        const url = new URL(jsonUrl.trim());
        https.request(url, async function(res) {
            try {
                res.setEncoding("utf-8");

                let chunks = "";
                for await (const chunk of res) chunks += chunk;

                resolve(JSON.parse(chunks));
            } catch (e) {
                reject(e);
            }
        })
        .on("error", reject)
        .end();
    });
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
    while (true) {
        try {
            console.log(await getJsonFromAPI(jsonUrl));

            await wait(+interval);
        } catch (e) {
            console.error(e);
        }
    }
};