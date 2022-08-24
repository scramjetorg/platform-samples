# Discord Read

Read messages from Discord channel and write to topic. This Sequence is a topic provider, it writes data under a topic name `messages-slack-inbound` in `"application/x-ndjson"` content type.

[Discord Documentation](https://discord.js.org/#/docs/discord.js/stable/general/welcome)

In order to read messages from Discord we need to create a bot first:

* Go to Developer Portal and click on [Applications](https://discord.com/developers/applications)
* Click on `New Application` button and give it a name. Then click on `Create`.
* In the newly created and selected app, click on `Bot` and click on `Add Bot` button.
* Under `Build-A-Bot` either click on `Click to Reveal Token` link or on `Copy` button to get Discord Bot Token. **This is important!**
* You can uncheck Public Bot.
* You can customize its name and icon.
* Expand `OAuth2` and select `URL Generator`.
* Select `bot` under scopes and `Read Messages/View Channels` under bot permissions. Copy URL.
* Paste the URL into web browser address bar. Connect to Discord message will appear. Select your server from `Add To Server` dropdown and click on `Continue`. If you don't have any servers you need to create one in those simple steps:
    1. Start the Discord app for desktop or smartphone/tablet.
    2. Log into your Discord account.
    3. Click on the plus symbol on the left-hand side of the page.
    4. Select the option “Create a server”.
    5. Enter the name of your new Discord server.
    6. Click on “Create”.
* Confirm permissions on the next screen by clicking `Authorize` button.
* You will get a confirmation saying: *you may now close this window or tab*.

Create a file called `config.json` and add:

```json
{
    "token": "DISCORD_BOT_TOKEN_GOES_HERE"
}
```

Add `config.json` to main directory in `discord-read` sample and follow running process below:

## Running

> ❗ Remember to [setup transform-hub locally](https://docs.scramjet.org/platform/self-hosted-installation) or use the [platform's environment](https://docs.scramjet.org/platform/quick-start) for the sequence deployment.


```bash
# install dependencies
npm install

# transpile TS->JS to dist/
npm run build

# make a compressed package with Sequence
si seq pack dist

# send Sequence to transform hub, this will output Sequence ID
si seq send dist.tar.gz

# start a Sequence
si seq start - -f config.json

# check Discord API connection via stdout stream
si inst stdout -

# type some messages on any channel on your Discord server and view the messages in topic
si topic get messages-slack-inbound
```
