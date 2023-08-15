import threading
import datetime
import time

from selenium.common.exceptions import TimeoutException, NoSuchWindowException

from res.string import strings
from settings import Settings
from wmrfast import WMRFast


_settings = Settings()
settings = _settings.get_settings()
lan = settings['language']


def start_config(_exit_event):
    global _settings
    global lan
    wmr_fast = WMRFast(_settings, _exit_event)
    driver = wmr_fast.log_in()
    print(f'{datetime.datetime.now()} {strings["sleep"][lan]} 5 {strings["seconds"][lan]}')
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
                print(f'{datetime.datetime.now()} {strings["tasks_is_not_available"][lan]}')
                is_video_tasks_available = True
                is_website_tasks_available = True
                time.sleep(3600)
        except (TimeoutException, NoSuchWindowException):
            print(f'{datetime.datetime.now()} {strings["sleep"][lan]} 60 {strings["seconds"][lan]}')
            time.sleep(60)
            continue


def main():
    exit_event = threading.Event()

    thread = threading.Thread(target=start_config, args=(exit_event,))
    thread.start()
    try:
        while True:
            command = input(f'\n{strings["command_list"][lan]}\n')
            if command == "pause":
                exit_event.set()
                print(f'{datetime.datetime.now()} {strings["bot_paused"][lan]}')
            elif command == "resume":
                exit_event.clear()
                print(f'{datetime.datetime.now()} {strings["bot_resume"][lan]}')
            else:
                print(f'{strings["invalid_command"][lan]} {strings["command_list"][lan]}\n')
    except KeyboardInterrupt:
        exit_event.set()

    thread.join()


if __name__ == "__main__":
    main()
