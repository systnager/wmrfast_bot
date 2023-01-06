from selenium.webdriver.common.by import By
from selenium import webdriver

from os.path import exists
import datetime
import pickle
import time


def _open_browser():
    options = webdriver.FirefoxOptions()
    options.set_preference("dom.webdriver.enabled", False)
    options.set_preference("dom.webdriver.enabled", False)
    options.set_preference('useAutomationExtension', False)
    driver = webdriver.Firefox(options=options)

    return driver, options


class WMRFast:
    def __init__(self):
        self.wmrfast_url = "https://wmrfast.com"
        self.total_earned_money = 0

    def start_watch_youtube(self):
        driver, options = self._log_in_on_wmrfast()
        time.sleep(3)
        driver.execute_script("ajax_load('serfing_ytn')")
        time.sleep(5)
        for i in driver.find_elements(By.CLASS_NAME, "sforms"):
            try:
                a = i.find_elements(By.CLASS_NAME, "serf_hash")[0]
                price_span, time_span = i.find_elements(By.CLASS_NAME, "clickprice")
                earned_money = float(price_span.get_attribute('innerHTML'))
                time_sleep = float(time_span.get_attribute('innerHTML').split()[0])
                a.click()
                time.sleep(3)
            except Exception:
                continue

            try:
                driver.switch_to.window(driver.window_handles[1])
                time.sleep(1)
                driver.find_element(By.XPATH, "/html/body/table/tbody/tr/iframe").click()
                time.sleep(time_sleep + 1)
                driver.execute_script("check()")
                time.sleep(2)
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
            except Exception:
                if len(driver.window_handles) > 1:
                    for handle in driver.window_handles[1:]:
                        driver.switch_to.window(handle)
                        driver.close()
                    driver.switch_to.window(driver.window_handles[0])
                continue
            self.total_earned_money += earned_money
            print(f"{datetime.datetime.now()} earned for session: {earned_money}, total: {self.total_earned_money}")

    def _log_in_on_wmrfast(self):
        driver, options = _open_browser()
        driver.get(self.wmrfast_url)
        if not exists("cookies"):
            file = open("authentication_data.txt", "r")
            auth_data = file.read().split(":")
            file.close()

            if len(auth_data) == 2:
                login, password = auth_data
            else:
                login, password = "", ""

            driver.find_element(By.ID, "logbtn").click()
            driver.find_element(By.ID, "vhusername").send_keys(login)
            driver.find_element(By.ID, "vhpass").send_keys(password)

            del auth_data, login, password
            while driver.current_url != "https://wmrfast.com/members.php":
                time.sleep(1)
        else:
            for cookie in pickle.load(open("cookies", "rb")):
                driver.add_cookie(cookie)

        driver.get(self.wmrfast_url)
        pickle.dump(driver.get_cookies(), open("cookies", "wb"))

        return driver, options
