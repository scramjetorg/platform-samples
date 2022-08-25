# hello-snowman ⛄

Sequence that reads incoming stream (input), and and modifies it by adding a text message according to the incoming data.

___

Stream is generated in [stream-gen.js](../tools/stream-gen-tool/stream-gen.js) file, where numbers in range of <-50,50> are randomly chosen and sent as Celsius degrees to `hello-snowman` Instance API endpoint `/input`.

Our `hello-snowman` app will read and interpret these Celsius degrees, and will inform us about state of our Snowman:

- if temperature will be 0 or below, Sequence will return message:

```bash
Snowman ⛄ is freezing 🥶 Winter is coming ❄️ ❄️ ❄️ ❄️ ❄️
```

- in the other case (temperature above 0 degrees), Sequence will return message:

```bash
 Snowman ⛄ is melting! 🥵
```

## Running

> ❗ Remember to [setup transform-hub locally](https://docs.scramjet.org/platform/self-hosted-installation) or use the [platform's environment](https://docs.scramjet.org/platform/quick-start) for the sequence deployment.

Open two terminals and run the following commands:

**The first terminal:**

```bash
# go to 'hello-snowman' directory
cd javascript/hello-snowman

# install dependencies
npm install

# go back to javascript/ directory
cd ../

# deploy 'hello-snowman' Sequence
si seq deploy hello-snowman

# see the Instance output
si inst output -    # nothing happens until some is sent to input
```

> 💡**NOTE:** Command `deploy` performs three actions at once: `pack`, `send` and `start` the Sequence. It is the same as if you would run those three commands separately:

```bash
si seq pack . -o hello-snowman.tar.gz    # compress 'hello-snowman/' directory into file named 'hello-snowman.tar.gz'

si seq send hello-snowman.tar.gz    # send compressed Sequence to STH, this will output Sequence ID

si seq start -    # start the Sequence, this will output Instance ID
```

**The second terminal**

```bash
# Start stream generator tool with Instance ID as parameter
node ./tools/stream-gen-tool/stream-gen.js <instance_id>
```

## Output

Now you should see the output in the console:

```js
$ si inst output -
----------------------------------------
Message# 1 | Temperature measure
INPUT | -16
OUTPUT| Snowman ⛄ is freezing 🥶 Winter is coming ❄️ ❄️ ❄️ ❄️ ❄️

----------------------------------------
Message# 2 | Temperature measure
INPUT | 49
OUTPUT| Snowman ⛄ is melting! 🥵

----------------------------------------
Message# 3 | Temperature measure
INPUT | 16
OUTPUT| Snowman ⛄ is melting! 🥵

----------------------------------------
Message# 4 | Temperature measure
INPUT | -46
OUTPUT| Snowman ⛄ is freezing 🥶 Winter is coming ❄️ ❄️ ❄️ ❄️ ❄️

----------------------------------------
```
