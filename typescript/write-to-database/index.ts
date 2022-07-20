import { DataStream } from "scramjet";
import { Connection, createConnection } from "mysql";
import { PassThrough, Transform } from "stream";

const createTodosQuery = `create table if not exists todos(
                            id int primary key auto_increment,
                            title varchar(255) not null,
                            completed tinyint(1) not null default 0
                        )`;

const createInsertTodoQuery = (title) =>
  `insert into todos (title) values (${title})`;

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

const app = async (input) => {
  // create output stream
  const out = new PassThrough({ encoding: "utf-8" });
  const connection = createConnection({
    host: "sql11.freemysqlhosting.net",
    user: "sql11507574",
    password: "ewsLgyjpUn",
    database: "sql11507574",
  });

  try {
    out.write("Connecting to database\n");
    await connect(connection);
    out.write("Checking for todos table\n");
    await createTodos(connection);
    out.write("Awaiting inserts\n");

    await DataStream.from(input)
      .map(async (title) => {
        out.write(title);
        return title;
      })
      .run();
  } catch (err) {
    out.write(`Error ${err.message}\n`);
    out.write("Disconnecting");
    await disconnect(connection);
  }

  return out;
};

export default app;
