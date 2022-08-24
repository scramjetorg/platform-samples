# mediawiki

Sequence that keeps printing mediawiki event stream.

## Running

> ❗ Remember to [setup transform-hub locally](https://docs.scramjet.org/platform/self-hosted-installation) or use the [platform's environment](https://docs.scramjet.org/platform/quick-start) for the sequence deployment.

Open the terminal and run the following commands:

```bash
# go to 'mediawiki' directory
cd typescript/mediawiki

# install dependencies
npm install

# transpile TS->JS to dist/
npm run build

# deploy the Sequence from the dist/ directory, which contains transpiled code, package.json and node_modules
si seq deploy dist

# See output
si inst output -

# Check console.log messages
si inst stdout -

# Check console.error messages
si inst stderr -

# Send event, e.g. `drain`: `si inst emit <instance-id> drain "{}"`
si inst event emit - <event> <payload>
```

> 💡**NOTE:** Command `deploy` performs three actions at once: `pack`, `send` and `start` the Sequence. It is the same as if you would run those three commands separately:

```bash
si seq pack dist/ -o mediawiki.tar.gz    # compress 'dist/' directory into file named 'mediawiki.tar.gz'

si seq send mediawiki.tar.gz    # send packed Sequence to STH, this will output Sequence ID

si seq start - --args [\"<search>\"]   # start the Sequence, this will output Instance ID. Search is optional and can be used to filter out results, e.g. "data.server_name === 'en.wikipedia.org'"
```

## Example Event

ID

```json
[
   {
      "topic":"eqiad.mediawiki.recentchange",
      "partition":0,
      "timestamp":1631710626001
   },
   {
      "topic":"codfw.mediawiki.recentchange",
      "partition":0,
      "offset":-1
   }
]
```

DATA

```json
{
   "$schema":"/mediawiki/recentchange/1.0.0",
   "meta":{
      "uri":"https://en.wikipedia.org/wiki/Bernie_Ecclestone",
      "request_id":"41ba28c2-c8ce-4331-9e5d-96ca10e116ef",
      "id":"48ae7d49-e28d-4ad5-9922-d2972e492ab7",
      "dt":"2021-09-15T12:57:06Z",
      "domain":"en.wikipedia.org",
      "stream":"mediawiki.recentchange",
      "topic":"eqiad.mediawiki.recentchange",
      "partition":0,
      "offset":3299628122
   },
   "id":1423007653,
   "type":"edit",
   "namespace":0,
   "title":"Bernie Ecclestone",
   "comment":"/* Racial statement */Fixed typo",
   "timestamp":1631710626,
   "user":"2A02:C7F:2CA7:F700:DC87:1AF6:9C2B:4497",
   "bot":false,
   "minor":false,
   "length":{
      "old":59388,
      "new":59393
   },
   "revision":{
      "old":1043848398,
      "new":1044480964
   },
   "server_url":"https://en.wikipedia.org",
   "server_name":"en.wikipedia.org",
   "server_script_path":"/w",
   "wiki":"enwiki",
   "parsedcomment":"<span dir=\"auto\"><span class=\"autocomment\"><a href=\"/wiki/Bernie_Ecclestone#Racial_statement\" title=\"Bernie Ecclestone\">→‎Racial statement</a>: </span>Fixed typo</span>"
}
```
