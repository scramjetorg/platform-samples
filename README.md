# Samples

Try out our samples prepared for you. We differentiated them according to the language in which they were written.

Every sample contains a short readme with a guidance describing the procedure for running the example. The execution will be performed from the command line using our CLI, which full description and documentation you will find [here](https://docs.scramjet.org/platform/cli-reference).

## Python samples

Python packages work in a similar way to all the others. They need to pack the dependencies and carry over anything they may need to run the program. They also need a `package.json` file.

- [kafka-transformer](python/kafka-transformer/) - Sequence sending data to any Kafka topic
- [kafka-consumer](python/kafka-consumer/) - Sequence fetching data from any Kafka topic
- [voice-recognition](python/voice-recognition) - a sample Sequence that performs voice recognition in real time.
- [gh-issues-to-clickup](python/gh-issues-to-clickup) - a sample that allows pushing github issues to clickup
- [markdown-keywords](python/markdown-keywords) - a sample that accepts a markdown and extracts keywords from that markdown

## JavaScript samples

JavaScript packages are pretty straight forward in use. After the dependency installation is performed inside the Sequence package it is ready to be compressed and sent to STH.

- [hello](javascript/hello) - Sequence that modifies incoming stream of strings by saying "Hello".
- [hello-snowman](javascript/hello-snowman) - Sequence that reads incoming stream, and modifies it by adding a text message according to the incoming data.
- [simple-counter-js](javascript/simple-counter-js) - Sequence, that counts to 1000, and logs the number in one-second intervals.
- [test-output](javascript/test-output) - Sequence that simply writes random values to the output stream.
- [json-url-stdout](javascript/json-url-stdout/) - Make a real-time JSON API scraper (stdout version)
- [json-url-output](javascript/json-url-output/) - Make a real-time JSON API scraper (output version)

## TypeScript samples

TypeScript compiles to JavaScript. It means that TypeScript packages except dependency installation also need to be compiled. We added a `build` and `postbuild` scripts to every `package.json` in TypeScript packages, which are responsible for compiling files into a `dist` folder and coping `package.json` file into the `dist` folder. In effect, it is the `dist` folder, that becomes the Sequence package, ready to be compressed and sent to STH.

- [crypto-prices](typescript/crypto-prices) - Sequence that keeps printing current crypto prices for a provided pair of currencies every 3s.
- [slack-write](typescript/slack-write/) - Write incoming data to a slack channel
- [slack-read](typescript/slack-read/) - Read data from Slack
- [discord-write](typescript/discord-write/) - Write to Discord
- [discord-read](typescript/discord-read/) - Read from Discord
- [mediawiki](typescript/mediawiki) - Sequence that keeps printing mediawiki event stream.
- [rss](typescript/rss) - Sequence that gets a list of RSS and then retrieves each feed and passes links to scraper.
- [write-to-database](typescript/write-to-database/) - Write incoming data to a database table
- [scraping](typescript/scraping) - Sequence that scrapes web pages.
- [stack-overflow](typescript/stack-overflow) - Sequence that gets a number of changes in Stack Overflow tag count.
- [transform-string-stream](typescript/transform-string-stream) - Sequence that modifies incoming stream of strings by adding a prefix and a suffix.
- [read-targz-stats](typescript/read-targz-stats/) - Stream through tar.gz file and output stats
- [send-to-github](typescript/send-to-github/) - Write incoming data to a file on github
- [linkedin](typescript/linkedin/) - Enrich csv data with Linkedin via RapidAPI
- [hexdump](typescript/hexdump/) -Sequence returns input in hex format.

## Guides and complex examples

- [kafka-setup](guides/kafka-setup/) - how to set up a kafka instance and consume data from it with Scramjet Cloud Platform
- [discord-slack-connection](guides/discord-slack-connection/) - how to interconnect discord and slack with Scramjet Cloud Platform
