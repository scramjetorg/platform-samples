import { Connection } from "mysql";
export { createConnection } from "mysql";

export const createTableTodosQuery = () => `create table if not exists todos(
                            id int primary key auto_increment,
                            title varchar(255) not null,
                            completed tinyint(1) not null default 0
                        )`;

export const createInsertTodoQuery = (title) =>
  `insert into todos (title) values ("${title}")`;

export const connect = (connection: Connection): Promise<void> => {
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

export const createTodos = (connection: Connection): Promise<any> => {
  return new Promise((res, rej) => {
    connection.query(createTableTodosQuery(), (err, results, fields) => {
      if (err) {
        rej(err);
      }

      res(results);
    });
  });
};

export const insertTodo =
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

export const disconnect = (connection: Connection): Promise<void> => {
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
