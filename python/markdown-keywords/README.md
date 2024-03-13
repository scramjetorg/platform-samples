# Sequence suggesting keywords for header in *.md

___

Easy example of usage Kafka with Scramjet platform.

## Running

> ❗ Remember to [setup transform-hub locally](https://docs.scramjet.org/platform/get-started/) or use the [platform's environment](https://docs.scramjet.org/platform/get-started/) for the sequence deployment.

Open two terminals and run the following commands:

**The first terminal:**

```bash
# go to 'markdown-keywords' directory
cd python/markdown-keywords

# build
npm run build
```

If you run this sample on Self Hosted Hub, please start it with process adapter option:

```bash
DEVELOPMENT=1 sth --runtime-adapter=process
```

Once you've built it, you need to deploy it.

```bash
si seq deploy dist
```

Now you can pass *.md file to instance input., for example `README.md`

```bash
si inst input - README.md
```

**The second terminal**

Now you should be able to see on the output the content of `README.md` file:

```bash
si inst output <INSTANCE_ID>
```
