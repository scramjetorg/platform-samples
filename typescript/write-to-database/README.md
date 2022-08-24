# write-to-database

Sequence writes data to MySQL database.

## Preparations

Before proceeding setup MySQL database. The database can be setup locally when using the local version of transform-hub. Free MySQL hostings are good too e.g. freemysqlhosting.net.

> ❗ Remember to [setup transform-hub locally](https://docs.scramjet.org/platform/self-hosted-installation) or use the [platform's environment](https://docs.scramjet.org/platform/quick-start) for the sequence deployment.

## Running

Create `config.json` using `example.config.json` as an example. Put valid mysql config in the `config.json` and save it.

To start the sequence run commands below:

```bash
# go to sample directory
cd typescript/write-to-database

# install dependencies
npm install

# transpile TS->JS and copy node_modules and package.json to dist/
npm run build

# deploy the Sequence from the dist/ directory, which contains transpiled code, package.json and node_modules
si sequence deploy ./dist -f config.json

# see the Instance log
si inst log -
```

Check for database connection and table creation. It should be present in the logs if everything is all right.

```json
{"level":"DEBUG","msg":"Connecting to database","ts":1658405585664,"from":"Sequence","Runner":{"id":"91c3ccb1-3a9d-46b7-bde2-7bfd693620f8"}}
{"level":"DEBUG","msg":"Connecting to database","ts":1658405585664,"from":"Sequence","CSIController":{"id":"91c3ccb1-3a9d-46b7-bde2-7bfd693620f8"}}
{"level":"DEBUG","msg":"Checking for todos table","ts":1658405585746,"from":"Sequence","Runner":{"id":"91c3ccb1-3a9d-46b7-bde2-7bfd693620f8"}}
{"level":"DEBUG","msg":"Checking for todos table","ts":1658405585746,"from":"Sequence","CSIController":{"id":"91c3ccb1-3a9d-46b7-bde2-7bfd693620f8"}}
{"level":"DEBUG","msg":"Awaiting inserts","ts":1658405585751,"from":"Sequence","Runner":{"id":"91c3ccb1-3a9d-46b7-bde2-7bfd693620f8"}}
{"level":"DEBUG","msg":"Awaiting inserts","ts":1658405585751,"from":"Sequence","CSIController":{"id":"91c3ccb1-3a9d-46b7-bde2-7bfd693620f8"}}
```

At this point there should be new table in the database. To add a new record to the table send some string to the input

```bash
# connect to the input stream of the instance
si inst input <id>
# provide title for the todo element
asdf
```

After that the logs should show that new element is added to the table.

```json
{"level":"DEBUG","msg":"Inserting asdf\n","ts":1658405665408,"from":"Sequence","Runner":{"id":"91c3ccb1-3a9d-46b7-bde2-7bfd693620f8"}}
{"level":"DEBUG","msg":"Inserting asdf\n","ts":1658405665408,"from":"Sequence","CSIController":{"id":"91c3ccb1-3a9d-46b7-bde2-7bfd693620f8"}}
```

Check the contents of the table to see if everything is in place.
