from scramjet.streams import Stream


async def run(context, input):
    # create a clean output stream
    stream = Stream()

    # write some data to the output stream
    stream.write("Hello World!")

    # return the output stream so it can be consumed (e.g. by CLI client)
    return stream
