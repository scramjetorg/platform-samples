# Audio to Text 

This Sequence transcribes an audio file to a text using AssemblyAI API.
The example audio file is provided with this sample, replacing this audio file with another is possible but the file must be renamed to `song.wav`.<br/>
The audio file 
<a href="https://salford.figshare.com/collections/HARVARD_speech_corpus_-_audio_recording_2019/4437578" target="_blank">`song.wav`</a> is licensed under the Creative Commons Attribution-NonCommercial 4.0 International License.

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
# Create directory __pypackages__ in the same directory as main.py
mkdir __pypackages__

# Install dependencies in the __pypackages__ folder. 
pip3 install -t __pypackages__ -r requirements.txt

# Pack the Sequence into a gzip format
si seq pack audio2text

# Send the Sequence to the Transform-Hub, with a return <Sequence-id> value
si seq send audio2text.tar.gz

# Start a Sequence, with the AssemblyAi-key as an argument parameter
si seq start <Sequence-id> --args [\"<AssemblyAI-token>\"]

# Transcription of the audio file as text output
si inst output <Instance-id>
```
