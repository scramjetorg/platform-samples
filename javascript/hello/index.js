const rl = require("readline");

module.exports = async function* (input) {
    for await (const line of new rl.Interface(input)) {
        yield `Hello ${line}!`;
    }
};
