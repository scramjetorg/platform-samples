from scramjet.streams import Stream
import yake

import re


class Extractor:
    code_block = False
    kw_extractor = yake.KeywordExtractor(top=3, stopwords=None)

    re_hashtag = r"^#+\ .*$"

    def identify_headers(data):
        if re.search(Extractor.re_hashtag, data):
            keywords = Extractor.kw_extractor.extract_keywords(data)
            print(keywords)


async def run(context, input):
    return (
        Stream
            .read_from(input, max_parallel=1)
            .each(Extractor.identify_headers)
    )
