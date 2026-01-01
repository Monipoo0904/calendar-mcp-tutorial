import asyncio
from api.mcp import handler


class Req:
    method = "POST"
    json = {
        "tool": "add_event",
        "input": {
            "title": "Demo",
            "date": "2026-01-01",
            "description": "Test event"
        }
    }


async def main():
    response = await handler(Req())
    print(response)


asyncio.run(main())

