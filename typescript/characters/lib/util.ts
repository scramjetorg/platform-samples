/* eslint-disable no-console */
import { dbPush, dbRead } from "./db";
import * as fs from "fs";
import { Character, CharacterType } from "./types";
const file = `${__dirname}/list.json`;

let charactersStore: Character[] = [];

class Warrior extends Character {
    message(): string {
        return `Your Character class is: "${this.spec}" uses: "${this.weapon}" and has: "${this.hp}"`;
    }

    toString(): string {
        return `,{ "spec": "${this.spec}", "weapon": "${this.weapon}", "hp": "${this.hp}" }`;
    }
}

class Wizard extends Character {
    constructor(info: CharacterType) {
        super(info);
        if (!info.spell) {
            throw new Error("Your Wizard class doesn't have required parameter: 'Spells'");
        }
    }

    message(): string {
        return `Your Character class is: "${this.spec}" uses: "${this.weapon}" has: "${this.hp}" and know how to use "${this.spell}" spell`;
    }

    toString(): string {
        return `{ spec: ${this.spec}, weapon: ${this.weapon}, hp: ${this.hp}, spell: ${this.spell}}`;
    }
}

export function readList(): Promise<string> {
    return new Promise((resolve, reject) => {
        let output = "";

        const readable = fs.createReadStream(file, { encoding: "utf-8" });

        readable
            .on("error", (err) => {
                console.log(err);
                reject();
            })
            .on("data", (chunk) => {
                output += chunk.toString();
            })
            .on("end", () => {
                charactersStore = JSON.parse(output);
                resolve(output);
            });
    });
}
export function save() {
    const data = JSON.stringify(
        charactersStore.map((char) => ({
            spec: char.spec,
            weapon: char.weapon,
            hp: char.hp,
        }))
    );

    fs.writeFile(file, data, (err) => {
        if (err) {
            console.error(err);
        }
    });
}
export async function checkIfExists() {
    return new Promise<void>((resolve, reject) => {
        fs.access(file, fs.constants.F_OK, (err) => {
            if (err) {
                fs.writeFile(file, "", (e) => {
                    if (e) {
                        console.log(e);
                        reject();

                        return;
                    }
                    resolve();
                });
            } else {
                resolve();
            }
        });
    });
}

export async function createCharacter(param) {
    let factory: typeof Wizard | typeof Warrior;

    if (param.spec === "wizard") {
        factory = Wizard;
    }

    if (param.spec === "warrior") {
        factory = Warrior;
    }

    if (!factory) {
        throw new Error("Unknown character class");
    }

    const char = new factory(param);

    await checkIfExists();

    return char;
}

export async function decide(chunk: string, arg1: string, arg2: string, arg3: string, arg4?: string): Promise<string> {
    let message = "";

    switch (chunk.toString()) {
        case "add\n":
            try {
                const char = await createCharacter({ spec: arg1.toLowerCase(), weapon: arg2, hp: arg3, spell: arg4 });

                charactersStore.push(char);
                await save();

                message += char.message();
            } catch (error) {
                message += error;
            }
            break;
        case "list\n":
            message += await readList().then(
                (l) => l,
                (_e) => "Error reading list"
            );
            break;
        case "db\n":
            message += await dbPush(charactersStore).then(
                (l) => l,
                (e) => e
            );
            break;
        case "dblist\n":
            message += await dbRead().then(
                (l) => l,
                (e) => e
            );
            break;
        default:
            message += "unknown command";
    }

    return message + "\n";
}
export async function listToObject() {
    await readList().then((c) => {
        JSON.parse(c).map(async (charData) => {
            charactersStore.push(await createCharacter(charData));
        });
    });
}
