import { CustomHttpsClient } from "./customHttpsClient";
export class DhClient {
    packageName:string;
    url:string;
    httpsClient = new CustomHttpsClient();
    setPackageName(packageName:string) {
        this.packageName = packageName;
        this.url = `https://hub.docker.com/v2/repositories/${packageName}`;
    }
    async getStars():Promise<string> {
        this.httpsClient.setUrl(this.url);
        const stars = await this.httpsClient.sendRequest()
            .then((res) => JSON.parse(res).star_count);

        return stars;
    }
    async getPullCount():Promise<string> {
        this.httpsClient.setUrl(this.url);
        const pulls = await this.httpsClient.sendRequest()
            .then((res) => JSON.parse(res).pull_count);

        return pulls;
    }
}
