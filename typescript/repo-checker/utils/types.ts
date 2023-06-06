export type Config = {
    npmPackages:Array<string>;
    pyPiPackages:Array<string>;
    gitHubRepos:Array<{ owner:string, repo:string}>;
    dockerHubRepos:Array<string>;
};

export class Results {
    repoName:string;
    repoType:string;
    dataType:string;
    number:number|string;
    constructor(repoName:string, repoType:string, dataType:string, number:number|string) {
        this.repoName = repoName;
        this.repoType = repoType;
        this.dataType = dataType;
        this.number = number;
    }
}
