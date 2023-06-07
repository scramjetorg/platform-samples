import { ReadableApp } from "@scramjet/types";
import { Assembly } from "./utils/assembly";

const app: ReadableApp<any> = async function(
    _stream,
    token:string
    ) {
    const assembly = new Assembly(token);

    await assembly.processFile();

    return Promise.resolve("finished");
};

export default app;
