from selenium.webdriver.common.by import By
from selenium import webdriver

from os.path import exists
import pickle
import time


class WMRFast:
    def __init__(self):
        self.wmrfast_url = "https://wmrfast.com"
        self.options = webdriver.FirefoxOptions()
        self.options.set_preference("dom.webdriver.enabled", False)
        self.options.set_preference("dom.webdriver.enabled", False)
        self.options.set_preference('useAutomationExtension', False)
        self.driver = webdriver.Firefox(options=self.options)

    def start_watch_youtube(self):
        self._log_in_on_wmrfast()

    def _log_in_on_wmrfast(self):
        self.driver.get(self.wmrfast_url)
        if not exists("cookies"):
            file = open("authentication_data.txt", "r")
            login, password = file.read().split(":")
            file.close()

            self.driver.find_element(By.ID, "logbtn").click()
            self.driver.find_element(By.ID, "vhusername").send_keys(login)
            self.driver.find_element(By.ID, "vhpass").send_keys(password)

            del login, password
            while self.driver.current_url != "https://wmrfast.com/members.php":
                time.sleep(1)
        else:
            for cookie in pickle.load(open("cookies", "rb")):
                self.driver.add_cookie(cookie)

        self.driver.get(self.wmrfast_url)
        pickle.dump(self.driver.get_cookies(), open("cookies", "wb"))
