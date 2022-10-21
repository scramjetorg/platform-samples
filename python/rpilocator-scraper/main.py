import asyncio
import feedparser
from scramjet.streams import Stream


# it will send data to the specified Topic
provides = {
    'provides': 'exampletopicname',
    'contentType': 'text/plain'
}

# specify models:
MODELS = "CM4,PI4,PIZERO"

# and regions:
REGIONS = "UK,DE,PL"

# and delay, min. 60 [seconds]
DELAY = 60

URL = f"https://rpilocator.com/feed/?country={REGIONS}&cat={MODELS}"

async def scrape_rp(stream):
    first_check = feedparser.parse(URL).entries
    stock_ids=[]

    for entry in first_check:
        stock_ids.append(entry.id)
        stream.write(entry.title[18:] + "| URL: " + entry.link)
        
    await asyncio.sleep(DELAY)

    while True:
        new_data = feedparser.parse(URL).entries
        for entry in new_data:
            if entry.guid not in stock_ids:
                stock_ids.append(entry.guid)
                stream.write(entry.title + "| URL: " + entry.link)
        await asyncio.sleep(DELAY)

async def run(context, input):
    stream = Stream()
    asyncio.create_task(scrape_rp(stream))
    return stream.map(lambda s: s+'\n')
