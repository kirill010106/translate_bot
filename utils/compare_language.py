
def compare_language(lang: str):
    if lang == "default":
        return "Автоопределение"
    with open("/home/kirill/PycharmProjects/translateBot/languages.txt") as f:
        a = [i.strip() for i in f]
        for x in a:
            el = x.split(":")
            if el[0] == lang:
                return el[1]
        return "Язык не опознан."

def get_list():
    st = ""
    with open("/home/kirill/PycharmProjects/translateBot/languages.txt") as f:
        a = [i for i in f]
        for x in a:
            st += x
    return st