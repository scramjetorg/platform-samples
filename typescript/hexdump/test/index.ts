import { createReadStream } from "fs";
import app from "../src";

async function runTest() {
    const context = {
        logger: {
            debug: console.log,
            error: console.error,
        }
    }

    const readFile = createReadStream("scramjet.ico");
    const read = app.bind(context);
    (await read(readFile)).on("data", chunk => console.log(chunk));
}

runTest();
