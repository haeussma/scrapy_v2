from time import time
from scrapy.utils.util import random_word
import logging


def do_something(now: str) -> str:
    utility = random_word()
    if len(utility) < 3:
        logging.info("utility succesfully imported")
    #else:
        logging.critical(f"Short word: {utility}!")

    time = now
    text = f"Doing something with #{utility}# at {now}"

    return [time, text]
