const rl = require("readline");
const { Readable } = require("stream");

module.exports = async function* (input) {
    for await (const line of new rl.Interface(input)) {
        yield `Hello ${line}!`;
    }
};
