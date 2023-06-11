import datetime
import random
import time

from bcolors import bcolors
from settings import Settings
from wmrfast import WMRFast


def main():
    settings = Settings()
    wmr_fast = WMRFast(settings)
    driver = wmr_fast.log_in()
    while True:
        try:
            driver, = wmr_fast.start_watch_youtube(driver)
        except Exception as e:
            print(f"{bcolors.WARNING}{datetime.datetime.now()}{e}{bcolors.ENDC}")
            print(f'{datetime.datetime.now()} sleep 60 seconds')
            time.sleep(60)
            continue

        time_sleep = random.randint(0, 60)
        print(f'{datetime.datetime.now()} sleep {time_sleep} seconds')
        time.sleep(time_sleep)

        try:
            driver = wmr_fast.start_view_website(driver)
        except Exception as e:
            print(f"{bcolors.WARNING}{datetime.datetime.now()}{e}{bcolors.ENDC}")
            print(f'{datetime.datetime.now()} sleep 60 seconds')
            time.sleep(60)
            continue

        time_sleep = random.randint(0, 300)
        print(f'{datetime.datetime.now()} sleep {time_sleep} seconds')
        time.sleep(time_sleep)


if __name__ == "__main__":
    main()
