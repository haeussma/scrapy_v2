from abc import ABC, abstractmethod
from datetime import datetime
from pydantic import BaseModel, Field
from typing import List, Optional

from scrapy.utils.enums import Attribute, Type, Platform
from scrapy.utils.browser import ProxyBrowser, StandardBrowser


class Scraper(BaseModel, ABC):

    date: str = Field(
        ...,
        description="Date of data aquisition.",
    )

    time: str = Field(
        ...,
        description="Time of data aquisition"
    )

    platform: Platform = Field(
        ...,
        description="Platform of data aquisition."
    )

    type: Type = Field(
        ...,
        description="Type of the track (Podcast, Track, Clip)"
    )

    track_name: str = Field(
        ...,
        description="Name of the track."
    )

    track_artist: str | List[str] = Field(
        ...,
        description="Artist(s) of the track."  
    )

    album_name: Optional[str] = Field(
        None,
        description="Album name of the track."
    )

    plays: int = Field(
        ...,
        description="Play count of the track."
    )

class SpotifyScraper(Scraper):

    length: int = Field(
        ...,
        description="Length of track in ms."
    )

    @classmethod
    def from_URL(cls, browser: ProxyBrowser, urls: List[str]) -> "List[SpotifyScraper]":

        # Check if url is valid spotify url
        #
        #

        # Iterate over urls and extract data
        list_of_scrapes = []

        for url in urls:
            data = browser(url).getData()

            # Extract data
            #
            #

            # Initialize Scrape instance with extracted data
            list_of_scrapes.append(cls(
                date=str(datetime.date(datetime.now())),
                time=str(datetime.time(datetime.now())),
                platform=Platform.SPOTIFY
            ))


        return list_of_scrapes

class SoundCloudScraper(Scraper):
    pass

class YoutubeScraper(Scraper):
    pass

if __name__ == "__main__":
    scrape = SpotifyScraper(
        date = str(datetime.date(datetime.now())),
        time = str(datetime.time(datetime.now())),
        track_name="J'áchete le pain dans la boulangerie âpres le sixième siècle",
        track_artist="maxmix",
        plays=12345,
        platform=Platform.SPOTIFY,
        type=Type.TRACK,
        length=324524
    )

    print(scrape)


