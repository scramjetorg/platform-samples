# Audio to Text

This Sequence transcribes an audio file to a text using AssemblyAI API.
The example audio file is provided with this sample, replacing this audio file with another is possible but the file must be renamed to `song.wav`.<br/>

___


## Requirements
---
For this Sequence to run properly, it is required to register and acquire an API key from <a href ="https://www.assemblyai.com/" target="_blank">AssemblyAI</a>

## Install and Run
---
Install the <a href="https://docs.scramjet.org/platform/self-hosted-installation/" target="_blank">Transform-Hub</a> locally or use
<a href="https://docs.scramjet.org/platform/get-started/" target="_blank">Scramjet's Cloud Platform</a> environment for the Sequence deployment.
For more information on the below commands check the
<a href="https://docs.scramjet.org/platform/cli-reference/#useful-commands" target="_blank">CLI reference</a> section on Scramjet's Website.

On the terminal run the following commands:

```bash
# install dependencies
npm install

# transpile TS->JS to dist/
npm run build

# make a compressed package with Sequence
si seq pack dist

# send Sequence to transform hub, this will output Sequence ID
si seq send dist.tar.gz

# start a Sequence, provide AssemblyAi-key as an argument parameter
si seq start - --args [\"AssemblyAi-key\"]

# Transcription of the audio file as text output
si inst stdout -
```
