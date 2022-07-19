A simple Sequence that pulls data from JSON url every x seconds (arguments: url, JSON path, time)

si command to deploy the Sequence:

```bash
si seq deploy javascript/json-url-app --args [\"https://www.thecocktaildb.com/api/json/v1/1/search.php?s=margarita\",10000]
```

see the output on stdout:

```bash
si inst stdout -
```

Arguments description:

- jsonUrl - it is the address where the data in json format is available, for example: https://www.thecocktaildb.com/api/json/v1/1/search.php?s=margarita

- time - time given in milliseconds (1s = 1000ms), with this parameter, we define how often the request is to be sent to the API, the time should be given in milliseconds, for example, providing this argument with a value of 5000 will result in sending the request every 5 seconds.
