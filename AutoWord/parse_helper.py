from bs4 import BeautifulSoup
import AutoWord.SearchResults as SR
import random
from googletrans import Translator

def word_hippo_urls(word):
    noun = f"https://www.wordhippo.com/what-is/the-noun-for/{word}.html"
    adjective = f"https://www.wordhippo.com/what-is/the-adjective-for/{word}.html"
    verb = f"https://www.wordhippo.com/what-is/the-verb-for/{word}.html"
    adverb = f"https://www.wordhippo.com/what-is/the-adverb-for/{word}.html"
    urls = [noun, adjective, verb, adverb]
    return urls


def create_normal_urls(word: SR.SearchResult):
    urls = []
    for word_formation in word.major_attributes():
        cambridge_turkish = f"https://dictionary.cambridge.org/dictionary/english-turkish/{word_formation}"
        cambridge_english = f"https://dictionary.cambridge.org/dictionary/english/{word_formation}"
        longman = f"https://www.ldoceonline.com/dictionary/{word_formation}"
        your_dictionary = f"https://sentence.yourdictionary.com/{word_formation}"
        thesaurus = f"https://www.thesaurus.com/browse/{word_formation}"
        urls.extend([cambridge_turkish, cambridge_english, longman, your_dictionary, thesaurus])
    return urls


def create_data_url():
    data = []
    urls = []
    num = 0
    for word in SR.SearchResult.word_data:
        result = create_normal_urls(word)
        urls.extend(result)
        data.append((num, num + len(result)))
        num += len(result)

    return data, urls


def delete_uncessery_words():
    word: SR.SearchResult
    new_data = []
    for num, word in enumerate(SR.SearchResult.word_data):
        result = word.noun or word.adjective or word.verb or word.adverb or word.phrase or ""
        if result:
            new_data.append(word)

    SR.SearchResult.word_data = new_data


def parse_word_formation(response_data):
    my_word = SR.SearchResult()
    for num, name in enumerate(["noun", "adjective", "verb", "adverb"]):
        try:
            soup = BeautifulSoup(response_data[num].text, "html.parser")
            forms = soup.find("div", class_="defv2wordtype")
        except:
            continue
        if forms:
            my_word.__dict__[name] = forms.text

    return my_word


def assign_new_calls(data, response_data):
    for current, numbers in enumerate(data):
        word: SR.SearchResult = SR.SearchResult.word_data[current]
        own_data = response_data[numbers[0]: numbers[1]]
        for x in range(0, len(own_data), 5):
            try:
                word.cambridge_turkish.append(own_data[x].text)
            except:
                pass
            try:
                word.cambridge_english.append(own_data[x + 1].text)
            except:
                pass
            try:
                word.longman.append(own_data[x + 2].text)
            except:
                pass
            try:
                word.your_dictionary.append(own_data[x + 3].text)
            except:
                pass
            try:
                word.thesaurus.append(own_data[x + 4].text)
            except:
                pass


def _find_parts(data):
    all_parts = []
    for page in data:
        if not page: continue
        try:
            soup = BeautifulSoup(page, "html.parser")
            forms = soup.find_all("div", class_="pr entry-body__el")
            all_parts.extend(forms)
        except:
            continue

    return all_parts


def _check_cambridge_word_formation(part):
    if not part: return
    try:
        soup = BeautifulSoup(str(part), "html.parser")
        result = soup.find("span", class_="pos dpos")
        if result:
            return result.text
    except:
        pass


def _check_cambridge_name(part):
    if not part: return
    try:
        soup = BeautifulSoup(str(part), "html.parser")
        result = soup.find("span", class_="hw dhw")
        if result:
            return result.text
        else:
            return
    except:
        return


def _find_turkish_part(part):
    if not part: return
    try:
        soup = BeautifulSoup(str(part), "html.parser")
        result = soup.find_all("span", class_="trans dtrans dtrans-se")
        if result:
            return result
        else:
            return
    except:
        return


def _find_turkish_meaning(data, word):
    parts = _find_parts(data)
    for part in parts:
        name = _check_cambridge_name(part)
        form = _check_cambridge_word_formation(part)
        try:
            if word.__getattribute__(form) == name:
                result = _find_turkish_part(part)
                examples = _find_english_part(part)
                if not result: continue
                if examples:
                    word.__dict__[form + "_quiz_examples"].update([x.text.strip() for x in examples])
                for num, turkish in enumerate([x.text for x in result][:2], start=1):
                    if word.__dict__[form + f"_tr{num}"]: continue
                    word.__dict__[form + f"_tr{num}"] += turkish
                    if examples:
                        if num == 2 and len(examples) == 1: continue
                        word.__dict__[form + f"_ex{num}"] += examples[num - 1].text
        except:
            continue


def _find_english_part(part):
    if not part: return
    try:
        soup = BeautifulSoup(str(part), "html.parser")
        result = soup.find_all("span", class_="eg deg")
        if result:
            return result
        else:
            return
    except:
        return


def _find_cambridge_english(data, word):
    parts = _find_parts(data)
    for part in parts:
        form = _check_cambridge_word_formation(part)
        name = _check_cambridge_name(part)
        try:
            if word.__getattribute__(form) == name:
                result = _find_english_part(part)
                if not result: continue
                word.__dict__[form + "_quiz_examples"].update([x.text.strip() for x in result])
                for num, example in enumerate([x.text for x in result][:2], start=1):
                    if word.__dict__[form + f"_ex{num}"]: continue
                    word.__dict__[form + f"_ex{num}"] += example
        except:
            pass


def your_dictionary_form(data):
    try:
        soup = BeautifulSoup(data, "html.parser")
        name = soup.find("h1",
                         class_="source-heading text-black text-2xl font-bold m-0 sm:text-3.66xl sm:leading-tight md:mr-6.25")
        if name:
            return name.text.split(" ")[0]
    except:
        return


def _find_which_attribute(word, result):
    if not result: return
    for name in ["noun", "adjective", "verb", "adverb", "phrase"]:
        if not word.__dict__[name]: continue
        if result.lower() in word.__dict__[name].lower():
            return name


def _your_dictionary_adjust_example(result):
    total = ""
    result = result.replace("\n", " ")
    x: str
    for x in result[::-1]:
        if x == " " or x.isnumeric():
            total = x + total
        else:
            break

    result = result.replace(total, "")
    return result.strip()


def _find_your_dictioanry_attributes(data):
    try:
        soup = BeautifulSoup(data, "html.parser")
        result = soup.find_all("li", class_="sentences-list-item")
        if result:
            return [_your_dictionary_adjust_example(x.text) for x in result]
    except:
        return


def _find_your_dictionary_examples(data, word):
    for part in data:
        form = _find_which_attribute(word, your_dictionary_form(part))
        if not form: continue
        result = _find_your_dictioanry_attributes(part)
        if result:
            word.__dict__[form + "_quiz_examples"].update(result)


def _find_thesaurus_synonyms(data, word):
    for part in data:
        try:
            soup = BeautifulSoup(str(part), "html.parser")
            result = soup.find_all("a", class_="css-1kg1yv8 eh475bn0")
            if result:
                for synonym in result:
                    synonym = synonym.text.strip()
                    if synonym in word.synonyms_set: continue
                    word.synonyms_set.add(synonym)
        except:
            continue


def _create_synonyms():
    word: SR.SearchResult
    for word in SR.SearchResult.word_data:
        choices = 10 if len(word.synonyms_set) > 10 else len(word.synonyms_set)
        word.synonyms = ",".join(random.sample(list(word.synonyms_set), k=choices))


def adjust_cambridge_turkish():
    word: SR.SearchResult

    for word in SR.SearchResult.word_data:
        _find_turkish_meaning(word.cambridge_turkish, word)


def adjust_cambridge_english():
    word: SR.SearchResult
    for word in SR.SearchResult.word_data:
        _find_cambridge_english(word.cambridge_english, word)


def adjust_longman():
    pass
    # TODO şimdilik pas


def adjust_your_dictionary():
    word: SR.SearchResult
    for word in SR.SearchResult.word_data:
        _find_your_dictionary_examples(word.your_dictionary, word)


def adjust_thesaurus():
    word: SR.SearchResult
    for word in SR.SearchResult.word_data:
        _find_thesaurus_synonyms(word.thesaurus, word)
        _create_synonyms()


def google_translate():
    word: SR.SearchResult
    for word in SR.SearchResult.word_data:
        for form in ["noun", "adjective", "verb", "adverb", "phrase"]:
            if not word.__getattribute__(form): continue
            if word.__getattribute__(form + "_tr1"): continue
            translator = Translator()
            word.__dict__[form + "_tr1"] = translator.translate(word.__getattribute__(form), dest="tr").text

def _do_thing(my_set):
    data = set()
    for ex in my_set:
        if len(ex) > 98: continue
        for sym in "\/":
            ex = ex.replace(sym, ",")
        ex = ex.replace("\n", " ").replace("  ", " ").replace("  ", " ").strip()
        if len(ex) < 90:
            data.add(ex)
    return data

def _filter_sentence(word):
    for form in ["noun", "adjective", "verb", "adverb", "phrase"]:
        for plus in ["_tr1", "_tr2", "_ex1", "_ex2"]:
            att = word.__dict__[form + plus]
            for sym in "\/":
                att = att.replace(sym, ",")
            att = att.replace("\n", " ").replace("  ", " ").replace("  ", " ").strip()
            if len(att) < 85:
                word.__dict__[form + plus] = att
            else:
                word.__dict__[form + plus] = ""

def adjust_settence(word):
    word.noun_quiz_examples = _do_thing(word.noun_quiz_examples)
    word.verb_quiz_examples = _do_thing(word.verb_quiz_examples)
    word.adverb_quiz_examples = _do_thing(word.adverb_quiz_examples)
    word.phrase_quiz_examples = _do_thing(word.phrase_quiz_examples)
    word.adjective_quiz_examples = _do_thing(word.adjective_quiz_examples)
    _filter_sentence(word)





def fill_examples(word):
    for form in ["noun", "adjective", "verb", "adverb", "phrase"]:
        if not word.__getattribute__(form): continue
        if not word.__getattribute__(form + "_quiz_examples"): continue
        ex1 = word.__getattribute__(form + "_ex1")
        ex2 = word.__getattribute__(form + "_ex2")
        if ex1 and ex2: continue
        word.__dict__[form + "_quiz_examples"].discard(ex1)
        word.__dict__[form + "_quiz_examples"].discard(ex2)
        if not ex1 and word.__dict__[form + "_quiz_examples"]:
            word.__dict__[form + "_ex1"] = result = random.choice(list(word.__dict__[form + "_quiz_examples"]))
            word.__dict__[form + "_quiz_examples"].discard(result)
        if not ex2 and word.__dict__[form + "_quiz_examples"]:
            word.__dict__[form + "_ex2"] = result = random.choice(list(word.__dict__[form + "_quiz_examples"]))
            word.__dict__[form + "_quiz_examples"].discard(result)

def fill_quiz(word):
    num = 0
    data = [form for form in ["adjective", "verb", "adverb", "noun"] if word.__getattribute__(form + "_quiz_examples")]
    if len(data) == 0:return
    if len(data) == 1: data = [data[0] for x in range(4)]
    if len(data) == 2: data = data + [data[0]] + [data[1]]
    if len(data) == 3: data = data + [data[0]]
    for form in data:
        result = word.__getattribute__(form + "_quiz_examples")
        if not result: continue
        num += 1
        if num == 5: break
        word.__dict__["quiz" + str(num)] = delete_this = random.choice(list(result))
        result.discard(delete_this)

def adjust_attribitus(word):
    for name in ["noun", "adjective", "verb", "adverb"]:
        ex1 = word.__getattribute__(name + "_ex1")
        ex2 = word.__getattribute__(name + "_ex2")
        if not ex1 and not ex2:
            word.__dict__[name] = ""
            word.__dict__[name + "_tr1"] = ""
            word.__dict__[name + "_tr2"] = ""
def adjust_everything():
    word: SR.SearchResult
    for word in SR.SearchResult.word_data:
        adjust_settence(word)
        fill_examples(word)
        fill_quiz(word)
        adjust_attribitus(word)

