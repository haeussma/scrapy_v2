from abc import ABC, abstractmethod
from enums import Attribute
from scrapy.utils.browser import Browser

class Scraper(ABC):
    url: str
    browser: Browser


class SoundCloudScraper:
    def __init__(self) -> None:
        pass

    
    
    
    
    def __init__(self, browser: Browser, urls: str) -> None:
        pass




if __name__ == "__main__":
