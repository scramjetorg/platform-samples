# Json url based Sequence with `jsonUrl` and `interval` arguments

This is a simple Sequence that pulls data from JSON url every x seconds and writes it to Instance stdout endpoint.
The Sequence takes two arguments:

- `jsonUrl` - it is the address where the data in json format is available. List of free and open API that you can use as `jsonUrl` argument:
  - Predict age based on a name: <https://api.agify.io?name=bella>
  - Cocktail recipes: <https://www.thecocktaildb.com/api/json/v1/1/search.php?s=margarita>
  - Weather forecasts: <http://www.7timer.info/bin/api.pl?lon=113.17&lat=23.09&product=astro&output=json>
  - Random dog images: <https://dog.ceo/api/breeds/image/random>

- `interval` - time given in milliseconds (1s = 1000ms), with this parameter, we define how often the request is to be sent to the API, the time should be given in milliseconds, for example, providing this argument with a value of 5000 will result in sending the request every 5 seconds.

## Start STH

Use command:

`sth` or `scramjet-transform-hub`

> Make sure your config is set to local STH: `si config reset all`

## Sequence deployment

Sequence is ready to use, id doesn't use any external modules so no dependencies need to be installed.

### Deploy

SI command to deploy the Sequence: `si seq deploy <path-to-sequence> --args [<jsonUrl>,<interval>]`, for example:

```bash
si seq deploy javascript/json-url-apps/json-seq-1 --args [\"https://api.agify.io?name=bella\",10000]
```

> Make sure there are no white spaces between the arguments in the args array.

The result of calling this command should be the info printed in the console similar to this one:

```bash
$ si seq deploy javascript/json-url-apps/json-seq-1 --args [\"https://api.agify.io?name=bella\",10000]
InstanceClient {
  host: HostClient {
    apiBase: 'http://127.0.0.1:8000/api/v1',
    client: ClientUtils {
      apiBase: 'http://127.0.0.1:8000/api/v1',
      fetch: [Function (anonymous)],
      normalizeUrlFn: [Function: normalizeUrl]
    }
  },
  _id: '816cfaa7-4ad8-4451-8e38-45bf1f2f1b6d',
  instanceURL: 'instance/816cfaa7-4ad8-4451-8e38-45bf1f2f1b6d'
}
```

### Read Instance stdout

The result of called sequence's function is a json object. It is printed out in the console using `console.log()`, it means that the Sequence writes it to stdout instance endpoint. To read this endpoint stream please use the command:

```bash
si inst output -
```

Result:

```bash
$ si inst output -
{ name: 'bella', age: 35, count: 40138 }
{ name: 'bella', age: 35, count: 40138 }
```

The request is sent to API every 10 seconds, so the result will be printed out after every request until the Instance is stopped.
