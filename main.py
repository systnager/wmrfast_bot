import threading
import datetime
import time

from selenium.common.exceptions import TimeoutException, NoSuchWindowException

from res.string import strings
from settings import Settings
from wmrfast import WMRFast


def main(exit_event):
    _settings = Settings()
    settings = _settings.get_settings()
    lan = settings['language']
    wmr_fast = WMRFast(_settings, exit_event)
    driver = wmr_fast.log_in()
    print(f'{datetime.datetime.now()} sleep {5} seconds')
    time.sleep(5)
    is_video_tasks_available = True
    is_website_tasks_available = True
    while True:
        try:
            if is_website_tasks_available or is_video_tasks_available:
                if is_video_tasks_available:
                    is_video_tasks_available = wmr_fast.watch_videos(driver)['is_tasks_available']
                if is_website_tasks_available:
                    is_website_tasks_available = wmr_fast.view_websites(driver)['is_tasks_available']
            else:
                print(f"{datetime.datetime.now()} {strings['nothing_watch_or_view'][lan]}")
                is_video_tasks_available = True
                is_website_tasks_available = True
                time.sleep(3600)
        except (TimeoutException, NoSuchWindowException) as e:
            print(f"{datetime.datetime.now()} Sleep 1 minute\n{e}\n")
            time.sleep(60)
            continue


if __name__ == "__main__":
    exit_event = threading.Event()

    thread = threading.Thread(target=main, args=(exit_event,))
    thread.start()
    try:
        while True:
            command = input("Enter 'pause' to pause or 'resume' to resume the bot\n")
            if command == "pause":
                exit_event.set()
                print("Bot paused.")
            elif command == "resume":
                exit_event.clear()
                print("Bot resumed.")
            else:
                print("Invalid command. Enter 'pause' to pause or 'resume' to resume.")
    except KeyboardInterrupt:
        exit_event.set()

    thread.join()
