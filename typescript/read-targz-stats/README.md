
# Read-TarGz-stats

Sequence reads tar.gz file from input and returns JSON containing basic informations about archived files along with unpacked data.

## Running

Open three terminals and run the following commands:

### The First Terminal

```bash
# start sth by executing command...
scramjet-transform-hub

# ...or use script
cd transform-hub
npm run start -P 8000
```

### The Second terminal

```bash
# go to 'hexdump' directory
cd samples/read-targz-stats

# install dependencies
npm install

# transpile TS->JS and copy node_modules and package.json to dist/
npm run build

# deploy the Sequence from the dist/ directory, which contains transpiled code, package.json and node_modules
si seq deploy dist
# copy instance _id - you'll use this in 3rd terminal window

# see the Instance output
si inst output -
```

### The third terminal

```bash
# replace INSTANCE_ID with actual instance ID and pipe packed tar.gz file as binary to instance input
si inst input <INSTANCE_ID> testFiles/testTar.tar.gz -t application/octet-stream

```

Check output in second terminal to see hex format of scramjet.ico file.

## Example output

```bash
{"name":"./testFiles/someTestFile","mode":436,"type":"file","uname":"esolecki","gname":"esolecki","size":26,"data":{"type":"Buffer","data":[83,111,109,101,32,116,101,120,116,32,105,110,115,105,100,101,32,116,101,115,116,32,102,105,108,101]}}
{"name":"./testFiles/someOtherTestFile","mode":436,"type":"file","uname":"esolecki","gname":"esolecki","size":28,"data":{"type":"Buffer","data":[79,116,104,101,114,32,116,101,120,116,32,105,110,115,105,100,101,32,111,116,104,101,114,32,102,105,108,101]}}
```