from scramjet.streams import Stream

async def run(context, input):
	stream  = Stream()
	stream.write("Hello World")
	return stream.map(lambda variable : variable)
