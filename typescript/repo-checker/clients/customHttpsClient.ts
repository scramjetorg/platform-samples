import { get } from "https";

export class CustomHttpsClient {
    url:string;

    setUrl(url:string) {
        this.url = url;
    }
    sendRequest():Promise<string> {
        return new Promise((resolve, reject) => {
            get(this.url, (res) => {
                let data = "";

                res.on("data", (chunk) => {
                    data += chunk;
                });
                res.on("end", () => {
                    if (res.statusCode !== 200) {
                        console.log(res.statusCode);
                        reject(`Unexpected status code: ${res.statusCode}`);
                        return;
                    }
                    resolve(data);
                });
            }).on("error", (error) => {
                reject(error);
            });
        });
    }
}
