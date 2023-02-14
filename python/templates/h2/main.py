def func():
	return "Hello World"

async def run(context, input):
   yield func()
