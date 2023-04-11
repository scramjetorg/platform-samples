/* eslint-disable no-console */
import { ClockifyEntryBuilder } from "./utils/clockifyEntryBuilder";
import { ReadableApp } from "@scramjet/types";

const app: ReadableApp<string> = async function(_stream, interval:number = 1000 * 60 * 60 * 24) {
    this.logger.info("starting instance which adds clockify entry daily");
    const entryBuilder = new ClockifyEntryBuilder();

    entryBuilder.setDate(new Date());
    await entryBuilder.sendRequest()
        .then((res) => this.logger.info(res));

    setInterval(async () => {
        entryBuilder.setDate(new Date());
        await entryBuilder.sendRequest()
            .then((res) => this.logger.info(res));
    }, interval);

    return new Promise((_res, _rej) => { });
};

export default app;
