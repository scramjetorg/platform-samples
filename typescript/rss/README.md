# RSS

___

This sample gets a list of RSS feed URLs from `./config/rss.json` file. Then it retrieves each feed and passes links to scraper.
Scraper reads content of each URL. Next, keywords are matched and a score given for each URL.

If score is grater than 0 it gets added to a list of links and short details are posted to slack channel.

## Configuration

Pass SLACK_WEBHOOK_URL as input parameter when starting Sequence.

Keywords are configured in `./config/keywords.json` file. Use `word` and `weight` as in the example:

```json
{ "word": "serverless", "weight": 15 }
```

RSS Feed URL as in `./config/rss.json`

## Running

> ❗ Remember to [setup transform-hub locally](https://docs.scramjet.org/transform-hub/installation) or use the [platform's environment](https://docs.scramjet.org/platform/get-started/) for the sequence deployment.

Open the terminal and run the following commands:

```bash
# install dependencies
npm install

# transpile TS->JS to dist/
npm run build

# make a compressed package with Sequence
si seq pack dist

# send Sequence to transform hub, this will output Sequence ID
si seq send dist.tar.gz

# start a Sequence, this will output Instance ID. Provide slack webhook URL as input parameter
si seq start - --args [\"SLACK_WEBHOOK_URL\"]

# See output - actual output will be send to slack channel
si inst output -
"GETTING RSS LINKS...\n"
"GETTING RSS LINKS...\n"
"GETTING RSS LINKS...\n"
"GETTING RSS LINKS...\n"

# Optional commands below:

# Check console.log messages
si inst stdout -

# Check console.error messages
si inst stderr -
```

As this is scraping content on regular basis `429 Too Many Requests` Error is inevitable. In order to mitigate this problem, increase pause between requests.
