import { ReadableApp } from "@scramjet/types";
import { Assembly } from "./utils/assembly";

const app: ReadableApp<any> = async function(
    _stream,
    token:string
    ) {
    const assembly = new Assembly(token);

    assembly.logger.outputLogStream.pipe(this.logger.inputLogStream);

    return assembly.processFileFs().then(res => {
        this.logger.info("Result", res);

        return res;
    });
};

export default app;
