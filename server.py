#!/usr/bin/env python3
import aiohttp
import aiohttp.server
import asyncio
import logging
import http.server
from urllib.parse import urlparse, parse_qs

import common
import config
import knowledge_engine

_knowledge_engine = None


class QuestionHandler(aiohttp.server.ServerHttpProtocol):

    @asyncio.coroutine
    def handle_request(self, message, payload):
        params = parse_qs(message.path[2:])
        question = params.get("question", [None])[0]

        logging.debug("params: %r, question: %s", params, question)
        if not message.path.startswith("/?") or question is None:
            answer = "Invalid request"
            code = 404
        else:
            _knowledge_engine = knowledge_engine.KnowledgeEngine()
            answer = yield from _knowledge_engine.getAnswer(question)
            code = 200

        logging.debug("Will send response '%s', code %d", answer, code)

        content = "{}\r\n".format(answer).encode(config.ENCODING)
        response = aiohttp.Response(self.writer, code, http_version=message.version)
        response.add_header(
            "ContentType", "text/plain; charset={}".format(config.ENCODING))
        response.add_header("ContentLength", str(len(answer)))

        response.send_headers()
        response.write(content)

        yield from response.write_eof()


def main():
    common.setup_logging("talk_asyncio_server", level=logging.DEBUG)

    loop = asyncio.get_event_loop()
    server_future = loop.create_server(
        QuestionHandler, config.SERVER_HOST, config.SERVER_PORT
    )
    loop.run_until_complete(server_future)

    logging.info("Starting server...")

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    except Exception as ex:
        logging.error("Error in execution: %s", ex)


if __name__ == "__main__":
    main()
