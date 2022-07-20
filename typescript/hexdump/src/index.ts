import { PassThrough } from "stream";

const app = async function (input) {
    const outputStream = new PassThrough({ encoding: "hex" });
    input.on("data", data => {
        this.logger.debug(`--> Output data: ${data}`);
        outputStream.write(data);
    }
    );
    return outputStream;
};

export default app;
