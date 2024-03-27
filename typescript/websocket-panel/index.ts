import { ReadableApp, Middleware } from "@scramjet/types";
import { createServer as apiServer } from "@scramjet/api-server";
import { staticContent } from "./static-content";
import { WebSocketServer, WebSocket } from "ws";
import { createServer } from "http";
import { DataStream } from "scramjet";

const port = 9080;

const corsMiddleware: Middleware = (req, res, next) => {
    res.setHeader("Access-Control-Allow-Origin", "*");
    res.setHeader("Access-Control-Allow-Methods", "DELETE, POST, GET, OPTIONS, PUT, PATCH");
    res.setHeader(
        "Access-Control-Allow-Headers",
        "Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With, X-Force, X-Revoke, x-timeout, x-end-stream, x-name"
    );
    next();
};

const exp: ReadableApp<any, any> = async function (_stream, ...args) {
    const api = apiServer({ server: createServer() });
    const out: DataStream = Object.assign(new DataStream(), { contentType: "text/x-ndjson" });

    const logger = this.logger;

    api.use("*", corsMiddleware);

    api.server.listen(port, "0.0.0.0", () => {
        this.logger.info("Instance server listening on port", port);
    });

    api.use("*", async (req, _res, next) => {
        if (req.method === "GET") {
            req.params ||= {};
        }

        this.logger.info("request", req.method, req.url);
        next();
    });

    api.get("/api/url", async () => {
        return { url: `http://localhost:9080/www/index.html` };
    });

    const wss = new WebSocketServer({ server: api.server });

    const connections: Set<WebSocket> = new Set();

    wss.on('connection', function connection(ws) {
        connections.add(ws);
        logger.info("Websocket connection established.");

        ws.on('message', function message(data, isBinary) {
            if (isBinary) {
                return;
            }

            try {
                const message = JSON.parse(data.toString());

                logger.info("Websocket message received", message);

                out.write(message);
            } catch (e: any) {
                logger.error("Error parsing websocket message", e?.stack, data.toString());
            }
        });

        ws.once('error', (e) => {
            logger.info("Error in websocket connection", e);
            ws.close();
            connections.delete(ws);
        });
        ws.on("close", () => {
            logger.info("Websocket connection closed.");
            connections.delete(ws);
        });
    });

    api.use("/www/:path", staticContent);

    out.on("pause", () => {
        logger.info("Pausing websocket connections");
        connections.forEach(ws => ws.pause())
    });
    out.on("resume", () => {
        logger.info("Resuming websocket connections");
        connections.forEach(ws => ws.resume())
    });

    return out;
};

export default exp;


