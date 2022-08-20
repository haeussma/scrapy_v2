from time import time
from scrapy.utils.util import utility_function
import logging


def do_something(now: str) -> str:
    utility = utility_function()
    if len(utility) > 0:
        logging.info("utility succesfully imported")
    else:
        logging.critical("utility not imported!")

    return f"Doing something with {utility} at {now}"
