# Hello world js 

___

Simple sequence that outputs "Hello world" written in javascript.

## Running

> ❗ Remember to [setup transform-hub locally](https://docs.scramjet.org/platform/self-hosted-installation) or use the [platform's environment](https://docs.scramjet.org/platform/quick-start) for the sequence deployment.

Open two terminals and run the following commands:

**The first terminal:**

```bash
# go to 'hello-world-js' directory
cd javascript/hello-world-js

# install node_modules
npm install

# go back to javascript/ directory
cd ../

# deploy 'hello-world-js' Sequence
si seq deploy hello-world-js
```

**The second terminal**

Read the Instance output:

```bash
si inst output -
```

You should see "Hello World!" printed out in the terminal.
