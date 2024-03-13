## Reading from telegram

This is a piece of cake sample which simply forward a last message of a certain telegram channel

It reads messages from **telegram-outbound** Topic.

___
## Prerequisites

You need to [add a bot](https://core.telegram.org/bots#3-how-do-i-create-a-bot) to your Telegram channel which will send messages for you.

The easiest way to achieve that is to follow a few steps given by BotFather here: 

https://t.me/botfather

and type `/newbot`.

After you input a username for your bot, you will see a message from BotFather that includes this part:

`"Use this token to access the HTTP API:`
/token/

`Keep your token secure and store it safely, it can be used by anyone to control your bot."`

**You'll need that token to control the bot.**

Next, you need to find the ID of the channel your bot will send messages to. There are several ways to do this, I'll show the least intrusive one (that doesn't include inviting other bots).

1. Go to https://web.telegram.org
2. Hover over the desired channel
3. Look at the URL, it should look like:
    `https://web.telegram.org/k/#-1636919854`
4. Take the digit part, add `-100` to the beggining:
```
-1001636919854   # That's your channel ID!
```
Now open `config.json` file and paste your **bot token** and **channel id**:
```
{
    "credentials": {
        "token": "Put-Token-here",
        "channel": "Put-ChannelID-here"
    }
}

At last, our bot must be added to the desired channel. In the Telegram client:

1. Inside the channel, click the 3-dotted line in the right upper corner.
2. Click on "Manage channel" -> "Administrators" -> "Add Administrator".
3. Type in your bot's name and click on it.
4. Hit 'save'.

```

## Running
> 💡**NOTE:** Packaging of Python Sequences is not very "pythonic" for now. If you have any idea, how we should resolve it for your comfort, please let us know [here](https://github.com/scramjetorg/transform-hub/issues/598).

> ❗ Remember to [setup transform-hub locally](https://docs.scramjet.org/transform-hub/installation) or use the [platform's environment](https://docs.scramjet.org/platform/get-started/) for the sequence deployment.

Open the terminal and run the following commands:

```bash
# Make sure you are inside 'telegram-read-last' directory, otherwise:
cd python/telegram-read-last

# Install dependencies
npm run build

# Deploy sample to STH
si seq deploy dist -f config.json


# Get last message from tg with:

si topic get <your topic name>

# Typing "stop" in tg channel terminate the sequence

```



