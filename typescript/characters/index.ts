/* eslint-disable no-console */
import { TransformApp } from "@scramjet/types";
import { PassThrough, Stream, Transform } from "stream";
import { createDb } from "./lib/db";
import { decide, listToObject } from "./lib/util";

module.exports = async function (input: Stream, arg1: string, arg2: string, arg3: string, arg4?: string) {
    const output = new PassThrough();

    this.on("create-db", async () => {
        await createDb();
        output.write("Db created");
    });
    this.on("list-to-object", async () => {
        await listToObject();
        output.write("Changed list to object");
    });
    input
        .pipe(
            new Transform({
                encoding: "utf-8",
                async transform(chunk, _encoding, callback) {
                    const dec = await decide(chunk, arg1, arg2, arg3, arg4);

                    callback(null, dec);
                },
            })
        )
        .pipe(output);
    return output;
} as TransformApp<any>;
