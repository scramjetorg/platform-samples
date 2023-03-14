import * as mysql from "mysql";
const connection = mysql.createConnection({
    host     : "localhost",
    user     : "user",
    password : "password",
    database : "db-name",
    port: 3306
});

export async function dbPush(charactersStore):Promise<string> {
    const re = await new Promise<string>((res, rej) =>
        charactersStore.forEach((element) => {
            connection.query(`insert into characters (spec,weapon,hp) values ("${element.spec}" , "${element.weapon}", "${element.hp}");`, (e) => {
                if (e) rej(e);
                res("Entries successfully added \n");
            });
        }));

    return re;
}
export async function createDb() {
    connection.query(
        `create table characters (
                id int auto_increment primary key,
                spec varchar(255),
                hp varchar(255),
                weapon varchar(255)
            );
            `
    );
}
export async function dbRead():Promise<string> {
    const con = await new Promise<string>((res, rej) =>
        connection.query("select * from characters", (error, results:Array<any>) => {
            if (error) { rej(error); }
            res(results.map(e => `spec: "${e.spec}" hp: "${e.hp}" weapon: "${e.weapon}"`).join("\n"));
        }));

    return con;
}

