import axios, { AxiosInstance } from "axios";

export class GitClient {
  public github: AxiosInstance;
  public repository: string;

  constructor(repository: string, token: string) {
    this.repository = repository;
    this.github = axios.create({
      baseURL: "https://api.github.com",
      headers: {
        authorization: `token ${token}`,
      },
    });
  }

  /**
   * Request contents of the file
   * @param path path to file relative to the repository root
   * @param branch branch name
   * @returns Promise<any>
   */
  getContents(
    path: string,
    branch: string | undefined = undefined
  ): Promise<any> {
    const ref = branch ? `?ref=${branch}` : "";
    return this.github.get(`/repos/${this.repository}/contents/${path}${ref}`);
  }

  /**
   * Commit new or update file contents
   * @param path path to file relative to the repository root
   * @param content file contents in base64 format
   * @param branch branch name
   * @param message commiet message
   * @returns Promise<any>
   */
  putContents(
    path: string,
    content: string,
    sha: string | undefined = undefined,
    branch: string | undefined = undefined,
    message: string | undefined = undefined
  ): Promise<any> {
    return this.github.put(`/repos/${this.repository}/contents/${path}`, {
      content,
      sha,
      message: message || `chore(${path}): updated json object`,
      path,
      branch,
    });
  }
}
