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
 *
 * @param jsonUrl - a url API address
 */
function jsonPathToValue(jsonData, path) {
    if (!(jsonData instanceof Object) || typeof (path) === "undefined") {
        throw "InvalidArgumentException(jsonData:" + jsonData + ", path:" + path
    };
    path = path.replace(/\[(\w+)\]/g, '.$1');
    
    const pathArray = path.split('.');

    for (let i = 0, n = pathArray.length; i < n; ++i) {
        const key = pathArray[i];
        if (key in jsonData) {
            if (jsonData[key] !== null) {
                jsonData = jsonData[key];
            } else {
                return null;
            }
        } else {
            return key;
        }
    }
    return jsonData;
}

/**
 * The getJsonFromAPI() function is to send a request to API.
 * Writes to stdout a value of indicated element in the json structure.
 *
 * @param jsonUrl - a url API address
 * @param path - a json path to the element that value we want to get
 */
async function printJsonFromAPI(jsonUrl, path) {
    const url = new URL(jsonUrl);
    https.get(url, async function(res){
        res.on("error", (e) => console.error(e));

        try {
            res.setEncoding("utf-8");
            
            let chunks = "";
            for await (const chunk of res)
            chunks += chunk;
            
            const json = JSON.parse(chunks);
            console.log(jsonPathToValue(json, path));
        } catch (e) {
            console.error(e);
        }
    })
};

module.exports = { wait, printJsonFromAPI }
