# Json url based Sequence with `jsonUrl`, `interval` and `jsonPath` arguments

This is a Sequence similar to `json-url-output`. It also pulls the data from JSON url every x seconds and writes it to Instance stdout endpoint, but in this example one more argument is added → `jsonPath`. The file structure has also changed, the `utils.js` file has been added, to which the functions responsible for downloading json from the API, the json pull interval and the third function were the `jsonPath` given in string is converted into a path indicating a specific element nested in the json body.

The Sequence takes three arguments:

- `jsonUrl` - it is the address where the data in json format is available. List of free and open API that you can use as `jsonUrl` argument:
  - Predict age based on a name: <https://api.agify.io?name=bella>
  - Cocktail recipes: <https://www.thecocktaildb.com/api/json/v1/1/search.php?s=margarita>
  - Weather forecasts: <http://www.7timer.info/bin/api.pl?lon=113.17&lat=23.09&product=astro&output=json>
  - Random dog images: <https://dog.ceo/api/breeds/image/random>

- `interval` - time given in milliseconds (1s = 1000ms), with this parameter, we define how often the request is to be sent to the API, the time should be given in milliseconds, for example, providing this argument with a value of 5000 will result in sending the request every 5 seconds.

- `jsonPath` - it is the path to the element contained in the json object structure. The path points at the element which value we want to read.

## Start STH

Use command:

`sth` or `scramjet-transform-hub`

> Make sure your config is set to local STH: `si config reset all`

## Sequence deployment

Sequence is ready to use, id doesn't use any external modules so no dependencies need to be installed.

### Deploy

SI command to deploy the Sequence: `si seq deploy <path-to-sequence> --args [<jsonUrl>,<interval>,<jsonPath>]`, for example:

```bash
si seq deploy javascript/json-url-apps/json-seq-2 --args [\"https://www.thecocktaildb.com/api/json/v1/1/search.php?s=margarita\",10000,\"drinks[0].strDrink\"]
```

> Make sure there are no white spaces between the arguments in the args array.

The result of calling this command should be the info printed in the console similar to this one:

```bash
$ si seq deploy javascript/json-url-apps/json-seq-2 --args [\"https://www.thecocktaildb.com/api/json/v1/1/search.php?s=margarita\",10000,\"drinks[0].strDrink\"]
InstanceClient {
  host: HostClient {
    apiBase: 'http://127.0.0.1:8000/api/v1',
    client: ClientUtils {
      apiBase: 'http://127.0.0.1:8000/api/v1',
      fetch: [Function (anonymous)],
      normalizeUrlFn: [Function: normalizeUrl]
    }
  },
  _id: '286e1473-dff9-4543-b98b-56285b3953f1',
  instanceURL: 'instance/286e1473-dff9-4543-b98b-56285b3953f1'
}
```

### Read Instance stdout

The result of called sequence's function is a value of key `"strDrink"` (in this case thi value is `"Margarita"`). It is printed out in the console using `console.log()`, it means that the Sequence writes it to stdout instance endpoint. To read this endpoint stream please use the command:

```bash
si inst stdout -
```

Result:

```bash
$ si inst stdout -
Margarita
Margarita
```

The request is sent to API every 10 seconds, so the result will be printed out after every request until the Instance is stopped.
