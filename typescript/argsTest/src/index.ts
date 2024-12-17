import { PassThrough } from "stream";

const app = async function (input, argNumber, argObject, argString) {
    const outputStream = new PassThrough();
    input.pipe(outputStream);

    this.logger.debug(`argNumber: ${argNumber}`);
    this.logger.debug(`argObject: ${JSON.stringify(argObject)}`);
    this.logger.debug(`argString: ${argString}`);
    return outputStream;
};

export default app;
