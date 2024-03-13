# Hello world ts

 ___

Simple sequence that outputs "Hello world" written in typescript.

## Running

> ❗ Remember to [setup transform-hub locally](https://docs.scramjet.org/transform-hub/installation) or use the [platform's environment](https://docs.scramjet.org/platform/get-started/) for the sequence deployment.

Open two terminals and run the following commands:

**The first terminal:**

```bash
# install dependencies
npm install

# transpile TS->JS to dist/
npm run build

# make a compressed package with Sequence
si seq pack dist

# send Sequence to transform hub, this will output Sequence ID
si seq send dist.tar.gz

# start a Sequence
si seq start -
```

**The second terminal**

Read the Instance output:

```bash
si inst output -
```

You should see "Hello World!" printed out in the terminal.
