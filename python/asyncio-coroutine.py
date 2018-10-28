import asyncio
import time

async def add_42(number):
    print("Adding 42")
    return 42 + number


async def hello_world():
    print("Hello world!")
    result = await add_42(23)
    time.sleep(5)
    return result


event_loop = asyncio.get_event_loop()

try:
    result = event_loop.run_until_complete(hello_world())
    print(result)
finally:
    event_loop.close()