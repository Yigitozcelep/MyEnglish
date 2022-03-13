import datetime

class SearchResult:
    word_data = []
    def __init__(self):
        self.cambridge_turkish = []
        self.cambridge_english = []
        self.longman = []
        self.your_dictionary = []
        self.thesaurus = []

        self.noun_quiz_examples = set()
        self.adjective_quiz_examples = set()
        self.verb_quiz_examples = set()
        self.adverb_quiz_examples = set()
        self.phrase_quiz_examples = set()

        self.synonyms_set = set() # TODO Kritik dikkat et

        self.noun = ""
        self.noun_tr1 = ""
        self.noun_tr2 = ""
        self.noun_ex1 = ""
        self.noun_ex2 = ""
        self.adjective = ""
        self.adjective_tr1 = ""
        self.adjective_tr2 = ""
        self.adjective_ex1 = ""
        self.adjective_ex2 = ""
        self.verb = ""
        self.verb_tr1 = ""
        self.verb_tr2 = ""
        self.verb_ex1 = ""
        self.verb_ex2 = ""
        self.adverb = ""
        self.adverb_tr1 = ""
        self.adverb_tr2 = ""
        self.adverb_ex1 = ""
        self.adverb_ex2 = ""
        self.phrase = ""
        self.phrase_tr1 = ""
        self.phrase_tr2 = ""
        self.phrase_ex1 = ""
        self.phrase_ex2 = ""
        self.synonyms = ""
        self.quiz1 = ""
        self.quiz2 = ""
        self.quiz3 = ""
        self.quiz4 = ""
        self.frequency = "0-1-7-14-30-90-360"
        self.shown = 0
        self.date = datetime.date.today()

        SearchResult.word_data.append(self)

    def __repr__(self):
        value = self.noun or self.adjective or self.verb or self.adverb or self.phrase
        return f"| {value} |"
    def __str__(self):
        return self.__repr__()

    def major_attributes(self):
        return [self.__getattribute__(name).strip() for name in ["noun", "adjective", "verb", "adverb", "phrase"] if self.__getattribute__(name).strip()]

    def all_attributes_without_finds(self):
        return {key:value for key,value in self.__dict__.items() if key not in ["cambridge_turkish", "cambridge_english", "longman", "your_dictionary", "thesaurus", "noun_quiz_examples", "adjective_quiz_examples", "verb_quiz_examples", "adverb_quiz_examples", "phrase_quiz_examples", "synonyms_set"]}
