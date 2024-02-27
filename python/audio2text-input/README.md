# Audio to Text Sequence

This Sequence demonstrates how to turn voice data into summaries with <a href="https://www.assemblyai.com/" target="_blank">AssemblyAI</a> Speech models. Audio is sent to Scramjet Transform Hub using data streaming with an audio transcript as an output.


Requirements
For this Sequence to run properly on your Linux machine use the following command to start <a href="https://docs.scramjet.org/transform-hub/installation" target="_blank">STH</a>.

```bash
$ DEVELOPMENT=true sth --runtime-adapter=process
```

**NOTE:** To run this Sequence, you'll need your <a href="https://www.assemblyai.com/" target="_blank">AssemblyAI</a> token, which must be included when executing the **si** start command


## Install and Run

Install the <a href="https://docs.scramjet.org/platform/self-hosted-installation/" target="_blank">Scramjet Transform Hub </a> (STH) locally or use 
<a href="https://docs.scramjet.org/platform/get-started/" target="_blank">Scramjet's Cloud Platform</a> environment for the Sequence deployment.
For more information on the below commands check the 
<a href="https://docs.scramjet.org/platform/cli-reference/#useful-commands" target="_blank">CLI reference</a> section on Scramjet's Website.

On the Linux terminal execute the following commands:

```bash
# Create a directory __pypackages__ in the same directory as main.py
~/audio2text-input$ mkdir __pypackages__

# Install dependencies in the __pypackages__ folder. 
~/audio2text-input$ pip3 install -t __pypackages__ -r requirements.txt

# Pack the audio2text-input folder into a gzip format
~$ si sequence pack audio2text-input

# Send the audio2text-input.tar.gz Sequence to the Scramjet's Transform-Hub, with a return <Sequence-id> value
~$ si sequence send audio2text-input.tar.gz --progress

# Start the Sequence with argument, you'll need your AssemblyAI token
~$ si seq start <Sequence-id> --args=[\"token\"] 

# Send the audio file as input
~$ si instance input <Instance-id> local/path/to/audio.wav -e -t application/octet-stream

# Return transcript from AssemblyAI as output
~$ si instance output <Instance-id>
```

--- 