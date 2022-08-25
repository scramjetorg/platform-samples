# simple-counter

___

As a default, the counter is started with 0 and ends with 1000. These values can be changed by passing the `start` and `end` parameters.

## Running

> ❗ Remember to [setup transform-hub locally](https://docs.scramjet.org/platform/self-hosted-installation) or use the [platform's environment](https://docs.scramjet.org/platform/quick-start) for the sequence deployment.

Open the terminal and run the following commands:

```bash
# go to 'simple-counter-js' directory
cd javascript/simple-counter-js

# instal dependencies
npm install

# go back to javascript/ directory
cd ../

# deploy 'simple-counter-js' Sequence
si seq deploy simple-counter-js

# See output of Instance process
si inst stdout -
```

> 💡**NOTE:** Command `deploy` performs three actions at once: `pack`, `send` and `start` the Sequence. It is the same as if you would run those three commands separately:

```bash
si seq pack . -o simple-counter-js.tar.gz    # compress 'simple-counter-js/' directory into file named 'simple-counter-js.tar.gz'

si seq send simple-counter-js.tar.gz    # send compressed Sequence to STH, this will output Sequence ID

si seq start -    # start the Sequence, this will output Instance ID
```

## Output

```bash
{ x: 1 }
{ x: 2 }
{ x: 3 }
{ x: 4 }
{ x: 5 }
{ x: 6 }
{ x: 7 }
{ x: 8 }
{ x: 9 }
{ x: 10 }
{ x: 11 }
{ x: 12 }
{ x: 13 }
{ x: 14 }
...
```

## Running the same Sequence but with some parameters

```bash
# go to 'simple-counter-js' directory
cd samples/simple-counter-js

# instal node_modules
npm install

# make a compressed package with Sequence
si seq pack . -o simple-counter-js.tar.gz

# send Sequence to transform hub, this will output Sequence ID
si seq send simple-counter-js.tar.gz

# start a Sequence with "start" and "end" parameters, this will output Instance ID
si seq start - 100 2000

# See output
si inst stdout -
```

## Output

```bash
# the counter will start counting at 100 and finish at 200
{ x: 101 }
{ x: 102 }
{ x: 103 }
{ x: 104 }
{ x: 105 }
{ x: 106 }
...
{ x: 193 }
{ x: 194 }
{ x: 195 }
{ x: 196 }
{ x: 197 }
{ x: 198 }
{ x: 199 }
{ x: 200 }
```
