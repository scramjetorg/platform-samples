
import time
import requests
from scramjet.streams import Stream


class AssemblyAi():

    def __init__(self, token: str, file: str):
        self.token = token
        self.file = file

    def transcript(self):
        base_url = "https://api.assemblyai.com/v2"

        headers = {
            "authorization": self.token  
        }

        with open(self.file, "rb") as f:
            response = requests.post(
                base_url + "/upload",
                headers=headers,
                data=f)

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
        self.transcription_result = transcription_result
        return transcription_result


def run(context, input, args):
    file = "song.wav" 
    key = args
    
    try:
        audio_1 = AssemblyAi(key, file)
        aud_txt = audio_1.transcript()
        
    except RuntimeError as e:
        context.logger.info(f"Error: {str(e)}")
        
    else:
        return Stream.read_from(f"Audio Transcription: {aud_txt['text']} \n")



