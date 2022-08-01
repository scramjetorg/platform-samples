# Discord to Slack (and vice versa) Connection

___

### The video that illustrates the execution of the sample is on our [YouTube](https://www.youtube.com/channel/UChgTmKeuAsKj8kDnylkmP6Q) channel [How to Connect Discord and Slack in 4 minutes](https://www.youtube.com/watch?v=y2L1f-f-wLM&t=1s).

___

> 💡 **Please note that the sample below requires some previous installations before you start running it, you will find them [here](../../README.md#3-install-scramjet-transform-hub).**

In this project you will find 4 STH Sequences:

* [discord-read](../../typescript/discord-read/)
* [discord-write](../../typescript/discord-write/)
* [slack-read](../../typescript/slack-read/)
* [slack-write](../../typescript/slack-write/)

You must run at least two (discord-read, slack write or discord-write, slack-read) in order to get one directional communication or all four for bi-directional communication.

Each Sequence either reads or writes to specified application respectively and uses `const TOPIC = ...` topic to exchange data between applications. You need two topics for bi-directional communication.

You can add your own topics at invoke time 

## TODO

As there is no way to map message IDs between the two applications, threads are not supported.

In order to get this working, Sequences must keep a track of posted and written IDs.
