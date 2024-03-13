# JSON url stdout

___

This is a Sequence similar to [json-url-output](../json-url-output/). It also pulls the data from JSON url every x seconds, but data is written to Instance stdout endpoint. Also one more argument is added → `jsonPath`.

The Sequence takes three arguments:

- `jsonUrl` - it is the address where the data in json format is available. List of free and open API that you can use as `jsonUrl` argument:
  - Predict age based on a name: <https://api.agify.io?name=bella>
  - Cocktail recipes: <https://www.thecocktaildb.com/api/json/v1/1/search.php?s=margarita>
  - Weather forecasts: <http://www.7timer.info/bin/api.pl?lon=113.17&lat=23.09&product=astro&output=json>
  - Random dog images: <https://dog.ceo/api/breeds/image/random>

- `interval` - time given in milliseconds (1s = 1000ms), with this parameter, we define how often the request is to be sent to the API, the time should be given in milliseconds, for example, providing this argument with a value of 5000 will result in sending the request every 5 seconds.

- `jsonPath` - it is the path indicating a specific element nested in the json body. The path points at the element which value we want to read.

## Running

> ❗ Remember to [setup transform-hub locally](https://docs.scramjet.org/platform/self-hosted-installation) or use the [platform's environment](https://docs.scramjet.org/platform/get-started/) for the sequence deployment.

Sequence is ready to use, id doesn't use any external modules so no dependencies need to be installed.

Open the terminal and run the following commands:

```bash
# go to 'javascript' directory
cd javascript

# deploy 'json-url-output' Sequence
si seq deploy json-url-stdout --args [\"https://www.thecocktaildb.com/api/json/v1/1/search.php?s=margarita\",10000,\"drinks[0].strDrink\"]

# see the Instance stdout
si inst stdout -
```

## Read Instance stdout

The result of called sequence's function is a value of key `"strDrink"` (in this case thi value is `"Margarita"`). It is printed out in the console using `console.log()`, it means that the Sequence writes it to stdout instance endpoint.
Result:

```bash
$ si inst stdout -
Margarita
Margarita
```

The request is sent to API every 10 seconds, so the result will be printed out after every request until the Instance is stopped.
