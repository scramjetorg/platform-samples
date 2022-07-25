import { ReadableApp } from "@scramjet/types";
import { chunksToLines } from "./lib/utils";
import { GitClient } from "./lib/gitClient";

const app: ReadableApp<string> = async function* (input) {
  const path = this.config.path as string;
  const branch = this.config.branch as string;
  const repository = this.config.repository as string;
  const token = this.config.token as string;

  this.logger.debug(`Creating GitClient`);

  const gitClient = new GitClient(repository, token);

  for await (const line of chunksToLines(input)) {
    let previousVerionSHA;

    try {
      this.logger.debug(`Trying to get ${path} file contents`);

      const previousVersion = await gitClient.getContents(path, branch);
      previousVerionSHA = previousVersion?.data?.sha;

      this.logger.info(`Previous version SHA ${previousVerionSHA}`);
    } catch (err) {
      this.logger.error(
        "Error while retriving current contents. File may not exist yet. Skipping previous content SHA.",
        err
      );
    }

    try {
      this.logger.debug(`Saving json to github repository file ${path}`);

      const content = Buffer.from(JSON.stringify(JSON.parse(line)))
        .toString("base64")
        .trim();

      await gitClient.putContents(path, content, previousVerionSHA, branch);

      this.logger.info(`Object have been saved!`);
    } catch (err) {
      this.logger.error("Error while saving", err);
    }
  }
};

export default app;
