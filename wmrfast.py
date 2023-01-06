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
        time.sleep(3)
        self.driver.execute_script("ajax_load('serfing_ytn')")
        time.sleep(5)
        for i in self.driver.find_elements(By.CLASS_NAME, "sforms"):
            try:
                a = i.find_elements(By.CLASS_NAME, "serf_hash")[0]
                span = i.find_elements(By.CLASS_NAME, "clickprice")[1]
                time_sleep = float(span.get_attribute('innerHTML').split()[0])
                a.click()
                time.sleep(3)
            except Exception:
                continue

            try:
                self.driver.switch_to.window(self.driver.window_handles[1])
                time.sleep(1)
                self.driver.find_element(By.XPATH, "/html/body/table/tbody/tr/iframe").click()
                time.sleep(time_sleep + 1)
                self.driver.execute_script("check()")
                time.sleep(2)
                self.driver.close()
                self.driver.switch_to.window(self.driver.window_handles[0])
            except Exception:
                if len(self.driver.window_handles) > 1:
                    for handle in self.driver.window_handles[1:]:
                        self.driver.switch_to.window(handle)
                        self.driver.close()
                    self.driver.switch_to.window(self.driver.window_handles[0])

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
