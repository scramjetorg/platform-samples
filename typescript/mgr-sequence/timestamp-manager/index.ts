/* eslint-disable no-loop-func */
import { AppConfig, AppContext } from "@scramjet/types";
import { PassThrough, Readable } from "stream";

const rht = require("./real-hrtime.node");

// Default configuration values
let CONFIG = {
    tsPerInstance: 1000,
    tsInterval: 100,
    instancesCount: 5
};

/**
 * This Sequence finds the Sequence with the name '@scramjet/timestamp-producer' on the Sequence list and starts it multiple times.
 * Each Instance of the '@scramjet/timestamp-producer' Sequence will send a 'start' event, triggering the data flow. The Instances will write
 * timestamps to the output stream based on the provided number and interval arguments.
 * The Sequence reads the output from each Instance, calculates the time differences, and returns the overall average to the output stream.
 *
 * @param {AppContext} this - Application context
 * @param {any}_stream - A dummy input stream
 * @param {number} instancesCount - The number of instances to start
 * @param {number} tsPerInstance - The number of timestamps to be sent to the output
 * @param {number} tsInterval - The interval at which the timestamps are sent
 * @returns {PassThrough} A PassThrough stream containing the overall average
 */

export default [
    async function (this: AppContext<AppConfig, any>, _stream: any, instancesCount: number, tsPerInstance: number, tsInterval: number) {
        // Wait for 5 seconds
        await new Promise((res) => setTimeout(res, 5000));

        // Update the configuration values if provided, otherwise use default values
        CONFIG.instancesCount ??= instancesCount;
        CONFIG.tsInterval ??= tsInterval;
        CONFIG.tsPerInstance ??= tsPerInstance;

        // Retrieve the Sequence ID by its name and create Sequence client
        const sequenceName = "@scramjet/timestamp-producer";
        const hostClient = this.hub!;
        const seqList = await hostClient.listSequences();
        const producerSequence = seqList.find((seq) => seq.config.name === sequenceName);
        const seqClient = hostClient.getSequenceClient(producerSequence!.id);

        // Start multiple instances of the sequence with specified arguments in CONFIG
        const instances = await Promise.all(
            new Array(CONFIG.instancesCount).fill(null)
                .map((_e, i) => {
                    return new Promise((res) => setTimeout(res, i * 1000))
                        .then(__ => seqClient.start({ args: [CONFIG.tsPerInstance, CONFIG.tsInterval], appConfig: {} }));
                })
        );

        // Get the "output" stream from each instance
        const outputs = await Promise.all(
            instances.map((instanceClient, i) =>
                new Promise((res) => setTimeout(res, i * 16))
                    .then(() => instanceClient.getStream("output")
                )
            )
        ) as Readable[];

        // Send "start" event to each instance
        instances.forEach(async (ic, i) => {
            await new Promise((res) => setTimeout(res, i * 8))
            ic.sendEvent("start", "");
        });

        // Calculate the differences between timestamps received from instances and the local timestamps
        const outputDiffs = await Promise.all(outputs.map((o, i) =>
            new Promise<bigint[]>(res => {
                const diffs: BigInt[] = [];  // Array to store the differences between timestamps

                // Event-based processing of data from the output stream
                o.on("data", (d) => {
                    const rx = d.toString().replace("\n", ""); // Convert received data to string and remove "\n"

                    // If end indicator received, resolve with the differences array
                    if (rx === "0") {
                        res(diffs as bigint[]);
                        return;
                    }

                    const rxTs = BigInt(rx);  // Convert received timestamp to BigInt
                    const ts = rht.bigint() as bigint;  // Get local timestamp using rht module

                    diffs.push((ts - rxTs) as bigint);  // Calculate difference and push it in the diffs array
                });
            })
        ));

        // Calculate the average difference for each output
        const outputDiffsAvg = outputDiffs.map((d: bigint[]) => d.reduce((partialSum: bigint, a: bigint) => partialSum + a, BigInt(0)) / BigInt(d.length));

        console.log("Channel averages (nanoseconds):");
        console.table(outputDiffsAvg.map(a => Number(a).toFixed(0).toString().padStart(10, " ")));

        // Calculate the overall average difference in nanoseconds
        const avg = outputDiffsAvg.reduce((partialSum: bigint, a: bigint) => partialSum + a, BigInt(0)) / BigInt(outputDiffsAvg.length);
        console.log(`Average from ${CONFIG.instancesCount} output streams:`, Number(avg), "(nanoseconds)");

        // Calculate the ultimate average in milliseconds
        const ultimateAvg = (Number(avg) / 1000000 / 2).toFixed(4);
        console.log(`Average of ${outputDiffsAvg.length} averages:`, ultimateAvg, "(milliseconds)\n");

        // Create a new PassThrough stream and write the overall average in ms
        const ps = new PassThrough({ encoding: "utf-8" });
        ps.write(ultimateAvg.toString()+ "\n");

        return ps;
    }
];
