# crypto-prices

Sequence that keeps printing current crypto prices for a provided pair of currencies every 3 seconds.

___

> 📽️ There is video that illustrates the execution of the sample is on our [YouTube](https://www.youtube.com/channel/UChgTmKeuAsKj8kDnylkmP6Q) channel [How to check cryptocurrency prices using Scramjet?](https://www.youtube.com/watch?v=BPLKPVVyHNY&t=3s). Give a 👍 if you liked it and "Subscribe" to the channel to keep up to date with new videos.

## Running

> ❗ Remember to [setup transform-hub locally](https://docs.scramjet.org/transform-hub/installation) or use the [platform's environment](https://docs.scramjet.org/platform/get-started/) for the sequence deployment.

Open the terminal and run the following commands:

```bash
# go to 'crypto-prices' directory
cd typescript/crypto-prices

# install dependencies
npm install

# transpile TS->JS and copy node_modules and package.json to dist/
npm run build

# deploy the Sequence from the dist/ directory, which contains transpiled code, package.json and node_modules
si seq deploy dist

# see the Instance output
si inst output -
```

> 💡**NOTE:** Command `deploy` performs three actions at once: `pack`, `send` and `start` the Sequence. It is the same as if you would run those three commands separately:

```bash
si seq pack dist/ -o crypto-prices.tar.gz    # compress 'dist/' directory into file named 'crypto-prices.tar.gz'

si seq send crypto-prices.tar.gz    # send packed Sequence to STH, this will output Sequence ID

si seq start -    # start the Sequence, this will output Instance ID
```

## Start with params

```bash
# run another Sequence by passing in arguments, any pair [cryptocurrency, currency]
$ si seq start - --args [\"ETH\",\"PLN\"]

# or similar with deploy
si seq deploy dist --args [\"ETH\",\"PLN\"]
```

## Output

Once you run `si inst output -` command you should get an output similar to this one:

```bash
"{\"data\":{\"base\":\"BTC\",\"currency\":\"USD\",\"amount\":\"40989.61\"}}\r\n"
"{\"data\":{\"base\":\"BTC\",\"currency\":\"USD\",\"amount\":\"40989.61\"}}\r\n"
"{\"data\":{\"base\":\"BTC\",\"currency\":\"USD\",\"amount\":\"40989.61\"}}\r\n"
"{\"data\":{\"base\":\"BTC\",\"currency\":\"USD\",\"amount\":\"40989.61\"}}\r\n"
"{\"data\":{\"base\":\"BTC\",\"currency\":\"USD\",\"amount\":\"40989.61\"}}\r\n"
"{\"data\":{\"base\":\"BTC\",\"currency\":\"USD\",\"amount\":\"40989.61\"}}\r\n"
"{\"data\":{\"base\":\"BTC\",\"currency\":\"USD\",\"amount\":\"40989.61\"}}\r\n"
"{\"data\":{\"base\":\"BTC\",\"currency\":\"USD\",\"amount\":\"40989.61\"}}\r\n"
"{\"data\":{\"base\":\"BTC\",\"currency\":\"USD\",\"amount\":\"40989.61\"}}\r\n"
```
