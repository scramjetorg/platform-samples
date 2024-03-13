# Stream through tar.gz file and output stats

Sequence reads tar.gz file from input and returns JSON containing basic information about archived files along with unpacked data.

___

## Running

> ❗ Remember to [setup transform-hub locally](https://docs.scramjet.org/transform-hub/installation) or use the [platform's environment](https://docs.scramjet.org/platform/get-started/) for the sequence deployment.

Open two terminals and run the following commands:

### The first Terminal

```bash
# go to 'read-targz-stats' directory
cd typescript/read-targz-stats

# install dependencies
npm install

# transpile TS->JS and copy node_modules and package.json to dist/
npm run build

# deploy the Sequence from the dist/ directory, which contains transpiled code, package.json and node_modules
si seq deploy dist
# copy instance _id - you'll use this in 2nd terminal window

# see the Instance output
si inst output -
```

### The second terminal

```bash
# create test.tar.gz file from testFiles directory
tar -czvf testTar.tar.gz testFiles

# replace INSTANCE_ID with actual instance ID and pipe packed tar.gz file as binary to instance input
si inst input <INSTANCE_ID> testTar.tar.gz -t application/octet-stream
```

## Example output

```bash
{"name":"./testFiles/someTestFile","mode":436,"type":"file","uname":"esolecki","gname":"esolecki","size":26,"data":{"type":"Buffer","data":[83,111,109,101,32,116,101,120,116,32,105,110,115,105,100,101,32,116,101,115,116,32,102,105,108,101]}}
{"name":"./testFiles/someOtherTestFile","mode":436,"type":"file","uname":"esolecki","gname":"esolecki","size":28,"data":{"type":"Buffer","data":[79,116,104,101,114,32,116,101,120,116,32,105,110,115,105,100,101,32,111,116,104,101,114,32,102,105,108,101]}}
```
