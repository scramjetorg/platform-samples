/* eslint-disable no-loop-func */

import { AppConfig, AppContext } from "@scramjet/types";
import { Readable } from "stream";

const rht = require("./real-hrtime.node");

/**
 * This Sequence is responsible for generating and sending timestamps to the output stream.
 * It listens for the "start" event and, upon receiving it, starts generating timestamps.
 * The Sequence will generate the specified number of timestamps at the given interval and push them to the output stream.
 * After generating the desired number of timestamps, it will push an end indicator to signify the end of data.
 *
 * * @param {AppContext} this - Application context
 * @param {any} _stream - A dummy input stream
 * @param {number} tsQuantity - The number of timestamps to be sent to the output (default: 128)
 * @param {number} delay - The delay between each timestamp generation in milliseconds (default: 100)
 * @returns {Readable} A Readable stream containing the generated timestamps
 */

export default [
    async function (this: AppContext<AppConfig, any>, _stream: any, tsQuantity: number = 128, delay: number = 100) {
        this.logger.info(`Sending ${tsQuantity} timestamps to output`);
        const p = new Readable({ read: () => {}});
        let l = 0;

        // Event listener for the "start" event
        this.on("start", async () => {
            while (l++ < tsQuantity) {
                await new Promise(res => setTimeout(res, delay));

                if (!p.push(`${rht.stringified()}\n`)) {
                    await new Promise(res => p.once("drain", res));
                }
            }

            await new Promise(res => setTimeout(res, 10));

            p.push("0\n");
        });

        return p;
    }
];
