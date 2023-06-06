import { CustomHttpsClient } from "./customHttpsClient";
export class NpmClient {
    packageName:string;
    url:string;
    httpsClient = new CustomHttpsClient();

    setPackageName(packageName:string) {
        this.packageName = packageName;
        this.url = `https://api.npmjs.org/downloads/point/last-week/${packageName}`;
    }

    async getWeeklyDownloads():Promise<string> {
        this.httpsClient.setUrl(this.url);
        const downloads = await this.httpsClient.sendRequest()
            .then((res) => JSON.parse(res).downloads);

        return downloads;
    }
}
