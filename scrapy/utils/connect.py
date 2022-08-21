import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

class Scraper:

    def __init__(self) -> None:
        self.driver: webdriver.Chrome = self.openBrowser()

    def openBrowser(self) -> webdriver.Chrome:

        chrome_service = Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())

        chrome_options = Options()
        options = [
            "--headless",
            "--disable-gpu",
            "--window-size=1920,1200",
            "--ignore-certificate-errors",
            "--disable-extensions",
            "--no-sandbox",
            "--disable-dev-shm-usage"
        ]
        for option in options:
            chrome_options.add_argument(option)

        driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

        return driver

    def scroll(self):

        scroll_pause_time = 1.1

        # Get scroll height
        last_height = self.driver.execute_script("return document.body.scrollHeight")

        while True:
            # Scroll down to bottom
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            time.sleep(scroll_pause_time)

            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height


if __name__ == "__main__":
    import platform
    import time
    import json
    from scrapy.utils.browser import Browser

    browser = Browser(use_proxy=True)

    browser.proxy.new_har('req', options={'captureHeaders': False, 'captureContent': True})
    

    url = "https://open.spotify.com/album/6Vi07YHPostxvPacTCESEW" 
    browser.driver.get(url)
    time.sleep(5)

    result = browser.proxy.har

    for i in range(len(result["log"]["entries"])):
        if "text" in result["log"]["entries"][i]["response"]["content"].keys():
            subdata = result["log"]["entries"][i]["response"]["content"]["text"]

            if "{\"data\":{\"album\":{\"playability\":{\"playable\":true}" in subdata:
                subdata_dict = json.loads(subdata)

                for track_item in subdata_dict['data']['album']['tracks']['items']:
                        print(f"name: {track_item['track']['name']}")
                        print(f"plays: {track_item['track']['playcount']}")
                        #artist = track_item['track']['artists']['artists']['items'][0]["profile"]["name"]



    #total_plays = 0
    #for element in soundlist:

    #    title = element.find_element(By.CLASS_NAME, "soundTitle__title")
     #   print(f"Title: {title.text}")

    #    plays = element.find_element(By.CLASS_NAME, "sc-ministats-plays")
     #   plays = int(plays.text.split("\n")[0].split(" ")[0].replace(",", ""))
      #  print(f"Plays: {plays}")
       # total_plays += plays

    #print(f"total play: {total_plays}")