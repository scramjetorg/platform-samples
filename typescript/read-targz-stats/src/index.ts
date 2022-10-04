import { TransformApp } from "@scramjet/types";
import { PassThrough } from "stream";
import { extract } from "tar-stream";
import { createGunzip } from "zlib";

const app: TransformApp<String> = async function (input) {
    const outputStream = new PassThrough({ encoding: "utf-8" })
    const tarStream = extract()
        .on("entry", (header, stream, next) => {
            const { name, mode, type, uname, gname, size } = header;
            let buf: Buffer[] = [];

            stream.on("data", chunk => buf.push(chunk))
            stream.on("end", () => {
                const fileStats = { name, mode, type, uname, gname, size, data: Buffer.concat(buf) }
                outputStream.write(JSON.stringify(fileStats));
                next();
            })
            stream.resume()
        })
        .on("finish", () => { outputStream.end(); })
    const unzipStream = createGunzip()

    input.pipe(unzipStream);
    unzipStream.pipe(tarStream);

    return outputStream;
};

export default app;
