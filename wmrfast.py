from selenium.webdriver.common.by import By
from selenium import webdriver

from os.path import exists
import datetime
import pickle
import time


def _open_browser(is_headless=False):
    options = webdriver.FirefoxOptions()
    options.headless = is_headless
    options.set_preference("dom.webdriver.enabled", False)
    options.set_preference("dom.webdriver.enabled", False)
    options.set_preference('useAutomationExtension', False)
    driver = webdriver.Firefox(options=options)

    return driver, options


class WMRFast:
    def __init__(self):
        self.wmrfast_url = "https://wmrfast.com"
        self.total_earned_money = 0


    def start_view_website(self):
        try:
            driver, options = self._log_in_on_wmrfast()
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

                time.sleep(time_sleep + 3)
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                time.sleep(3)
                self.total_earned_money += earned_money
                print(f"{datetime.datetime.now()} earned for session: {earned_money}, total: {self.total_earned_money} in view site")
        except Exception as e:
            print(f"\n\n\n{datetime.datetime.now()}\nWARNING, {e}\n\n\n\n")
            print(f"{datetime.datetime.now()} end view site")
        finally:
            driver.quit()


    def start_watch_youtube(self):
        try:
            driver, options = self._log_in_on_wmrfast()
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
                print(f"{datetime.datetime.now()} earned for session: {earned_money}, total: {self.total_earned_money} in youtube video")
        except Exception as e:
            print(f"\n\n\n{datetime.datetime.now()}\nWARNING, {e}\n\n\n\n")
            print(f"{datetime.datetime.now()} end watch youtube")
        finally:
            driver.quit()

    def _log_in_on_wmrfast(self):
        if not exists("cookies"):
            print("Cookie not found")
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
            print("Cookie find")
            driver, options = _open_browser(True)
            driver.get(self.wmrfast_url)
            for cookie in pickle.load(open("cookies", "rb")):
                driver.add_cookie(cookie)
            driver.get(self.wmrfast_url)

        while not ("https://wmrfast.com/members.php" in driver.current_url):
                time.sleep(1)
        pickle.dump(driver.get_cookies(), open("cookies", "wb"))
        print("End log in")
        return driver, options
