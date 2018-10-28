import asyncio


async def hello_world():
    print("Hello World")
    return 42


hello_world_coroutine = hello_world()

print(hello_world_coroutine)

event_loop = asyncio.get_event_loop()
try:
    print("entering event loop")
    result = event_loop.run_until_complete(hello_world_coroutine)
    print(result)
finally:
    event_loop.close()