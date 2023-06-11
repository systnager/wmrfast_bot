import datetime
import random
import time

from settings import Settings
from wmrfast import WMRFast


def main():
    settings = Settings()
    wmrfast = WMRFast(settings)
    driver, options = wmrfast.log_in()
    while True:
        try:
            driver, options = wmrfast.start_watch_youtube(driver, options)
        except Exception as e:
            print(f"{bcolors.WARNING}{datetime.datetime.now()} ERROR. PLEASE, CHECK BROWSER\n{e}{bcolors.ENDC}")
            print(f'{datetime.datetime.now()} sleep 60 seconds')
            time.sleep(60)
            continue

        time_sleep = random.randint(0, 60)
        print(f'{datetime.datetime.now()} sleep {time_sleep} seconds')
        time.sleep(time_sleep)

        try:
            driver, options = wmrfast.start_view_website(driver, options)
        except Exception as e:
            print(f"{bcolors.WARNING}{datetime.datetime.now()} ERROR. PLEASE, CHECK BROWSER\n{e}{bcolors.ENDC}")
            print(f'{datetime.datetime.now()} sleep 60 seconds')
            time.sleep(60)
            continue

        time_sleep = random.randint(0, 300)
        print(f'{datetime.datetime.now()} sleep {time_sleep} seconds')
        time.sleep(time_sleep)


if __name__ == "__main__":
    main()
