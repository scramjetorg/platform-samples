# Sequence sends forest images to the fire detecting machine learning API.
___


## Running

> ❗ Remember to [setup transform-hub locally](https://docs.scramjet.org/platform/self-hosted-installation) or use the [platform's environment](https://docs.scramjet.org/platform/quick-start) for the sequence deployment.

Open two terminals and run the following commands:


```bash
# go to 'seq-fire-alert' directory
cd python/seq-fire-alert

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


Now you should be able to see on the parameters on topic "fire":

```bash
si topic get pi