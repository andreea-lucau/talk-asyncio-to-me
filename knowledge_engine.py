import asyncio
import logging
import random


class KnowledgeEngine():
    MIN_THINKING_TIME = 1
    MAX_THINKING_TIME = 10

    def __init__(self):
        pass

    @asyncio.coroutine
    def getAnswer(self, question):
        thinking_time = random.randint(self.MIN_THINKING_TIME,
                self.MAX_THINKING_TIME)
        logging.debug("Answering question '%s' after %d seconds",
            question, thinking_time)
        yield from asyncio.sleep(thinking_time)
        return "42"
