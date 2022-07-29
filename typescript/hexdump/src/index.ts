import { PassThrough } from "stream";

const app = async function (input) {
    const outputStream = new PassThrough({ encoding: "hex" });
    input.pipe(outputStream);
    return outputStream;
};

export default app;
