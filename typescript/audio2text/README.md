# Audio to text

Sequence used to transcript audio file to a text using AssemblyAi api.

For now this sequence lets transcript only file that is in a dist folder

## Prerequirements

To run this sequence it is required to have own api key from [AssemblyAi](https://www.assemblyai.com)


## Running

> ❗ Remember to [setup transform-hub locally](https://docs.scramjet.org/platform/self-hosted-installation) or use the [platform's environment](https://docs.scramjet.org/platform/quick-start) for the sequence deployment.

Open the terminal and run the following commands:

```bash
# install dependencies
npm install

# transpile TS->JS to dist/
npm run build

# make a compressed package with Sequence
si seq pack dist

# send Sequence to transform hub, this will output Sequence ID
si seq send dist.tar.gz

# start a Sequence, provide AssemblyAi-key as an argument parameter
si seq start - --args [\"AssemblyAi-key\"]
```

To get a output:

```bash
si inst stdout -

```
