from selenium.webdriver.common.by import By

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
    def __init__(self, settings):
        self.wmr_fast_url = "https://wmrfast.com"
        self.total_earned_money = 0
        self.settings = settings.get_settings()
        self.lan = self.settings['language']

    def start_view_website(self, driver):
        print(f"{datetime.datetime.now()} " +
              f"{strings['view_web'][self.lan]}"
              )
        driver.get("https://wmrfast.com/serfingnew.php")

        website_list = driver.find_elements(By.CLASS_NAME, "no_active_link")
        if len(website_list) == 0:
            print(f"{datetime.datetime.now()} {strings['nothing_watch_or_view'][self.lan]}")
            time.sleep(1800)
            return driver

        if _is_captcha_available(driver):
            input(f'\n\n\n{bcolors.WARNING}WARNING, COMPLETE THE CAPTCHA AND PRESS ENTER{bcolors.ENDC}\n\n\n')
        for i in website_list:
            try:
                a = i.find_element(By.CLASS_NAME, "serf_hash")
                price_span, time_span = i.find_elements(By.CLASS_NAME, "clickprice")
                earned_money = float(price_span.get_attribute('innerHTML'))
                time_sleep = int(time_span.get_attribute('innerHTML').split()[0]) + 3
                a.click()
            except Exception as e:
                print(f"{bcolors.WARNING}{e}{bcolors.ENDC}")
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

        return driver

    def start_watch_youtube(self, driver):
        print(f"{datetime.datetime.now()} " +
              f"{strings['watch_videos'][self.lan]}"
              )

        driver.get("https://wmrfast.com/serfing_ytn.php")
        video_list = driver.find_elements(By.CLASS_NAME, "sforms")
        if len(video_list) == 0:
            print(f"{datetime.datetime.now()} {strings['nothing_watch_or_view'][self.lan]}")
            time.sleep(1800)
            return driver

        if _is_captcha_available(driver):
            input(f'\n\n\n{bcolors.WARNING}WARNING, COMPLETE THE CAPTCHA AND PRESS ENTER{bcolors.ENDC}\n\n\n')
        for i in video_list:
            try:
                a = i.find_elements(By.CLASS_NAME, "serf_hash")[0]
                price_span, time_span = i.find_elements(By.CLASS_NAME, "clickprice")
                earned_money = float(price_span.get_attribute('innerHTML'))
                time_sleep = int(time_span.get_attribute('innerHTML').split()[0])
                a.click()
            except Exception as e:
                print(f"{bcolors.WARNING}{datetime.datetime.now()}{e}{bcolors.ENDC}")
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
            try:
                driver.execute_script("check()")
            except Exception as e:
                print(f"{bcolors.WARNING}{datetime.datetime.now()}{e}{bcolors.ENDC}")
                continue
            time.sleep(1.5)

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

        return driver

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

        pickle.dump(driver.get_cookies(), open("cookies", "wb"))
        print(f"{datetime.datetime.now()} {strings['finish_log_in'][self.lan]}")

        return driver
