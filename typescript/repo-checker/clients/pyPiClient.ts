import { CustomHttpsClient } from "./customHttpsClient";
export class PyPiClient {
    packageName:string;
    url:string;

    setPackageName(packageName:string) {
        this.packageName = packageName;
        this.url = `https://pypistats.org/api/packages/${packageName}/recent`;
    }
    async sendRequest() {
        const customHttpsClient = new CustomHttpsClient();

        customHttpsClient.setUrl(this.url);
        return await customHttpsClient.sendRequest()
            .then((res) => JSON.parse(res).data.last_week);
    }
}
