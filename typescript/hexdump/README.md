
# Hexdump

Sequence returns input in hex format.

## Running

Open three terminals and run the following commands:

### The First Terminal

```bash
# start sth by executing command...
scramjet-transform-hub

# ...or use script
cd transform-hub
yarn start -P 8000
```

### The Second terminal

```bash
# go to 'hexdump' directory
cd samples/hexdump

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
# replace INSTANCE_ID with actual instance ID and pipe scramjet.ico as binary to instance input
si inst input <INSTANCE_ID> scramjet.ico -t application/octet-stream
```

Check outpu in second terminal to see hex format of scramjet.ico file.
