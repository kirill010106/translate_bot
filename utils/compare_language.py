
def compare_language(lang: str):
    if lang == "default":
        return "По умолчанию"
    with open("./languages.txt", encoding="utf-8") as f:
        a = [i.strip() for i in f]
        for x in a:
            el = x.split(":")
            if el[0] == lang:
                return el[1]
        return "Язык не опознан."


def get_lang_keys():
    with open("./languages.txt", encoding="utf-8") as f:
        a = [i.strip() for i in f]
        keys = []
        for x in a:
            el = x.split(":")
            keys.append(el[0])
    return keys


def get_list():
    st = ""
    with open("./languages.txt", encoding="utf-8") as f:
        a = [i for i in f]
        for x in a:
            st += x
    return st
