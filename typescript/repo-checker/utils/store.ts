import { PyPiClient } from "../clients/pyPiClient";
import { NpmClient } from "../clients/npmClient";
import { GitHubClient } from "../clients/gitHubClient";
import { DhClient } from "../clients/dockerHubClient";
import { Config, Results } from "./types";

export class Store {
    pyPiClient:PyPiClient = new PyPiClient();
    npmClient: NpmClient = new NpmClient();
    gitHubClient: GitHubClient = new GitHubClient();
    dhClient :DhClient = new DhClient();
    npmPackages:Array<string>;
    pyPiPacakges:Array<string>;
    gitHubRepos:Array<{owner:string, repo:string}>;
    dockerHubRepos:Array<string>;
    results:Array<Results> = [];

    constructor(config:Config) {
        this.npmPackages = config.npmPackages;
        this.pyPiPacakges = config.pyPiPackages;
        this.gitHubRepos = config.gitHubRepos;
        this.dockerHubRepos = config.dockerHubRepos;
    }
    setGitHubApiKey(ApiKey:string):void {
        this.gitHubClient.setAuth(ApiKey);
    }
    getPyPiClient():PyPiClient {
        return this.pyPiClient;
    }
    getNpmClient():NpmClient {
        return this.npmClient;
    }
    getGitHubClient():GitHubClient {
        return this.gitHubClient;
    }
    getDhClient():DhClient {
        return this.dhClient;
    }
    getPyPiWeeklyDownloads(repo:string):Promise<string> {
        this.pyPiClient.setPackageName(repo);
        return this.pyPiClient.sendRequest();
    }
    getGitHubWeeklyStars(repo:{owner:string, repo:string}):Promise<any> {
        this.gitHubClient.setRepo(repo);
        return this.gitHubClient.getStars();
    }
    getGitHubWeeklyViews(repo:{owner:string, repo:string}) {
        this.gitHubClient.setRepo(repo);
        return this.gitHubClient.getViews();
    }
    getDockerHubPullCount(repo:string) {
        this.dhClient.setPackageName(repo);
        return this.dhClient.getPullCount();
    }
    getDockerHubStars(repo:string) {
        this.dhClient.setPackageName(repo);
        return this.dhClient.getStars();
    }
    getNpmWeeklyDownloads(repo:string) {
        this.npmClient.setPackageName(repo);
        return this.npmClient.getWeeklyDownloads();
    }
    private async pushNpmWeeklyDownloads() {
        await Promise.all(
            this.npmPackages.map(async (repo) => {
                const downloads = await this.getNpmWeeklyDownloads(repo);

                this.results.push(new Results(repo, "npm", "weekly downloads", downloads));
            }));
    }
    private async pushDockerHubStars() {
        await Promise.all(
            this.dockerHubRepos.map(async (repo) => {
                const stars = await this.getDockerHubStars(repo);

                this.results.push(new Results(repo, "docker hub", "total stars", stars));
            }));
    }
    private async pushDockerHubPullCount() {
        await Promise.all(
            this.dockerHubRepos.map(async (repo) => {
                const pulls = await this.getDockerHubPullCount(repo);

                this.results.push(new Results(repo, "docker hub", "total pulls", pulls));
            }));
    }
    private async pushPyPiWeeklyDownloads() {
        await Promise.all(
            this.pyPiPacakges.map(async (repo) => {
                const downloads = await this.getPyPiWeeklyDownloads(repo);

                this.results.push(new Results(repo, "PyPi", "weekly downloads", downloads));
            }));
    }
    private async pushGitHubWeeklyViews() {
        await Promise.all(
            this.gitHubRepos.map(async (repo) => {
                const views = await this.getGitHubWeeklyViews(repo);

                this.results.push(new Results(repo.repo, "github", "weekly views", views));
            }));
    }
    private async pushGitHubWeeklyStars() {
        await Promise.all(
            this.gitHubRepos.map(async (repo) => {
                const stars = await this.getGitHubWeeklyStars(repo);

                this.results.push(new Results(repo.repo, "github", "weekly stars", stars));
            }));
    }
    async getAllData() {
        await Promise.all([
            this.pushNpmWeeklyDownloads(),
            this.pushDockerHubStars(),
            this.pushDockerHubPullCount(),
            this.pushPyPiWeeklyDownloads(),
            this.pushGitHubWeeklyStars(),
            this.pushGitHubWeeklyViews()
        ]);
        return this.results;
    }
}
