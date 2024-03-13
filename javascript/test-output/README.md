# test-output

Sequence that just writes random values to output stream.

___

## Running

> ❗ Remember to [setup transform-hub locally](https://docs.scramjet.org/transform-hub/installation) or use the [platform's environment](https://docs.scramjet.org/platform/get-started/) for the sequence deployment.

Open the terminal and run the following commands:

```bash
# go to 'test-output' directory
cd javascript/test-output

# install dependencies
npm install

# go back to javascript/ directory
cd ../

# deploy 'hello' Sequence
si seq deploy test-output

# See output of Instance process
si inst output -
```

> 💡**NOTE:** Command `deploy` performs three actions at once: `pack`, `send` and `start` the Sequence. It is the same as if you would run those three commands separately:

```bash
si seq pack . -o test-output.tar.gz    # compress 'test-output/' directory into file named 'test-output.tar.gz'

si seq send test-output.tar.gz    # send compressed Sequence to STH, this will output Sequence ID

si seq start -    # start the Sequence, this will output Instance ID
```

## Output

```bash
Test 6
Test 0
Test 5
Test 4
Test 9
Test 2
Test 3
Test 4
Test 0
Test 2
Test 2
...
```
