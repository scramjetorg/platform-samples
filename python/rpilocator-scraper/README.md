# Send to Telegram

This sample watches [rpilocator](https://rpilocator.com/feed/) for new stock. It then sends its urls to the specified Topic.

___
## Prerequisites
Open *main.py* file and configure the following settings:

- **topic name:** change ```example-topic-name``` to the desired Topic
```
provides = {
    'provides': 'example-topic-name',
    'contentType': 'text/plain'
}
```

- **specify models:** CM3,CM4,PI3,PI4,PIZERO

`MODELS = "CM4,PI4,PIZERO"`

- **specify regions:** AT,AU,BE,CA,CH,CN,DE,ES,FR,IT,NL,PL,PT,SE,UK,US,ZA

`REGIONS = "UK,DE,PL"`

- **set delay [in seconds]:**

`DELAY = 60`
 
**Note:** Don't set value lower than 60.

___
## Running
> 💡**NOTE:** Packaging of Python Sequences is not very "pythonic" for now. If you have any idea, how we should resolve it for your comfort, please let us know [here](https://github.com/scramjetorg/transform-hub/issues/598).

> ❗ Remember to [setup transform-hub locally](https://docs.scramjet.org/platform/self-hosted-installation) or use the [platform's environment](https://docs.scramjet.org/platform/quick-start) for the sequence deployment.

Open the terminal and run the following commands:

```bash
# Make sure you are inside 'rpilocator-scraper' directory, otherwise:
cd python/rpilocator-scraper

# Install dependencies
npm run build

# Deploy sample to STH
si seq deploy dist

# Get the output
si topic get <topicName>

```

If any new stock comes up, it will be written into the stream.
___


