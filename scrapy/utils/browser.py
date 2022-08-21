from dataclasses import dataclass
import platform
import time

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from browsermobproxy import Server



class Browser:

    def __init__(self, use_proxy: bool = False) -> None:
        self.use_proxy = use_proxy
        self.driver = self.startDriver()

    def startDriver(self) -> webdriver.Chrome:

            chrome_service = Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())

            if self.use_proxy:
                self.startProxy()

            chrome_options = Options()
            options = [
                "--headless",
                "--disable-gpu",
                "--window-size=1200,1920",
                "--ignore-certificate-errors",
                "--disable-extensions",
                "--no-sandbox",
                "--disable-dev-shm-usage"
            ]
            if self.use_proxy:
                options.append(
                    '--proxy-server={host}:{port}'.format(host='localhost', port=self.proxy.port))
                options.append(
                    "disable-extensions"
                )

            for option in options:
                chrome_options.add_argument(option)

            driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

            return driver


    def startProxy(self):

        system_platform = platform.system()

        if system_platform  == "Darwin":
            browsermob_path = "/Users/maxhaussler/Downloads/browsermob-proxy-2.1.42/bin/browsermob-proxy"
        elif system_platform == "Linux":
            browsermob_path = "/home/runner/browsermob-proxy-2.1.4/bin/browsermob-proxy"
        else:
            raise SystemError("System not found: browsermob-proxy path could not be provided.")

        self.server = Server(browsermob_path)
        self.server.start()
        self.proxy = self.server.create_proxy()


    
    def scroll(self):
        scroll_pause_time = 1

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
    import time

    browser = Browser(use_proxy=True)
    

    url = "https://soundcloud.com/akronymcollective/tracks" 
    browser.driver.get(url)
    time.sleep(1)
    browser.scroll()


    soundlist = driver.find_elements(By.CLASS_NAME, "soundList__item")
    print(len(soundlist))