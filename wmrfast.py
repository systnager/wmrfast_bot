from selenium.webdriver.common.by import By
from selenium import webdriver

from os.path import exists
import datetime
import random
import pickle
import time

from res.string import strings
from bcolors import bcolors


def _open_browser(is_headless=False):
    options = webdriver.FirefoxOptions()
    options.headless = is_headless
    options.set_preference('intl.accept_languages', 'ru')
    options.set_preference("dom.webdriver.enabled", False)
    options.set_preference("dom.webdriver.enabled", False)
    options.set_preference('useAutomationExtension', False)
    driver = webdriver.Firefox(options=options)

    return driver, options


class WMRFast:
    def __init__(self, settings):
        self.wmr_fast_url = "https://wmrfast.com"
        self.total_earned_money = 0
        self.settings = settings

    def start_view_website(self, driver, options):
        print(f"{datetime.datetime.now()} start view web")
        driver.get("https://wmrfast.com/serfingnew.php")
        while driver.current_url != "https://wmrfast.com/serfingnew.php":
            time.sleep(1)
        website_list = driver.find_elements(By.CLASS_NAME, "no_active_link")
        if len(website_list) == 0:
            input(f"{datetime.datetime.now()} web list is employ. Press enter to continue")
            return driver, options
        for i in website_list:
            print(f"\n{datetime.datetime.now()} get info")
            try:
                a = i.find_elements(By.CLASS_NAME, "serf_hash")[0]
                price_span, time_span = i.find_elements(By.CLASS_NAME, "clickprice")
                earned_money = float(price_span.get_attribute('innerHTML'))
                time_sleep = int(time_span.get_attribute('innerHTML').split()[0]) + random.randint(3, 5)
                print(f"{datetime.datetime.now()} click on button")
                a.click()
            except Exception as e:
                print(f"{bcolors.WARNING}{datetime.datetime.now()} ERROR. PLEASE, CHECK BROWSER\n{e}{bcolors.ENDC}")
                continue

            for j in range(5):
                if len(driver.window_handles) < 2:
                    print(f"{datetime.datetime.now()} wait opened second tab")
                    time.sleep(1)
                    continue
                else:
                    break

            if len(driver.window_handles) < 2:
                print(f"{datetime.datetime.now()} second tab does not open")
                continue

            driver.switch_to.window(driver.window_handles[1])
            print(f"{datetime.datetime.now()} wait required time: {time_sleep} seconds")
            time.sleep(time_sleep)
            self.total_earned_money += earned_money
            print(
                f"{bcolors.OKGREEN}{datetime.datetime.now()} " +
                f"{strings['earned'][self.settings.get_settings()['language']]}: " +
                f"{round(earned_money, 5)}, {strings['total'][self.settings.get_settings()['language']]}: " +
                f"{round(self.total_earned_money, 5)}{bcolors.ENDC}\n"
            )
            for handle in driver.window_handles[1:]:
                driver.switch_to.window(handle)
                driver.close()

            driver.switch_to.window(driver.window_handles[0])
            time.sleep(3)

        print(f"{datetime.datetime.now()} finish view web")
        return driver, options

    def start_watch_youtube(self, driver, options):
        driver.get("https://wmrfast.com/serfing_ytn.php")
        while driver.current_url != "https://wmrfast.com/serfing_ytn.php":
            time.sleep(1)
        video_list = driver.find_elements(By.CLASS_NAME, "sforms")
        if len(video_list) == 0:
            input(f"{datetime.datetime.now()} video list is employ. Press enter to continue")
            return driver, options
        for i in video_list:
            print(f"\n{datetime.datetime.now()} get info")
            try:
                a = i.find_elements(By.CLASS_NAME, "serf_hash")[0]
                price_span, time_span = i.find_elements(By.CLASS_NAME, "clickprice")
                earned_money = float(price_span.get_attribute('innerHTML'))
                time_sleep = int(time_span.get_attribute('innerHTML').split()[0]) + random.randint(1, 3)
                print(f"{datetime.datetime.now()} click on button")
                a.click()
            except Exception as e:
                print(f"{bcolors.WARNING}{datetime.datetime.now()} ERROR. PLEASE, CHECK BROWSER\n{e}{bcolors.ENDC}")
                continue

            for j in range(5):
                if len(driver.window_handles) < 2:
                    print(f"{datetime.datetime.now()} wait opened second tab")
                    time.sleep(1)
                    continue
                else:
                    break

            if len(driver.window_handles) < 2:
                print(f"{datetime.datetime.now()} second tab does not open")
                continue

            driver.switch_to.window(driver.window_handles[1])
            # driver.find_element(By.XPATH, "/html/body/table/tbody/tr/iframe").click()
            print(f"{datetime.datetime.now()} wait required time: {time_sleep} seconds")
            time.sleep(time_sleep)
            print(f"{datetime.datetime.now()} click to check button")
            try:
                driver.execute_script("check()")
            except Exception as e:
                print(f"{bcolors.WARNING}{datetime.datetime.now()} ERROR. PLEASE, CHECK BROWSER\n{e}{bcolors.ENDC}")
                continue
            time.sleep(random.randint(1, 3))

            self.total_earned_money += earned_money
            print(
                f"{bcolors.OKGREEN}{datetime.datetime.now()} " +
                f"{strings['earned'][self.settings.get_settings()['language']]}: " +
                f"{round(earned_money, 5)}, {strings['total'][self.settings.get_settings()['language']]}: " +
                f"{round(self.total_earned_money, 5)}{bcolors.ENDC}\n"
            )
            for handle in driver.window_handles[1:]:
                driver.switch_to.window(handle)
                driver.close()

            driver.switch_to.window(driver.window_handles[0])
            time.sleep(1)

        print(f"{datetime.datetime.now()} finish view youtube")
        return driver, options

    def log_in(self):
        print(f"{datetime.datetime.now()} {strings['start_log_in'][self.settings.get_settings()['language']]}")
        print(f"{datetime.datetime.now()} Open browser")
        driver, options = _open_browser()
        print(f"{datetime.datetime.now()} get url")
        driver.get(self.wmr_fast_url)

        print(f"{datetime.datetime.now()} get login and password from file")
        file = open("authentication_data.txt", "r")
        auth_data = file.read().split(":")
        file.close()

        if len(auth_data) == 2:
            print(f"{datetime.datetime.now()} login and password exist")
            login, password = auth_data
        else:
            print(f"{datetime.datetime.now()} login and password write incorrect")
            login, password = "", ""

        while not (self.wmr_fast_url in driver.current_url):
            print(f"{datetime.datetime.now()} wait while site loading")
            time.sleep(1)

        if exists("cookies"):
            print(f"{datetime.datetime.now()} {strings['cookies_find'][self.settings.get_settings()['language']]}")
            print(f"{datetime.datetime.now()} getting cookies")
            for cookie in pickle.load(open("cookies", "rb")):
                driver.add_cookie(cookie)
            print(f"{datetime.datetime.now()} cookies getting finish")
            driver.get("https://wmrfast.com/members.php")
        else:
            print(f"{datetime.datetime.now()} {strings['cookies_not_find'][self.settings.get_settings()['language']]}")
            driver.find_element(By.ID, "logbtn").click()
            time.sleep(random.randint(1, 3))
            driver.find_element(By.ID, "vhusername").send_keys(login)
            time.sleep(random.randint(1, 3))
            driver.find_element(By.ID, "vhpass").send_keys(password)
            del auth_data, login, password

        while not ("wmrfast.com/members.php" in driver.current_url):
            print(f"{datetime.datetime.now()} wait while site loading")
            time.sleep(1)

        print(f"{datetime.datetime.now()} dump cookies")
        pickle.dump(driver.get_cookies(), open("cookies", "wb"))
        print(f"{datetime.datetime.now()} {strings['finish_log_in'][self.settings.get_settings()['language']]}")

        return driver, options
