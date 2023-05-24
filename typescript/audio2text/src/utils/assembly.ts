/* eslint-disable no-console */
import axios, { AxiosInstance } from "axios";
import { defer } from "@scramjet/utility";
import { readFile } from "fs";
import path from "path";


export class Assembly {
    //path to file change song.wav to name of your file
    //file has to be in a same directory
    file = path.join(__dirname, "song.wav");
    fileUrl:string = "";
    status:string = "";
    transciptId:string = "";
    token:string;
    client:AxiosInstance;
    constructor(token:string) {
        this.token = token;
        this.client = axios.create({
            baseURL: "https://api.assemblyai.com/v2",
            headers: {
                authorization: this.token, //conf.apiKey,
                "transfer-encoding": "chunked",
            },
        });
    }
    private async upload(): Promise<string> {
        return new Promise((resolve, reject) => {
            readFile(this.file, async (err, data) => {
                if (err) reject(err);

                await this.client
                    .post("/upload", data)
                    .then((res) => {
                        this.fileUrl = res.data.upload_url;
                        resolve("succesfully uploaded");
                    })
                    .catch((error) => console.error(error));
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
    private async transcript():Promise<string> {
        return new Promise(async (resolve, _reject) => {
            while (this.status !== "completed") {
                this.client
                    .get(`/transcript/${this.transciptId}`)
                    // eslint-disable-next-line no-loop-func
                    .then((res) => {
                        if (res.data.status === "completed") {
                            resolve(res.data.text);
                        } else {
                            console.log(res.data.status + "...");
                            this.status = res.data.status;
                        }
                    })
                    .catch(console.error);

                await defer(3000);
            }
        });
    }
    async processFile():Promise<void> {
        await this.upload();
        await this.startTranscript();
        await this.transcript().then(console.log);
    }
}

