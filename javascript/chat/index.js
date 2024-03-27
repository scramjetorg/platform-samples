const { createServer } = require("@scramjet/api-server");


/** @type {import("@scramjet/types").ReadableApp} */
module.exports = [
	{ requires: "chat-input" },
	/** @this {import("@scramjet/types").AppContext} */
	async function* (input, queueSize = "1000") {
		this.logger.info("Starting chat server...");

		const api = createServer();
		const messages = [];
		const output = Object.assign(new DataStream(), { contentType: "text/x-ndjson" });

		input.on("data", (data) => {
			messages.unshift({timestamp: Date.now(), data});
			if (messages.length > queueSize) {
				messages.length = queueSize;
			}
		});

		api.get("/input", (req) => {
			if (req.query.since) {
				const since = +new Date(req.query.since);
				const filtered = messages.filter((msg) => msg.timestamp > since);
				return filtered.map((msg) => msg.data);
			}
            return messages.map((msg) => msg.data);
		});
		api.op("POST", "/output", (req) => {
            output.write(messages[0]);
		});
		api.server.listen(1234);

		return output;
	}
]
