# Slack Write

___

Read messages from topic and write to Slack. This Sequence is a topic consumer, to make it work you need start another Sequence → sample [discord-read](../discord-read/) that provides topic data  under topic name `"messages-slack-inbound"`.

In order to get SLACK_WEBHOOK_URL you need to create application in Slack first.
Please refer to notes in [slack-read](../slack-read/) example.

Once you have an application in Slack. Open it and under Features select `Incoming Webhooks`

Activate incoming webhooks and add a new webhook to workspace by clicking on `Add New Webhook to Workspace` button. Follow prompts and select which channel you want to use.

Copy Webhook URL and save, it will be used later as `SLACK_WEBHOOK_URL` in the notes below.

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

# start a Sequence, provide SLACK_WEBHOOK_URL as the second parameter
si seq start - --args [\"SLACK_WEBHOOK_URL\"]

# now type some messages in Discord, you should see them send and displayed in Slack on the dedicated #channel
```
