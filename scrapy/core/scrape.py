from abc import ABC, abstractmethod
from argparse import _UNRECOGNIZED_ARGS_ATTR
from datetime import datetime
from multiprocessing.sharedctypes import Value
from platform import platform
from pydantic import BaseModel, Field
from typing import List, Optional
import json, time


from scrapy.utils.enums import Attribute, Type, Platform
from scrapy.utils.browser import Browser, ProxyBrowser


class Scraper(BaseModel, ABC):

    timestamp: str = Field(
        ...,
        description="Date of data aquisition.",
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

    track_artist: list[str] = Field(
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

    duration: int = Field(
        ...,
        description="Length of track in ms."
    )

    @classmethod
    def from_URL(cls, urls: List[str]) -> "List[SpotifyScraper]":
        platform = Platform.SPOTIFY.value

        # Check if url is valid spotify url
        for url in urls:
            try:
                if platform in url:
                    pass
            except ValueError as e:
                f"Provided URL {url} does not match platform {platform}"

        # Iterate over urls and extract data
        list_of_scrapes = []

        for num, url in enumerate(urls):
            browser = ProxyBrowser()
            browser.openURL(url)
            har_response = browser.getHar()
            album_name = browser.findElement("h1.Type__TypeElement-goli3j-0")


            # Extract data
            for i in range(len(har_response["log"]["entries"])):
                if "text" in har_response["log"]["entries"][i]["response"]["content"].keys():
                    subdata = har_response["log"]["entries"][i]["response"]["content"]["text"]

                    if "{\"data\":{\"album\":{\"playability\":{\"playable\":true}" in subdata:
                        subdata_dict = json.loads(subdata)

                        for track_item in subdata_dict['data']['album']['tracks']['items']:
                            track_name = track_item['track']['name']
                            plays = track_item['track']['playcount']
                            track_artist = [x["profile"]["name"] for x in track_item['track']['artists']["items"]]
                            duration = track_item['track']['duration']["totalMilliseconds"]

                            # Initialize Scrape instance with extracted data
                            list_of_scrapes.append(cls(
                                timestamp=datetime.now().ctime(),
                                platform=Platform.SPOTIFY,
                                type=Type.TRACK,
                                album_name=album_name,
                                track_artist=track_artist,
                                track_name=track_name,
                                plays=plays,
                                duration=duration
                            ))
                            print(list_of_scrapes[-1])

            print(f"Scraping album {num+1} finnished.")
        browser.close()



        return list_of_scrapes

class SoundCloudScraper(Scraper):
    pass

class YoutubeScraper(Scraper):
    pass

if __name__ == "__main__":
    urls = [
        "https://open.spotify.com/album/08zsw1AY0mZdfJQMGxb0nZ",
        "https://open.spotify.com/album/3uPnO1aZBwMgWK1DI5zve9",
        "https://open.spotify.com/album/1dvekhJPaROZQ5j6MRP0TH",
        "https://open.spotify.com/album/1Aa7MMQ3VXZH28wURtApo0",
        #"https://open.spotify.com/album/3bBLnNMW2k5XbZyzsyIQUk",
        #"https://open.spotify.com/album/7ebrRMbLDEU5kBycQUNjCM",
        #"https://open.spotify.com/album/12opSVMxNXryWQVzdmu9mm",
        #"https://open.spotify.com/album/5jC7MjpviHV3IkEjtS9iV3",
        #"https://open.spotify.com/album/314tOEIdTMCWt0HjGOagt7",
        #"https://open.spotify.com/album/3ihkDxBRnocXB9VsTzuyf6",
        #"https://open.spotify.com/album/38gm6VGs4uuEbWO6Bj5elO",
        #"https://open.spotify.com/album/6PHtfmP1NJk0Wx3efAGuYA",
        #"https://open.spotify.com/album/7LrJEtnQzA1sAeMxRMGDqj",
        #"https://open.spotify.com/album/1z5xJdmnKmnidKfT6x1IUG",
        #"https://open.spotify.com/album/05KJcT7QPUcXp20teI61PW",
        #"https://open.spotify.com/album/6dQXvUxuZWWYGYnY6hasNo",
        #"https://open.spotify.com/album/3aw2QCVglkQ3dUBPZKkDRA",
        #"https://open.spotify.com/album/56wfN8bWMePGYI5ohYW85i",
    ]
    scrape = SpotifyScraper.from_URL(urls)



