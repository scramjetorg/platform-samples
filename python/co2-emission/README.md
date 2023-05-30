# CO₂ country emission fetching data from CO2Signal 

___

## Preparation

Get your own free API key from [CO2Signal](https://www.co2signal.com) site.

Prepare configuration:

```bash
cp config-example.json config.json
```

and replace ```<YOUR-TOKEN>``` in ```config.json``` with token recevied from CO2Signal.

## Running

Build sample:

```bash
cd python/co2-emission

npm run build

si seq deploy dist -f config.json
```

### Preview

To see the output, run in terminal:

```bash
si inst output -
```
