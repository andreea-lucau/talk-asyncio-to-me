# talk-asyncio-to-me

## Requirements

*   asyncio
*   aiohttp
*   Apache Benchmark Tool

## Running

To run the server:

$ python3 server

To run clients:

$ ab -c 1 -n 10 http://localhost:8020/?question=bla
