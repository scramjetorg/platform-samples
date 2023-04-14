import asyncio
import aiohttp
from scramjet.streams import Stream

class CO2SignalDataFetcher:

    def __init__(self, auth_token: str, country_codes: list, delay: int = 60) -> None:
        self._headers = {'accept': 'application/json',
                         'auth-token': '{}'.format(auth_token)}
        self._url = 'https://api.co2signal.com/v1/'

        self._country_codes = country_codes if isinstance(country_codes,list) else []
        self._delay = int(delay) if int(delay) > 60 else 60
        self._client_session = aiohttp.ClientSession()

    async def _get_latest_measurement(self, country_code: str) -> dict:
        url = f'{self._url}latest?countryCode={country_code}'
        resp = await self._client_session.get(url,  headers=self._headers)
        return await resp.json() if resp.status == 200 else {}

    async def prepare(self, stream: Stream) -> None:
        while True:
            for country in self._country_codes:
                latest_measurement = await self._get_latest_measurement(country)
                if latest_measurement and latest_measurement['status'] == 'ok':
                    stream.write(f'Date: {latest_measurement["data"]["datetime"]} |'
                                f'Country: {latest_measurement["countryCode"]} |'
                                f'CO2 emission : {latest_measurement["data"]["carbonIntensity"]} {latest_measurement["units"]["carbonIntensity"]}')
            await asyncio.sleep(self._delay)


async def fetch_task(auth_token: str, country_codes: list, delay: int, stream: Stream) -> None:

    await CO2SignalDataFetcher(auth_token, country_codes, delay).prepare(stream)


async def run(context, input, *args) -> Stream:

    run.TOPIC = context.config['topic']
    auth_token = context.config['auth_token']
    country_codes = context.config['country_codes']
    delay = context.config['delay']

    stream = Stream()

    asyncio.create_task(fetch_task(auth_token, country_codes, delay, stream))

    return stream.map(lambda s: s+'\n')
