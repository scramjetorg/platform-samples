# Hello world py

Simple Sequence that outputs "Hello world" written in python

## Running

> ❗ Remember to [setup transform-hub locally](https://docs.scramjet.org/platform/self-hosted-installation) or use the [platform's environment](https://docs.scramjet.org/platform/quick-start) for the sequence deployment.

Open two terminals and run the following commands:

**The first terminal:**

Open the terminal and run the following commands:

```bash
# go to 'hello-world-py' directory
cd python/hello-world-py

# build
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
