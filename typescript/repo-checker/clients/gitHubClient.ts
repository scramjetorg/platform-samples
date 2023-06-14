/* eslint-disable no-console */
import { Octokit } from "octokit";

export class GitHubClient {
    octokit;
    repo:string;
    key:string;
    owner:string;
    setRepo(repo:{owner:string, repo:string}) {
        this.repo = repo.repo;
        this.owner = repo.owner;
    }
    setAuth(key:string) {
        this.key = key;
        this.octokit = new Octokit({
            auth: key,
        });
    }

    async getViews():Promise<string> {
        return new Promise((resolve, reject) => {
            this.octokit.request(`get /repos/${this.owner}/${this.repo}/traffic/views?week`)
                .then((res) => resolve(res.data.count))
                .catch((error) => reject(error));
        });
    }
    async getStars() {
        const stars = await this.octokit.request(`get /repos/${this.owner}/${this.repo}`)
            .then((res) => res.data.stargazers_count);

        return stars;
    }
}
