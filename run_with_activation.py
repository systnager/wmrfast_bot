from datetime import datetime
from activation import Activation
from main import main

file = open("authentication_data.txt", "r")
userdata = file.read().split(':')
if len(userdata) < 2:
    print('WARNING, ENTER YOUR USERNAME IN authentication_data.txt FILE')
    quit()


username = userdata[0]
key = userdata[-1]
file.close()
user_id = Activation.get_user_id(username)

while not Activation.is_key_valid(key, user_id):
    file = open("YOUR USER ID.txt", 'w')
    file.write(user_id)
    file.close()
    print(f'YOUR USER ID: {user_id}\nITS WAS WRITTEN IN "YOUR USER ID.txt" FILE IN BOT FOLDER')
    key = input('ENTER VALID PRODUCT KEY: ')

user_date = datetime.strptime(Activation.get_expire_data_from_key(key), "%d%m%Y")
current_date = datetime.now()

if user_date < current_date:
    print('KEY IS EXPIRE. BUY NEW IN TELEGRAM: @systnager')
    quit()

file = open("authentication_data.txt", 'w')
if len(userdata) == 1:
    file.write(f'{username}: :{key}')
else:
    file.write(f'{username}:{userdata[1]}:{key}')
file.close()

main()
