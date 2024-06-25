const http = require('http');

module.exports = [
    { requires: "inputs", contentType: "application/x-ndjson" },
    async function (input) {
        let data = null;

        const server = http.createServer((req, res) => {
            res.setHeader('Content-Type', 'application/json');
            res.end(JSON.stringify({ greet: 'Hello World', data }));
        });

        server.listen(9080, () => {
            console.log('Server is listening on port 9080');
        });

        for await (const message of input) {
            data = message;
        }

        await new Promise((res, rej) => {
            server.on('close', res);
            server.on('error', rej);
        });
    }
];
