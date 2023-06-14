/* eslint-disable no-console */
import { Store } from "./utils/store";
import * as data from "./data.json";
import { ReadableApp } from "@scramjet/types";
import { PassThrough } from "stream";

const app: ReadableApp<any> = async function(
    _stream,
    interval:number = 1000 * 30,
    ghApiKey:string
) {
    const output: PassThrough & { topic: string, contentType: string } = Object.assign(
        new PassThrough({ encoding:"utf-8" }), { topic: "repo-data", contentType: "application/x-ndjson" }
    );

    async function main() {
        const store = new Store({
            gitHubRepos:data.gitHubRepos,
            dockerHubRepos:data.dockerHubRepos,
            npmPackages:data.npmRepos,
            pyPiPackages:data.pyPiRepos
        });

        store.setGitHubApiKey(ghApiKey);
        await store.getAllData()
            .then((res) => {
                res.forEach((element) => {
                    output.push(JSON.stringify(element));
                });
            });
    }
    main().catch((error) => {
        console.error(error);
    });
    setInterval(() => {
        main().catch((error) => {
            console.error(error);
        });
    }
    , interval);
    return output;
};

export default app;

