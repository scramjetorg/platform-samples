import requests

# topic to send data to
provides = {
   'provides': 'structures-xml',
   'contentType': 'text/plain'
}
import time

def fetch_tall_structures(min_lat, min_lon, max_lat, max_lon, height=50):
    overpass_url = "http://overpass-api.de/api/interpreter"
    query = f"""
        [out:xml];
        (
            way(if:number(t["height"]) > {int(height)})({min_lat},{min_lon},{max_lat},{max_lon});
        );
        out geom;
    """
    resp = requests.get(overpass_url, params={'data': query})
    print(resp.text)
    return resp.text


async def run(context, input):
    context.logger.info('Waiting for coordinates...')

    return input.map(lambda x: fetch_tall_structures(*(x.split())))
