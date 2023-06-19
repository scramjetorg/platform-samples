import { ReadableApp } from "@scramjet/types";
import { Assembly } from "../../audio2text/src/utils/assembly";
import { PassThrough } from "stream";

const app: ReadableApp<any> = async function(input, apiKey: string) {
    const assembly = new Assembly(apiKey);
    const output = new PassThrough({ defaultEncoding:"utf-8" });
    
    assembly.logger.outputLogStream.pipe(this.logger.inputLogStream);

    let timer;
    let helpStream: PassThrough = new PassThrough();

    async function transcript() {
        helpStream.end();
        await assembly.processFile(helpStream).then(res => {
            this.logger.info("Result", res);
            helpStream = new PassThrough();
            output.push(res);
        });
    }
    function startTimer() {
        timer = setTimeout(() => {
            transcript();
        }, 2000);
    }

    input.on("data", (chunk) => {
        if(!timer) {
            startTimer();
        }
        helpStream.push(chunk);
        clearTimeout(timer);
        startTimer();
    });
    this.on("pause", () => {
        input.pause();
    });
    this.on("resume", () => {
        input.resume();
    });
    return output;
};

export default app;
