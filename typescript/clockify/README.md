# Clockify entry adder

Sequence which daily adds a new entry in Clockify

> ❗ By default this code adds 5 same entries for all weekdays. For weekends it adds new entries with 0 hours on them.

## Requirements

You need to have a [clockify account](https://app.clockify.me/signup) and a [access key](https://clockify.me/help/faq/where-can-i-find-api-information)

You also need to have scramjet cli installed, for guide how to install [visit our documentation](https://docs.scramjet.org/platform/get-started/)
## Preparations

Before running the code enter valid data in `data.json`, you need to fill all options to make the code working. For more informations how to get those details visit [Clockify Api documentation](https://docs.clockify.me/).

```json
{
    "apikey":"YOUR-API-KEY-HERE",
    "workspace":"WORKSPACE-ID",
    "weekDayProjectId":"WEEKDAY-PROJECT-ID",
    "satProjectId":"SATURDAY-PROJECT-ID",
    "sunProjectId":"SUNDAY-PROJECT-ID",
    "startHour": 9,//Start hour here in 24h format without leading 0 and minutes
    "endHour" : 17//End hour here in 24h format without leading 0 and minutes
}

```

## Running

To start the sequence simply run those commands in your terminal:


```bash
# go to sample directory
cd typescript/clockify

# install dependencies
npm install

# transpile TS->JS and copy node_modules and package.json to dist/
npm run build

# deploy the Sequence from the dist/ directory, which contains transpiled code, package.json and node_modules
si sequence deploy dist -f config.json

```

After completeing all steps the instance should be running and adding new entries to clockify daily.
