import https from "https";

async function wait(timeInMs) {
    await new Promise(res => setTimeout(res, timeInMs));
}

async function getPageFromAPI(apiKey) {
        this.apiKey = apiKey;
        const options = {
            method: "GET",
            hostname: "tasty.p.rapidapi.com",
            port: null,
            path: "/recipes/auto-complete?prefix=chicken%20soup",
            headers: {
                "X-RapidAPI-Key": `${apiKey}`,
                "X-RapidAPI-Host": "tasty.p.rapidapi.com",
                useQueryString: true
            }
        };

        const req = https.request(options, function(res) {
            let chunks = "";

            res.on("data", function(chunk) {
                chunks += chunk;
            });

            res.on("end", function() {
                const json = JSON.parse(chunks);
                console.log(json);
            });
        });

        req.on("error", (e) => {
            console.error(e);
        });

        req.end();
};

async function app (_stream, apiKey) {
    while (true) {
        await getPageFromAPI(apiKey);
        await wait(5000);
    }
};

export default app;
