import datetime
import random
import time

from settings import Settings
from wmrfast import WMRFast


def main():
    settings = Settings()
    wmr_fast = WMRFast(settings)
    driver = wmr_fast.log_in()
    while True:
        driver = wmr_fast.start_watch_youtube(driver)
        time_sleep = random.randint(0, 15)
        print(f'{datetime.datetime.now()} sleep {time_sleep} seconds')
        time.sleep(time_sleep)

        driver = wmr_fast.start_view_website(driver)
        time_sleep = random.randint(0, 200)
        print(f'{datetime.datetime.now()} sleep {time_sleep} seconds')
        time.sleep(time_sleep)


if __name__ == "__main__":
    main()
