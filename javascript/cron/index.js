const noop = () => {};

const timer = (async function*(getNext) {
    while (true) {
        try {
            await getNext();
        } catch (error) {
            // Handle any errors from the external event
        }
        yield;
    }
});

/**
 * @typedef {{interval?: number,  sequence: string, ruleNumber?: number, args: any[]}} CronRule
 * @type {import("@scramjet/types").WritableApp<
 *   CronRule,
 *   [number, ...any[]],
 *   any,
 *   {rules: CronRule[]},
 * >}
 */
module.exports = async function(input, tick = 1000) {
    /** @type {NodeJS.Timer | null} */
    let next = null;

    const rules = this.config.rules;
    const interrupt = noop;

    const getNext = async () => {
        return Promise.race([new Promise((resolve) => {
            next = setTimeout(() => {
                next = null;
                resolve();
            }, tick);
        }), new Promise((resolve) => {
            interrupt = resolve;
        })]);
    };

    for await (let _dummy of timer(getNext)) {

    }
};
