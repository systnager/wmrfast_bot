import hashlib

"""
key consist from 64 symbols. 64 symbols divide for 4 block
everyone block consist from 4 block. small block consist from 16 symbols
first and last block is complementary user id (view const in class Activation)
second and third block have duplicate data expiry info.
"""


class Activation:
    COMPLEMENTARY_PAIR = {
        'a': 'n',
        'b': 'o',
        'c': 'p',
        'd': 'q',
        'e': 'r',
        'f': 's',
        'g': 't',
        'h': 'u',
        'i': 'v',
        'j': 'w',
        'k': 'x',
        'l': 'y',
        'm': 'z',
        '0': '6',
        '1': '7',
        '2': '8',
        '3': '9',
        '4': '5',
        'n': 'a',
        'o': 'b',
        'p': 'c',
        'q': 'd',
        'r': 'e',
        's': 'f',
        't': 'g',
        'u': 'h',
        'v': 'i',
        'w': 'j',
        'x': 'k',
        'y': 'l',
        'z': 'm',
        '6': '0',
        '7': '1',
        '8': '2',
        '9': '3',
        '5': '4',
    }

    COMPLEMENTARY_FOR_NUMBER_PAIR = {
        '0': 'a',
        '1': 'b',
        '2': 'c',
        '3': 'd',
        '4': 'e',
        '5': 'f',
        '6': 'g',
        '7': 'h',
        '8': 'i',
        '9': 'j',
        'a': '0',
        'b': '1',
        'c': '2',
        'd': '3',
        'e': '4',
        'f': '5',
        'g': '6',
        'h': '7',
        'i': '8',
        'j': '9',
    }

    @staticmethod
    def get_user_id(string: str) -> str:
        return hashlib.sha256(string.encode()).hexdigest()

    @staticmethod
    def get_expire_data_from_key(key: str) -> str:
        second_key_part = key[16:32]
        third_key_part = key[32:48]
        if second_key_part != third_key_part:
            raise ValueError('KEY IS NOT COMPLEMENTARY')
        return Activation.get_complementary_number(second_key_part[0:8])

    @staticmethod
    def get_complementary_value(value: str) -> str:
        result = ''
        for i in value:
            result += Activation.COMPLEMENTARY_PAIR[i]
        return result

    @staticmethod
    def get_complementary_number(value: str) -> str:
        result = ''
        for i in value:
            result += Activation.COMPLEMENTARY_FOR_NUMBER_PAIR[i]
        return result

    @staticmethod
    def is_key_valid(key: str, user_id: str) -> bool:
        if len(key) != 64:
            return False
        first_key_part = key[0:16]
        second_key_part = key[16:32]
        third_key_part = key[32:48]
        forth_key_part = key[48:63]

        first_user_id_part = user_id[0:16]
        forth_user_id_part = user_id[48:63]

        if first_user_id_part != Activation.get_complementary_value(first_key_part):
            return False
        if forth_user_id_part != Activation.get_complementary_value(forth_key_part):
            return False
        if second_key_part != third_key_part:
            return False

        return True

    @staticmethod
    def generate_key(user_id: str, expire_date: str) -> str:
        return (f'{Activation.get_complementary_value(user_id[0:16])}' +
                f'{Activation.get_complementary_number(expire_date)}'*2 +
                f'{Activation.get_complementary_number(expire_date)}'*2 +
                f'{Activation.get_complementary_value(user_id[48:64])}')
