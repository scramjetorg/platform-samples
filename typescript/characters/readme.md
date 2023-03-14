# Character-db-fs

Sequence that can create new classes and export/import them from filesystem and database

___

## Preparations

Before proceeding setup MySQL database. The database can be setup locally when using the local version of transform-hub. Free MySQL hostings are good too e.g. freemysqlhosting.net.

For more information how to setup MySQL database check : https://dev.mysql.com/doc/mysql-getting-started/en/#mysql-getting-started-installing

> ❗ This sequence will only work locally as it implements saveing to filesystem, check how to:  [setup transform-hub locally](https://docs.scramjet.org/platform/self-hosted-installation)
## Running
Firstly you need to start local sth server using command
```bash
DEVELOPMENT=1 sth --runtime-adapter=process
```
Then change connection settings in `/lib/db.ts` with your valid database details and process further.
```bash
const connection = mysql.createConnection({
    host     : "hostname",
    user     : "username",
    password : "password",
    database : "db-name",
    port: your-port
});
```
You can change values in `/lib/list.json` to any string values you wish in following format
```bash
#sequence only supports 2 specs:warrior/wizard
[
    {"spec":"warrior","weapon":"sword","hp":"120"},
    {"spec":"wizard","weapon":"blunt","hp":"115","spell":"fireball"}
]
```

To start the sequence run commands below:

```bash
# go to sample directory
cd directory/of/this/file
# install dependencies
npm install
# transpile TS->JS and copy node_modules and package.json to dist/
npm run build
# deploy the Sequence from the dist/ directory
#if you want to be able to add new character add --args '["warrior","axe","100"]' at the end of the command
si sequence deploy dist
# Open 2 terminals

# On the first one
si inst input <instance-id>
# On the second one
si inst output <instance-id>
```

## Available input commands:
**add** - add new character specified by --args argument and automaticaly save it to JSON file

**list** - read all character data saved in JSON file

**dbpush** - save all the entries saved in a classes to database

**dblist** - output all the entries saved in database

## Using events:
To use events type in your terminal:
```bash
 si inst event emit <inst-id> <event-name>
```
## Available events:

**create-db** - creates table to be used for this sequence

**list-to-object** - reads `/lib/list.json` and tranfer it to character classes

