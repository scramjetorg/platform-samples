import { ReadableApp } from "@scramjet/types";
import {
  connect,
  createConnection,
  createTodos,
  disconnect,
  insertTodo,
} from "./lib/db";
import { chunksToLines } from "./lib/utils";

const app: ReadableApp<string, [string, string, string, string]> =
  async function* (input) {
    const connection = createConnection({
      host: this.config.host as string,
      user: this.config.user as string,
      password: this.config.password as string,
      database: this.config.database as string,
    });

    try {
      this.logger.debug("Connecting to database");
      await connect(connection);
      this.logger.debug("Checking for todos table");
      await createTodos(connection);
      this.logger.debug("Awaiting inserts");

      for await (const line of chunksToLines(input)) {
        try {
          this.logger.debug(`Insering ${line}`);
          await insertTodo(connection)(line);
        } catch (err) {
          this.logger.error("Error while inserting", err);
        }
      }
    } catch (err) {
      this.logger.error("Error while starting", err);
      this.logger.debug("Disconnecting");
      await disconnect(connection);
    }
  };

export default app;
