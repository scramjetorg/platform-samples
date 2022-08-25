# Slack Read

___

Read messages from Slack and write to topic. This Sequence is a topic provider, it writes data under a topic name `messages-slack-outbound` in `"application/x-ndjson"` content type.

In order to read messages from Slack you need to create application first. Go to [Slack API](https://api.slack.com/apps) and `Create New App`.
Next, select your app and under `Settings` -> select `Socket Mode`.
Enable Socket Mode as per message:

> To start receiving payloads in Socket Mode, turn on the toggle below and call the apps.connections.open endpoint using an App Level Token to establish a connection.

After enabling socket mode, follow link to App Level Tokens, scroll down to `App-Level Tokens` and generate new token. Give it a name and select scope: `connections:write`.

Copy SOCKET_MODE_TOKEN. It will look like: `xapp-1-A....` and save it on your disc, you will need it later on.

## Running

> ❗ Remember to [setup transform-hub locally](https://docs.scramjet.org/platform/self-hosted-installation) or use the [platform's environment](https://docs.scramjet.org/platform/quick-start) for the sequence deployment.

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

# start a Sequence, provide SOCKET_MODE_TOKEN as the second parameter
si seq start - --args [\"SOCKET_MODE_TOKEN\"]

# check Slack connection status displayed via stdout stream
si inst stdout -

# view messages in topic
si topic get messages-slack-outbound
```
