/* eslint-disable no-console */
import axios, { AxiosInstance } from "axios";
import { defer } from "@scramjet/utility";
import { readFile } from "fs";
import path from "path";
import { ObjLogger } from "@scramjet/obj-logger";
import { Readable } from "stream";


export class Assembly {
    //path to file change song.wav to name of your file
    //file has to be in a same directory
    file = path.join(__dirname, "song.wav");
    logger = new ObjLogger("Assembly");
    fileUrl: string = "";
    transciptId: string = "";
    client: AxiosInstance;
    constructor(token:string) {
        this.client = axios.create({
            baseURL: "https://api.assemblyai.com/v2",
            headers: {
                authorization: token,
                "transfer-encoding": "chunked",
                "content-type" : "application/octet-stream"
            },
        });
    }
    private async uploadFromFs(): Promise<void> {
        return new Promise((resolve, reject) => {
            readFile(this.file, async (err, data) => {
                if (err) reject(err);
                await this.client
                    .post("/upload", data)
                    .then((res) => {
                        this.fileUrl = res.data.upload_url;
                        this.logger.info("succesfully uploaded");
                        this.logger.info("upload URL", this.fileUrl);

                        resolve();
                    })
                    .catch((error) => this.logger.error("got axios error:", error));
            });
        });
    }
    private async startTranscript():Promise<void> {
        await this.client
            .post("/transcript", {
                audio_url: this.fileUrl
            })
            .then((res) => { this.transciptId = res.data.id; });
    }
    private async upload(inputStream: Readable): Promise<void> {
        return this.client
            .post("/upload", inputStream)
            .then((res) => {
                this.fileUrl = res.data.upload_url;

                this.logger.info("succesfully uploaded");
                this.logger.info("upload URL", this.fileUrl);
            })
            .catch((error) => this.logger.error(error));
    }
    private async transcript(): Promise<string> {
        const result = await this.client
            .get<{ status?: string, error?: string, text?: string }>(`/transcript/${this.transciptId}`)
            .then((res) => {
                if (res.data.status === "error") {
                    this.logger.info("Got error from API", res.data.error);
                }

                return res.data;
            });

        if (result.status !== "completed") {
            this.logger.info(result.status);
            await defer(3000);

            return this.transcript();
        }

        return result.text;
    }
    async processFileFs(): Promise<string> {
        await this.uploadFromFs();

        await this.startTranscript();
        return this.transcript();
    }
    async processFile(inputStream: Readable): Promise<string> {
        await this.upload(inputStream);
        await this.startTranscript();

        return this.transcript();
    }
}

