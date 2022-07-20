const https = require("https");
const { wait, jsonPathToValue, printJsonFromAPI } = require("./utils");

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
 * It returns a promise with the result.
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

module.exports = { wait, getJsonFromAPI }
