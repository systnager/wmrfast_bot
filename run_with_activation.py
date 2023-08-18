from datetime import datetime
from activation import Activation
from main import main
from settings import Settings
from res.string import strings

_settings = Settings()
settings = _settings.get_settings()
lan = settings['language']

file = open("authentication_data.txt", "r")
userdata = file.read().split(':')
username = userdata[0]
file.close()
if len(userdata) < 2:
    input(f'{strings["username_not_exist_warning"][lan]}')
    raise SystemExit

user_id = Activation.get_user_id(username)
file = open("key.txt", "r")
key = file.read().replace(' ', '')
file.close()

file = open("YOUR USER ID.txt", 'w')
file.write(user_id.replace(' ', ''))
file.close()

while not Activation.is_key_valid(key, user_id):
    print(f'{strings["user_id_was_writen_warning"][lan]}')
    input(f'{strings["write_key_in_file_warning"][lan]}')
    file = open("key.txt", 'r')
    key = file.read().replace(' ', '')
    file.close()

user_date = datetime.strptime(Activation.get_expire_data_from_key(key), "%d%m%Y")
current_date = datetime.now()

if user_date < current_date:
    input(f'{strings["key_expire_warning"][lan]}')
    raise SystemExit

main()
