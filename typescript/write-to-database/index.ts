import { ReadableApp } from "@scramjet/types";
import { Connection, createConnection } from "mysql";
import { PassThrough, Readable } from "stream";

const createTodosQuery = `create table if not exists todos(
                            id int primary key auto_increment,
                            title varchar(255) not null,
                            completed tinyint(1) not null default 0
                        )`;

const createInsertTodoQuery = (title) =>
  `insert into todos (title) values ("${title}")`;

const connect = (connection: Connection): Promise<void> => {
  return new Promise((res, rej) => {
    connection.connect((err) => {
      if (err) {
        rej(err);
      } else {
        res();
      }
    });
  });
};

const createTodos = (connection: Connection): Promise<any> => {
  return new Promise((res, rej) => {
    connection.query(createTodosQuery, (err, results, fields) => {
      if (err) {
        rej(err);
      }

      res(results);
    });
  });
};

const insertTodo =
  (connection: Connection) =>
  (title: string): Promise<any> => {
    return new Promise((res, rej) => {
      connection.query(createInsertTodoQuery(title), (err, results, fields) => {
        if (err) {
          rej(err);
        }

        res(results);
      });
    });
  };

const disconnect = (connection: Connection): Promise<void> => {
  return new Promise((res, rej) => {
    connection.end(function (err) {
      if (err) {
        rej(err);
      } else {
        res();
      }
    });
  });
};

async function* chunksToLines(chunksAsync: Readable) {
  let previous = "";
  for await (const chunk of chunksAsync.pipe(
    new PassThrough({ encoding: "utf-8" })
  )) {
    previous += chunk;
    let eolIndex;
    while ((eolIndex = previous.indexOf("\n")) >= 0) {
      // line includes the EOL
      const line = previous.slice(0, eolIndex + 1);
      yield line;
      previous = previous.slice(eolIndex + 1);
    }
  }
  if (previous.length > 0) {
    yield previous;
  }
}

const app: ReadableApp<string, [string, string, string, string]> =
  async function* (input, host, user, password, database) {
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
