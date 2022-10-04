# hello 🙋‍♂️

Sequence that modifies incoming stream of strings by adding "Hello".

___

## Running

> ❗ Remember to [setup transform-hub locally](https://docs.scramjet.org/platform/self-hosted-installation) or use the [platform's environment](https://docs.scramjet.org/platform/quick-start) for the sequence deployment.

Open two terminals and run the following commands:

**The first terminal:**

```bash
# go to 'hello' directory
cd javascript/hello

# install dependencies
npm install

# go back to javascript/ directory
cd ../

# deploy 'hello' Sequence
si seq deploy hello

# see the Instance output
si inst output -    # nothing happens until some is sent to input
```

> 💡**NOTE:** Command `deploy` performs three actions at once: `pack`, `send` and `start` the Sequence. It is the same as if you would run those three commands separately:

```bash
si seq pack . -o hello.tar.gz    # compress 'hello/' directory into file named 'hello.tar.gz'

si seq send hello.tar.gz    # send compressed Sequence to STH, this will output Sequence ID

si seq start -    # start the Sequence, this will output Instance ID
```

**The second terminal**

```bash
# Send file to Instance input steam
si inst input - path/to/file/data.txt
# if file not given the data will be read from stdin
si inst input -
# hit enter and type "John"
John
```

## Output

```bash
# Now you should see "Hello John" in output console
$ si inst output -
Hello John
```
