import grequests
from tkinter.messagebox import showerror
import AutoWord.parse_helper as ph
import AutoWord.SearchResults as SR
import DataBase as DB
headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36"
    }

def main_auto_word(words):
    data = [x.strip() for x in words.split(",") if x.strip()]
    urls = [url for word in data for url in ph.word_hippo_urls(word)]
    rs = (grequests.get(u, headers=headers) for u in urls)
    response_data = grequests.map(rs)
    if not [x for x in response_data if x]:
        showerror("error","while trying to receive data error occurred try again\n 1: maybe you did not connect to the internet \n2:because of the server which we were trying to access\n if you try to save more then 15 word, you can try to save less word")
        return
    create_word(response_data)


def create_word(data):
    for num in range(0, len(data), 4):
        ph.parse_word_formation(data[num: num + 4])
    call_other_urls()

def call_other_urls():
    ph.delete_uncessery_words()
    data, urls = ph.create_data_url()
    rs = (grequests.get(u, headers=headers) for u in urls)
    response_data = grequests.map(rs)
    ph.assign_new_calls(data, response_data)
    adjust_attributes()

def adjust_attributes():
    ph.adjust_cambridge_turkish()
    ph.adjust_cambridge_english()
    ph.adjust_your_dictionary()
    ph.adjust_longman()
    ph.adjust_thesaurus()
    ph.google_translate()
    ph.adjust_everything()
    word: SR.SearchResult

    for word in SR.SearchResult.word_data:
        DB.save_word(word.all_attributes_without_finds())

    showerror("error","words are successfully saved")
