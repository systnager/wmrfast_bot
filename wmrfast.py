from selenium.webdriver.common.by import By
from selenium import webdriver
import random

from os.path import exists
import datetime
import pickle
import time

from res.string import strings

def _open_browser(is_headless=False):
    options = webdriver.FirefoxOptions()
    options.headless = is_headless
    options.set_preference("dom.webdriver.enabled", False)
    options.set_preference("dom.webdriver.enabled", False)
    options.set_preference('useAutomationExtension', False)
    driver = webdriver.Firefox(options=options)

    return driver, options


class WMRFast:
    def __init__(self, settings):
        self.wmrfast_url = "https://wmrfast.com"
        self.total_earned_money = 0
        self.settings = settings


    def start_view_website(self, driver, options):
        try:
            driver.get("https://wmrfast.com/serfingnew.php")
            while driver.current_url != "https://wmrfast.com/serfingnew.php":
                time.sleep(0.1)
            website_list = driver.find_elements(By.CLASS_NAME, "no_active_link")
            if len(website_list) == 0:
                driver.quit()
            for i in website_list:
                a = i.find_elements(By.CLASS_NAME, "serf_hash")[0]
                price_span, time_span = i.find_elements(By.CLASS_NAME, "clickprice")
                earned_money = float(price_span.get_attribute('innerHTML'))
                time_sleep = float(time_span.get_attribute('innerHTML').split()[0])
                a.click()
                driver.switch_to.window(driver.window_handles[1])

                time.sleep(time_sleep + random.randint(3, 5))
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                time.sleep(random.randint(3, 7))
                self.total_earned_money += earned_money
                print(f"{datetime.datetime.now()} {strings['earned'][self.settings.get_settings()['language']]}: {earned_money}, {strings['total'][self.settings.get_settings()['language']]}: {self.total_earned_money}")
        except Exception as e:
            print(f"{datetime.datetime.now()} {e}")
        finally:
            return driver, options


    def start_watch_youtube(self, driver, options):
        try:
            driver.get("https://wmrfast.com/serfing_ytn.php")
            while driver.current_url != "https://wmrfast.com/serfing_ytn.php":
                time.sleep(0.1)
            video_list = driver.find_elements(By.CLASS_NAME, "sforms")
            if len(video_list) == 0:
                driver.quit()
            for i in video_list:
                a = i.find_elements(By.CLASS_NAME, "serf_hash")[0]
                price_span, time_span = i.find_elements(By.CLASS_NAME, "clickprice")
                earned_money = float(price_span.get_attribute('innerHTML'))
                time_sleep = float(time_span.get_attribute('innerHTML').split()[0])
                time.sleep(random.randint(1, 4))
                a.click()
                while len(driver.window_handles) < 2:
                    time.sleep(0.1)
                driver.switch_to.window(driver.window_handles[1])


                #driver.find_element(By.XPATH, "/html/body/table/tbody/tr/iframe").click()
                time.sleep(time_sleep + 2.5)
                driver.execute_script("check()")
                time.sleep(0.5)
                driver.close()
                driver.switch_to.window(driver.window_handles[0])

                self.total_earned_money += earned_money
                print(
                    f"{datetime.datetime.now()} {strings['earned'][self.settings.get_settings()['language']]}: {earned_money}, {strings['total'][self.settings.get_settings()['language']]}: {self.total_earned_money}")
        except Exception as e:
            print(f"{datetime.datetime.now()} {e}")
        finally:
            return driver, options

    def _log_in_on_wmrfast(self):
        print(f"{datetime.datetime.now()} {strings['start_log_in'][self.settings.get_settings()['language']]}")
        if not exists("cookies"):
            print(f"{datetime.datetime.now()} {strings['cookies_not_find'][self.settings.get_settings()['language']]}")
            driver, options = _open_browser()
            driver.get(self.wmrfast_url)
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
        else:
            print(f"{datetime.datetime.now()} {strings['cookies_find'][self.settings.get_settings()['language']]}")
            driver, options = _open_browser(True)
            driver.get(self.wmrfast_url)
            for cookie in pickle.load(open("cookies", "rb")):
                driver.add_cookie(cookie)
            driver.get(self.wmrfast_url)

        while not ("https://wmrfast.com/members.php" in driver.current_url):
                time.sleep(1)
        pickle.dump(driver.get_cookies(), open("cookies", "wb"))
        print(f"{datetime.datetime.now()} {strings['finish_log_in'][self.settings.get_settings()['language']]}")
        return driver, options
