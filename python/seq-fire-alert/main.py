import asyncio
from scramjet.streams import Stream
import aiohttp
import os


API_BASE = 'https://forestapi.bieda.it'
IMAGE_DIR = '/Users/spiderman/raspberry-pi-dash/seq-fire-alert/images'

provides = {
   'provides': 'fire',
   'contentType': 'text/plain'
}

def get_bytes(path):
    with open(path, 'rb') as f:
        data = f.read()
    return data

async def post(data, url):
    async with aiohttp.ClientSession() as session:
        form_data = aiohttp.FormData()
        form_data.add_field('file', data)
        url = f'{API_BASE}/{url}'
        async with session.post(url, data=form_data) as response:
            return await response.json()

async def main(stream):
    for file in os.listdir(f'{IMAGE_DIR}'):
        image = get_bytes(f'{IMAGE_DIR}/{file}')
        response = await post(image, 'predict')
        stream.write([response])
        stream.write(['some actions...'])
        await asyncio.sleep(3)

async def run(context, input):
    stream = Stream()
    asyncio.gather(main(stream), return_exceptions=True)
    return stream.map(lambda x : str(x) + "\n")



