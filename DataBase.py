import datetime
import sqlite3
import random
con = sqlite3.connect('deneme.db')
c = con.cursor()

total = ""
for name in ["noun", "adjective", "verb", "adverb", "phrase"]:
    for plus in ["", "_tr1", "_tr2", "_ex1", "_ex2"]:
        total += name + plus + " text, "
total += "quiz1 text,quiz2 text, quiz3 text, quiz4 text, frequency text, shown INT(1), synonyms text, date text"
c.execute(f"CREATE TABLE IF NOT EXISTS words({total})")
con.commit()

def save_word(data: dict):
    data = {key: value for key,value in data.items() if key != "list_t_f"}
    if not "frequency" in data or not "shown" in data or "date" not in data or len(data) < 5:
        raise Exception(f"Frequency, shown yada date eklenen kelimede yok yada len {len(data)} < 5  leni 5 den küçük")

    placeholders = ', '.join(['?'] * len(data))
    columns = ', '.join(data.keys())
    sql = "INSERT INTO words( %s ) VALUES ( %s )" % (columns, placeholders)
    c.execute(sql, list(data.values()))
    con.commit()

def update_word(data: dict):
    data = {key: value for key,value in data.items() if key != "list_t_f" and value != ""}
    sql = f"UPDATE words set {','.join([f'{key} = ?' for key in data if key != 'id'])} WHERE rowid = ?"
    c.execute(sql, list(data.values()))
    con.commit()

def delete_word(id):
    c.execute(f"DELETE FROM words WHERE rowid = {id}")
    con.commit()

def collect_words():
    c.execute("SELECT rowid,* from words")
    items = c.fetchall()
    for x in items:
        Word((x))
    print(Word.all_words)

class Word:
    all_words = []
    today_words = []
    def __init__(self, data):
        if len(data) != 34: raise Exception(f"word: {data} kelimesinin leni 29 değil")
        muz = {name + plus: data[(num * 5) + num2 + 1] for num, name in enumerate(["noun", "adjective", "verb", "adverb", "phrase"]) for num2, plus in enumerate(["", "_tr1", "_tr2", "_ex1", "_ex2"])}
        muz["frequency"], muz["shown"], muz["synonyms"], muz["date"], muz["id"] = data[-4], data[-3], data[-2], data[-1], data[0]
        muz["quiz1"], muz["quiz2"], muz["quiz3"], muz["quiz4"] = data[-5], data[-6], data[-7], data[-8]
        self.__dict__ = muz
        self.list_t_f = []
        if self.control_date():return
        self.find_today_worlds()
        Word.all_words.append(self)

    def __repr__(self):
        result = self.noun or self.adjective or self.verb or self.adverb or self.phrase
        return f"|{result} id: {self.id} date: {self.date} shown: {self.shown} list: {self.list_t_f}|"
    def __str__(self):
        return self.noun or self.adjective or self.verb or self.adverb or self.phrase

    def control_date(self):
        try:
            year, mounth, day = self.date.split("-")
            if self.shown > self.frequency.count("-"):
                delete_word(self.id)
                return True
            if 2021 < int(year) < 2050 and 0 <= int(mounth) < 13 and 0 <= int(day) < 32:
                return False
            else:
                return True
        except:
            return True

    def find_today_worlds(self):
        frequency = self.frequency.split("-")
        shown = self.shown
        initial_day = datetime.date(*[int(x) for x in self.date.split("-")])
        today = datetime.date.today()
        if (today - initial_day).days >= int(frequency[shown]):
            Word.today_words.append(self)

    def major_attributes(self):
        data = []
        for x in ["noun", "adjective", "verb", "adverb", "phrase"]:
            if self.__dict__[x]:
                data.append(x)
        return data


def find_turkish(word):
    my_turkish = set()
    for name in ["noun", "adjective", "verb", "adverb", "phrase"]:
        for plus in ["_tr1", "_tr2"]:
            result = word.__dict__[name + plus].split(",")
            for turkish in result:
                if turkish.strip():
                    my_turkish.add(turkish.strip())
    return my_turkish

def find_english(word):
    data = set()
    for name in ["noun", "adjective", "verb", "adverb", "phrase"]:
        result = word.__dict__[name].strip()
        if result:
            data.add(result)
    return data


def do_synonyms(my_word: Word):
    data_in_word = set()
    data_not_word = set()
    my_turkish = find_turkish(my_word)
    for word in Word.all_words:
        for turkish in my_turkish:
            word_turkish = find_turkish(word)
            if turkish in word_turkish:
                data_in_word.add(word)
                break
    replaced_synonyms = my_word.synonyms.replace("|"," ").replace("  ", " ").strip()
    my_synoyms = {x.strip() for x in replaced_synonyms.split(",") if x.strip()}

    for synoynm in my_synoyms:
        for word in Word.all_words:
            result = find_english(word)
            if synoynm in result:
                data_in_word.add(word)
                break
        else:
            data_not_word.add(synoynm)

    data_in_word.discard(my_word)
    x1 = " "
    x2 = " "
    if data_in_word:
        x1 = ",".join([str(x) for x in data_in_word])
    if data_not_word:
        x2 = ",".join(str(x) for x in data_not_word)
    result = x1 + "|" + x2
    print(result)
    return result.strip()


def change_all_synonyms():
    word: Word
    for word in Word.all_words:
        word.synonyms = do_synonyms(word)

collect_words()







