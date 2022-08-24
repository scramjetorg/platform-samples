# Discord Write

___

Read messages from topic and write to Discord via webhook. This Sequence is a topic consumer, to make it work you need start another Sequence → sample [slack-read](../slack-read/) that provides topic data under topic name `"messages-slack-outbound"`.

[Discord Documentation](https://discord.com/developers/docs/resources/webhook)

## Running

Before start you need `DISCORD_WEBHOOK_URL`. In Discord go to your server. Then next to the server name click on the drop down menu and select `Server Settings` -> `Integrations` -> `Webhooks` -> `Create webhook` -> Select channel name and save changes. You can copy webhook URL by clicking on `Copy webhook URL` button.

WebHook URL has following format: `https://discord.com/api/webhooks/{webhook.id}/{webhook.token}` where `webhook.id` are numbers and `webhook.token` are letters and numbers.

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

# start a Sequence, provide DISCORD_WEBHOOK_URL as the second parameter
si seq start - --args [\"DISCORD_WEBHOOK_URL\"]
```
