import { ReadableApp } from "@scramjet/types";
import { Assembly } from "../../audio2text/src/utils/assembly";
import { Readable } from "stream";

const app: ReadableApp<any> = async function(input: Readable, apiKey: string) {
    const assembly = new Assembly(apiKey);

    assembly.logger.outputLogStream.pipe(this.logger.inputLogStream);

    return assembly.processFile(input).then(res => {
        this.logger.info("Result", res);

        return res;
    });
};

export default app;
