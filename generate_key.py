from activation import Activation


def is_numeric(input_string):
    try:
        int(input_string)
        return True
    except ValueError:
        return False


user_id = input('enter user id: ')
date_expire = input('enter date expire: ')
if len(date_expire) != 8 or is_numeric(date_expire) or len(user_id) != 64:
    print('incorrect date')
else:
    print(Activation.generate_key(user_id, date_expire))
