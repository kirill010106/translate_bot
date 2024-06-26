import json
from utils.compare_language import get_lang_keys
import requests
from config_data.config import load_config

config = load_config()
oauth_token = config.translate_api.oauth
folder_id = config.translate_api.folder


def create_iam_token(oauth):
    params = {'yandexPassportOauthToken': oauth}
    response = requests.post('https://iam.api.cloud.yandex.net/iam/v1/tokens', params=params)
    decode_response = response.content.decode('UTF-8')
    text = json.loads(decode_response)
    iam_token = text.get('iamToken')
    return iam_token


config = load_config()


def translate_text(texts: list[str], source_language: str, target_language: str = None, speller=True)\
        -> requests.Response.text:
    iam_token = create_iam_token(oauth_token)
    if target_language == "default" or source_language not in get_lang_keys():
        return "Язык перевода не определён:("
    if source_language == "default":
        src = None
    else:
        src = source_language
    body = {
        "sourceLanguageCode": src,
        "targetLanguageCode": target_language,
        "texts": texts,
        "folderId": folder_id,
        "speller": speller,
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer {0}".format(iam_token)
    }

    response = requests.post('https://translate.api.cloud.yandex.net/translate/v2/translate',
                             json=body,
                             headers=headers
                             )
    decode_response = response.content.decode('UTF-8')
    text = json.loads(decode_response)
    try:
        text = text["translations"][0]["text"]
    except KeyError:
        return "Ошибка перевода. Возможно, устарел токен."
    return text


def get_languages_list(folder):
    iam_token = create_iam_token(oauth_token)
    params = {'folderId': folder}
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer {0}".format(iam_token)
    }
    response = requests.post('https://translate.api.cloud.yandex.net/translate/v2/languages', params=params,
                             headers=headers)
    decode_response = response.content.decode('UTF-8')
    text = json.loads(decode_response)
    text = text.get("languages")
    res = []
    for el in text:
        code = str(el.get("code"))
        name = el.get("name")
        res.append({code: name})
    for x in res:
        for key in x:
            a = key
            b = x[key]
            with open("languages.txt", "a+") as f:
                f.write(f"{a}:{b}\n")
