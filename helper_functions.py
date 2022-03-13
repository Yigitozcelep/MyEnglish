from tkinter.messagebox import showerror


def check_validty(data, info):
    for x in "\/":
        data = {key: value.replace(x, ",") for key, value in data.items()}
    data = {key: value.replace("\n", " ").replace("  ", " ").replace("  ", " ").strip() for key, value in data.items()}
    if not _check_navap(data, info): return
    if not _check_word_len(data, info): return
    if not _check_attributes(data, info): return
    if not _check_frequency_and_shown(data, info): return
    if not _check_normal_and_auto(data, info): return
    if not _check_part(data, info): return
    if not _check_write_atleast_thing(data, info): return
    if not _check_synonyms(data, info): return
    if not _check_word_max_len(data, info): return

    return data


def _check_navap(data, info):
    if "auto_words" in data and data["auto_words"]:return True

    if not (data["noun"] or data["adverb"] or data["verb"] or data["adjective"] or data["phrase"]):
        if info == "show":showerror("erorr", "You should fill one of (noun, adjective, verb, adverb, phrase)")
        return False
    return True


def _check_word_len(data, info):
    for name, value in data.items():
        if name == "shown": continue
        if 1 <= len(value) < 4:
            if info == "show":showerror("error", f"{name} has not enough letter it should be at least 4")
            return False
    return True


def _check_attributes(data, info):
    for name in ["noun", "adjective", "verb", "adverb", "phrase"]:
        if not data[name]: continue
        for plus in ["_tr1", "_ex1"]:
            if not data[name + plus]:
                if info == "show":showerror("error", f"pleas fill {name + plus}")
                return False
    return True


def _check_synonyms(data, info):
    if not data["synonyms"]: return True
    for name in ["noun", "adjective", "verb", "adverb", "phrase"]:
        if data[name]:
            return True
    if info == "show":showerror("error", "you can not just feel synonyms")
    return False


def _check_frequency_and_shown(data, info):
    if not data["shown"] or not data["shown"].isnumeric():
        if info == "show": showerror("error", "wrong shown statement")
        return False

    if data["frequency"].count("-") < 2:
        if info == "show":showerror("error", "frequency need atleas two: seperater {-}")
        return False
    for x in data["frequency"].split("-"):
        if not x.isnumeric():
            if info == "show":showerror("error", "frequency can only contain numeric and seperater {-}")
            return False

    return True


def _check_normal_and_auto(data, info):
    if not "auto_words" in data or not data["auto_words"]: return True
    for key, value in data.items():
        if key == "shown" or key == "auto_words" or key == "frequency" or key == "date": continue
        if value:
            if info == "show":showerror("error", "You can not add normal and auto word in same time")
            return False
    return True


def _check_part(data, info):
    for name, value in data.items():
        if name == "auto_words": continue
        if value and "_" in name and not data[name.split("_")[0]]:
            if info == "show":showerror("error", f"you should fill {name.split('_')[0]}")
            return False
    return True


def _check_write_atleast_thing(data, info):
    for key, values in data.items():
        if key == "frequency" or key == "shown" or key == "date": continue
        if values:
            break
    else:
        if info == "show":showerror("error", "you should fill something")
        return False
    return True


def _check_word_max_len(data, info):
    for key, value in data.items():
        if key == "synonyms" or key == "auto_words":continue
        if len(value) > 90:
            if info == "show":showerror("error", f"{key} it can not be has more then 90 letter")
            return False

    return True
