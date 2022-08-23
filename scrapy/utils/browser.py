from abc import ABC, abstractmethod
import psutil, signal, time, platform
from contextlib import suppress

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from browsermobproxy import Server


# TODO browser
class Browser(ABC):
    url: str
    driver: webdriver.Chrome

    @abstractmethod
    def startBrowser(self) -> webdriver.Chrome:
        """Downloads and setups Chrome webdriver."""

    @abstractmethod
    def openURL(self) -> None:
        """Navigates to URL."""
        self.driver.get(self.url)

    @abstractmethod
    def getData(self) -> webdriver.Chrome:
        """Export loaded Webpage with loaded page"""

    @abstractmethod
    def close(self):
        """Closes Browser and quits all connections."""



class StandardBrowser(Browser):
    def __init__(self, url: str) -> None:
        self.url = url
        self.driver: webdriver.Chrome = self.startBrowser()
        self.openURL()
        self.scroll()

    def startBrowser(self) -> webdriver.Chrome:

            # TODO browser needs to be installed only once
            chrome_service = Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())

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

            for option in options:
                chrome_options.add_argument(option)

            driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
            return driver


    def openURL(self) -> None:
        super().openURL()

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

    def getData(self) -> webdriver.Chrome:
            return self.driver

    def findElement(self, css_selector: str) -> str:
        super().findElement(css_selector)

    def close(self) -> None:
        self.driver.close()


class ProxyBrowser(Browser):
    def __init__(self, url: str) -> None:
        self.url = url
        self.startProxy()
        self.driver: webdriver.Chrome = self.startBrowser()
        self.openURL()

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

    def startBrowser(self) -> webdriver.Chrome:
        chrome_service = Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())

        self.proxy.new_har('req', options={'captureHeaders': False, 'captureContent': True})

        chrome_options = Options()
        options = [
            "--headless",
            "--disable-gpu",
            "--window-size=1200,1920",
            "--ignore-certificate-errors",
            "--disable-extensions",
            "--no-sandbox",
            "--disable-dev-shm-usage",
            "disable-extensions",
            '--proxy-server={host}:{port}'.format(host='localhost', port=self.proxy.port)
        ]

        for option in options:
            chrome_options.add_argument(option)

        driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

        return driver

    def openURL(self) -> None:
        super().openURL()
        time.sleep(4)

    def getHar(self) -> dict:
        har = self.proxy.har
        return har

    def getData(self) -> webdriver.Chrome:
        return self.driver

    def findElement(self, css_selector: str) -> str:
        return self.driver.find_element(By.CSS_SELECTOR, css_selector).text


    def close(self) -> None:
        self.driver.close()
        self.proxy.close()
        bmp_daemon = self.server
        if bmp_daemon is not None and bmp_daemon.process is not None:
            childs_process = None
            try:
                cmd_process = psutil.Process(bmp_daemon.process.pid)
                childs_process = cmd_process.children(recursive=True)
                childs_process = [*childs_process, cmd_process]

                bmp_daemon.stop()

            finally:
                for child in childs_process:
                    # we can't accidentally kill newly created process
                    # we can kill only the process we have cached earlier
                    # if process was already finished we will get NoSuchProcess
                    # that we're just suppressing
                    with suppress(psutil.NoSuchProcess):
                        try:
                            child.send_signal(signal.SIGTERM)
                        except:
                            pass
        

if __name__ == "__main__":
    import time
    import json

    #browser = StandardBrowser("https://soundcloud.com/akronymcollective/tracks")
    
    #soundlist = browser.getData().find_elements(By.CLASS_NAME, "soundList__item")
    #print(len(soundlist))

    proxybrowser = ProxyBrowser("https://open.spotify.com/album/3uPnO1aZBwMgWK1DI5zve9")
    #proxybrowser.closeBrowser()
    result = proxybrowser.getData()
    har = proxybrowser.getHar()
    result = result.find_element(By.CSS_SELECTOR, "h1.Type__TypeElement-goli3j-0")

    print(result.text)

    proxybrowser.close()
