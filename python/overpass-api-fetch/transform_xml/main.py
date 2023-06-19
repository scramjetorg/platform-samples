from transform_xml import transform_xml_data

# topic to get data from
requires = {
   'requires': 'structures-xml',
   'contentType': 'text/plain'
}
end_tag = '</osm>'


async def run(context, input):
    while True:
        chunks = []

        async for chunk in input:
            chunks.append(chunk)

            if end_tag in chunk:
                break

        xml_file = transform_xml_data(''.join(chunks))
        context.logger.info('Transformed xml file')
        # save to e.g. database...
