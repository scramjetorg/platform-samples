# simple-counter

___

As a default, the counter is started with 0 and ends with 1000. These values can be changed by passing the `start` and `end` parameters.

## Running

> ❗ Remember to [setup transform-hub locally](https://docs.scramjet.org/transform-hub/installation) or use the [platform's environment](https://docs.scramjet.org/platform/get-started/) for the sequence deployment.

Open the terminal and run the following commands:

```bash
# go to 'simple-counter-js' directory
cd javascript/simple-counter-js

# instal dependencies
npm run build

# deploy 'simple-counter-js' Sequence
si seq deploy dist

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

# instal dependencies
npm run build

# deploy sequence with arguments 
si seq deploy dist --args [100, 200]

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
```
