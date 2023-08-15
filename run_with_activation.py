from datetime import datetime
from activation import Activation
from main import main

file = open("authentication_data.txt", "r")
userdata = file.read().split(':')
username = userdata[0]
file.close()
if len(userdata) < 2:
    input('WARNING, ENTER YOUR USERNAME IN authentication_data.txt FILE')
    raise SystemExit

user_id = Activation.get_user_id(username)
file = open("key.txt", "r")
key = file.read().replace(' ', '')
file.close()

file = open("YOUR USER ID.txt", 'w')
file.write(user_id.replace(' ', ''))
file.close()

while not Activation.is_key_valid(key, user_id):
    print(f'YOUR USER ID: {user_id}\nITS WAS WRITTEN IN "YOUR USER ID.txt" FILE IN BOT FOLDER')
    input('PRESS ENTER AFTER ENTER VALID PRODUCT KEY IN "key.txt"')
    file = open("key.txt", 'r')
    key = file.read().replace(' ', '')
    file.close()

user_date = datetime.strptime(Activation.get_expire_data_from_key(key), "%d%m%Y")
current_date = datetime.now()

if user_date < current_date:
    input('KEY IS EXPIRE. BUY NEW IN TELEGRAM: @systnager')
    raise SystemExit

main()
