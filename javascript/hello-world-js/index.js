const { PassThrough } = require("stream");

module.exports = async function(_input) {
    // create a clean output stream
    const out = new PassThrough({ encoding: "utf-8" });

    // write some data to the output stream
    out.write("Hello World!");

    // return the output stream so it can be consumed (e.g. by CLI client)
    return out;
};
