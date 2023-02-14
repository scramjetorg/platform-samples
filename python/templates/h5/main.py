from scramjet.streams import Stream


async def run(context, input):
	return input.each(lambda variable: variable)
