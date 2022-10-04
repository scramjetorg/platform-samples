# send-to-github

___

In this sample, Sequence after deployment takes JSON objects on input stream and commits it to a file on Github. If the file does not exist a new file is created. If the file exists contents of the file are updated.

## Preparations

For the sequence to work the Github repository is necessary. Also Personal Access Token needs to be provided and it can be obtained [here](https://github.com/settings/tokens).

> ❗ Remember to [setup transform-hub locally](https://docs.scramjet.org/platform/self-hosted-installation) or use the [platform's environment](https://docs.scramjet.org/platform/quick-start) for the sequence deployment.

## Running

Create `config.json` using `example.config.json` as an example. Put valid Github repository info and the Personal Access Token in the `config.json` and save it.

To start the sequence run the commands below:

```bash
# go to sample directory
cd typescript/send-to-github

# install dependencies
npm install

# transpile TS->JS and copy node_modules and package.json to dist/
npm run build

# deploy the Sequence from the dist/ directory, which contains transpiled code, package.json and node_modules
si sequence deploy dist -f config.json

# see the Instance log
si inst log -
```

Check logs for the Github client creation. It should be present if everything is all right.

```json
{"level":"DEBUG","msg":"Creating GitClient","ts":1658791965555,"from":"Sequence","Runner":{"id":"1fa83e60-9705-41c5-83a6-722d926bd137"}}
{"level":"DEBUG","msg":"Creating GitClient","ts":1658791965555,"from":"Sequence","CSIController":{"id":"1fa83e60-9705-41c5-83a6-722d926bd137"}}
```

To create or update a file in the repository send a JSON object to the input of the sequence. Remember it should be in one line.

```bash
# connect to the input stream of the instance
si inst input <id>
# provide title for the todo element
{"test":2}
```

After that, the logs should show which file is being changed and if it ended with success.

```json
{"level":"DEBUG","msg":"Trying to get test.json file contents","ts":1658789843499,"from":"Sequence","Runner":{"id":"bb32a230-cceb-48db-b2e2-eb7fedbd18bf"}}
{"level":"DEBUG","msg":"Trying to get test.json file contents","ts":1658789843499,"from":"Sequence","CSIController":{"id":"bb32a230-cceb-48db-b2e2-eb7fedbd18bf"}}
{"level":"INFO","msg":"Previous version SHA 7ee7b727838a5d8e76088a01348d3081542c5266","ts":1658789843655,"from":"Sequence","Runner":{"id":"bb32a230-cceb-48db-b2e2-eb7fedbd18bf"}}
{"level":"DEBUG","msg":"Saving json to github repository file test.json","ts":1658789843655,"from":"Sequence","Runner":{"id":"bb32a230-cceb-48db-b2e2-eb7fedbd18bf"}}
{"level":"INFO","msg":"Previous version SHA 7ee7b727838a5d8e76088a01348d3081542c5266","ts":1658789843655,"from":"Sequence","CSIController":{"id":"bb32a230-cceb-48db-b2e2-eb7fedbd18bf"}}
{"level":"DEBUG","msg":"Saving json to github repository file test.json","ts":1658789843655,"from":"Sequence","CSIController":{"id":"bb32a230-cceb-48db-b2e2-eb7fedbd18bf"}}
{"level":"INFO","msg":"Object have been saved!","ts":1658789843965,"from":"Sequence","Runner":{"id":"bb32a230-cceb-48db-b2e2-eb7fedbd18bf"}}
{"level":"INFO","msg":"Object have been saved!","ts":1658789843965,"from":"Sequence","CSIController":{"id":"bb32a230-cceb-48db-b2e2-eb7fedbd18bf"}}
```

As the last step, check the file's contents in the Github repository.

```json
{ "test": 2 }
```
