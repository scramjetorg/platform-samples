/* eslint-disable no-console */
import * as data from "../data.json";
import { request } from "https";
import { ClientRequest } from "http";

type clockifyTimeEntry = {
    startTime:Date,
    endTime:Date,
    projectId:string
}
export class ClockifyClient {
    apiKey:string = data.apikey;
    workspace:string = data.workspace;
    options = {
        hostname: "api.clockify.me",
        path: `/api/v1/workspaces/${data.workspace}/time-entries`,
        port: 443,
        headers: {
            "X-Api-Key": data.apikey,
            "content-type": "application/json"
        },
        method: "POST",
    };
    async sendRequest(info:clockifyTimeEntry) :Promise<any> {
        const body = JSON.stringify({
            billable:"false",
            end: info.endTime,
            projectId: info.projectId,
            start:info.startTime
        });

        console.log(body);

        const req:ClientRequest = request(this.options, (res) => {
            console.log("statusCode:", res.statusCode);
        });

        return new Promise((res, rej) => {
            req.on("error", (e) => {
                rej(e);
            });
            req.on("end", () => {
                res("succesfully added new entry ");
            });
            req.write(body);
            req.end();
        });
    }
}
