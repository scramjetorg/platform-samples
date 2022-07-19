const https = require("https");

async function wait(timeInMs) {
    await new Promise(res => setTimeout(res, timeInMs));
}

async function getPageFromAPI(jsonUrl) {
        const url = new URL(jsonUrl.trim());
        const req = https.request(url, function(res) {
            let chunks = "";

            res.on("data", function(chunk) {
                chunks += chunk;
            });

            res.on("end", function(path) {
                const json = JSON.parse(chunks);
                json.drinks.forEach(element => {
                    console.log(element.strDrink)
                });
            });
        });

        req.on("error", (e) => {
            console.error(e);
        });

        req.end();
};

module.exports = async function app (_stream, arg1, arg2) {
    try {
        while (true) {
            await getPageFromAPI(arg1);
            await wait(+arg2);
        }
    } catch (e) {
        console.error(e);
    }
};
