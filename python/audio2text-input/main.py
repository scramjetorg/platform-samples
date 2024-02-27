import requests
import time
from scramjet.streams import Stream
import json

async def run(context, input, args1):
    audio_file = await input.reduce(lambda a, b: a+b)
    base_url = "https://api.assemblyai.com/v2"

    headers = {
        "authorization": args1
    }

    response = requests.post(
        base_url + "/upload",
        headers=headers,
        data=audio_file 
    )
    upload_url = response.json()["upload_url"]
    data = {
        "audio_url": upload_url  
    }
    url = base_url + "/transcript"
    response = requests.post(url, json=data, headers=headers)

    transcript_id = response.json()['id']
    polling_endpoint = f"https://api.assemblyai.com/v2/transcript/{transcript_id}"

    while True:
        transcription_result = requests.get(polling_endpoint, headers=headers).json()

        if transcription_result['status'] == 'completed':
            break

        elif transcription_result['status'] == 'error':
            raise RuntimeError(f"Transcription failed: {transcription_result['error']}")

        else:
            time.sleep(3)


    return Stream.read_from(f"{transcription_result['text']} \n")