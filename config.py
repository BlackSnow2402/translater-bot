from enum import Enum

bot_token = '546696964:AAFS9Doj58ib5A8dClOpq8Vt2MFJaAn9Lxs'
state_db_file = "state_database.vdb"
phrase_db_file = "phrase_database.vdb"

yandex_key = 'trnsl.1.1.20180429T151635Z.433915e83e4e0e51.4c5c1eac6f39e476ba5ae6ca24248af5040a1676'
yandex_translate_url = 'https://translate.yandex.net/api/v1.5/tr.json/translate?'
yandex_detect_url = 'https://translate.yandex.net/api/v1.5/tr.json/detect'
yandex_get_langs_url = 'https://translate.yandex.net/api/v1.5/tr.json/getLangs'



class States(Enum):
    """
    Мы используем БД Vedis, в которой хранимые значения всегда строки,
    поэтому и тут будем использовать тоже строки (str)
    """
    S_START = "0" # Дефолтное состояние
    S_ENTER_PHRASE = "1"  # Ввод фразы
    S_ENTER_LANG = "2" # Ввод языка
