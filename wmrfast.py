from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementClickInterceptedException, JavascriptException, ElementNotInteractableException

from os.path import exists
import datetime
import pickle
import time

from res.string import strings
from bcolors import bcolors
from browser import Browser


def _is_captcha_available(driver):
    if len(driver.find_elements(By.ID, 'h-captcha')) != 0:
        return True
    else:
        return False


class WMRFast:
    def __init__(self, settings, exit_event):
        self.wmr_fast_url = "https://wmrfast.com"
        self.total_earned_money = 0
        self.exit_event = exit_event
        self.settings = settings.get_settings()
        self.lan = self.settings['language']

    def view_websites(self, driver):
        print(f"{datetime.datetime.now()} " +
              f"{strings['view_web'][self.lan]}"
              )
        driver.get("https://wmrfast.com/serfingnew.php")
        while _is_captcha_available(driver):
            print(f'{bcolors.WARNING}{strings["complete_captcha"][self.lan]}{bcolors.ENDC}')
            time.sleep(1)

        website_list = driver.find_elements(By.CLASS_NAME, "no_active_link")
        is_tasks_available = True
        if len(website_list) > 0:
            for i in website_list:
                while self.exit_event.is_set():
                    time.sleep(1)
                try:
                    a = i.find_element(By.CLASS_NAME, "serf_hash")
                    price_span, time_span = i.find_elements(By.CLASS_NAME, "clickprice")
                    earned_money = float(price_span.get_attribute('innerHTML'))
                    time_sleep = int(time_span.get_attribute('innerHTML').split()[0]) + 5
                    if 't.me' in a.get_attribute('href'):
                        continue
                    else:
                        a.click()
                except (ElementClickInterceptedException, ElementNotInteractableException):
                    time.sleep(1)
                    continue

                for j in range(5):
                    if len(driver.window_handles) < 2:
                        time.sleep(1)
                        continue
                    else:
                        break

                if len(driver.window_handles) < 2:
                    continue

                driver.switch_to.window(driver.window_handles[1])
                time.sleep(time_sleep)
                self.total_earned_money += earned_money
                print(
                    f"{bcolors.OKGREEN}{datetime.datetime.now()} " +
                    f"{strings['earned'][self.lan]}: " +
                    f"{round(earned_money, 5)}, {strings['total'][self.lan]}: " +
                    f"{round(self.total_earned_money, 5)}{bcolors.ENDC}"
                )
                for handle in driver.window_handles[1:]:
                    driver.switch_to.window(handle)
                    driver.close()

                driver.switch_to.window(driver.window_handles[0])
                time.sleep(5)
        else:
            is_tasks_available = False

        return {
            'is_tasks_available': is_tasks_available,
        }

    def watch_videos(self, driver):
        print(f"{datetime.datetime.now()} " +
              f"{strings['watch_videos'][self.lan]}"
              )

        driver.get("https://wmrfast.com/serfing_ytn.php")
        while _is_captcha_available(driver):
            print(f'{bcolors.WARNING}{strings["complete_captcha"][self.lan]}{bcolors.ENDC}')
            time.sleep(1)
        video_list = driver.find_elements(By.CLASS_NAME, "sforms")
        is_tasks_available = True
        if len(video_list) > 0:
            for i in video_list:
                while self.exit_event.is_set():
                    time.sleep(1)
                try:
                    a = i.find_elements(By.CLASS_NAME, "serf_hash")[0]
                    price_span, time_span = i.find_elements(By.CLASS_NAME, "clickprice")
                    earned_money = float(price_span.get_attribute('innerHTML'))
                    time_sleep = int(time_span.get_attribute('innerHTML').split()[0])
                    a.click()
                except (ElementClickInterceptedException, ElementNotInteractableException):
                    time.sleep(1)
                    continue

                for j in range(5):
                    if len(driver.window_handles) < 2:
                        time.sleep(1)
                        continue
                    else:
                        break

                if len(driver.window_handles) < 2:
                    continue

                driver.switch_to.window(driver.window_handles[1])
                time.sleep(time_sleep)
                time.sleep(3)
                try:
                    driver.execute_script("check()")
                    time.sleep(3)
                except JavascriptException:
                    time.sleep(1)
                else:
                    self.total_earned_money += earned_money
                    print(
                        f"{bcolors.OKGREEN}{datetime.datetime.now()} " +
                        f"{strings['earned'][self.lan]}: " +
                        f"{round(earned_money, 5)}, {strings['total'][self.lan]}: " +
                        f"{round(self.total_earned_money, 5)}{bcolors.ENDC}"
                    )
                for handle in driver.window_handles[1:]:
                    driver.switch_to.window(handle)
                    driver.close()

                driver.switch_to.window(driver.window_handles[0])
                time.sleep(1)
        else:
            is_tasks_available = False

        return {
            'is_tasks_available': is_tasks_available,
        }

    def log_in(self):
        print(f"{datetime.datetime.now()} {strings['start_log_in'][self.lan]}")
        driver = Browser(self.settings['browser_is_headless']
                         ).open_browser() if exists("cookies") else Browser(False).open_browser()

        driver.get(self.wmr_fast_url)

        if exists("cookies"):
            print(f"{datetime.datetime.now()} {strings['cookies_find'][self.lan]}")
            for cookie in pickle.load(open("cookies", "rb")):
                driver.add_cookie(cookie)
            driver.get("https://wmrfast.com/members.php")
        else:
            print(f"{datetime.datetime.now()} {strings['cookies_not_find'][self.lan]}")
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
        while not ('member' in driver.current_url):
            time.sleep(1)

        pickle.dump(driver.get_cookies(), open("cookies", "wb"))
        print(f"{datetime.datetime.now()} {strings['finish_log_in'][self.lan]}")

        return driver
