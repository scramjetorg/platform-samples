# JSON url output

___

This is a simple Sequence that pulls data from JSON url every x seconds and writes it to Instance stdout endpoint.
The Sequence takes two arguments:

- `jsonUrl` - it is the address where the data in json format is available. List of free and open API that you can use as `jsonUrl` argument:
  - Predict age based on a name: <https://api.agify.io?name=bella>
  - Cocktail recipes: <https://www.thecocktaildb.com/api/json/v1/1/search.php?s=margarita>
  - Weather forecasts: <http://www.7timer.info/bin/api.pl?lon=113.17&lat=23.09&product=astro&output=json>
  - Random dog images: <https://dog.ceo/api/breeds/image/random>

- `interval` - time given in milliseconds (1s = 1000ms), with this parameter we define how often the request is sent to the API, the time should be given in milliseconds, for example, providing this argument with a value of 5000 will result in sending the request every 5 seconds.

## Running

> ❗ Remember to [setup transform-hub locally](https://docs.scramjet.org/platform/self-hosted-installation) or use the [platform's environment](https://docs.scramjet.org/platform/quick-start) for the sequence deployment.

Sequence is ready to use, id doesn't use any external modules so no dependencies need to be installed.

Open the terminal and run the following commands:

```bash
# go to 'javascript' directory
cd javascript

# deploy 'json-url-output' Sequence
si seq deploy json-url-output --args [\"https://api.agify.io?name=bella\",10000]

# see the Instance output
si inst output -
```

## Output

Result:

```bash
$ si inst output -
{ name: 'bella', age: 35, count: 40138 }
{ name: 'bella', age: 35, count: 40138 }
```

The request is sent to API every 10 seconds, so the result will be printed out after every request until the Instance is stopped.
