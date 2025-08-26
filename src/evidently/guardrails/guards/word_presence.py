import re
from typing import List

from evidently.guardrails.core import GuardException
from evidently.guardrails.core import GuardrailBase


class WordsPresence(GuardrailBase):
    def __init__(self, words: List[str], presence_mode: str, search_mode: str, lemmatize: bool = False):
        super().__init__()
        self.words = words
        self.lemmatize = lemmatize
        if presence_mode not in ["includes", "include", "excludes", "exclude"]:
            raise ValueError(f"Invalid presence mode: {presence_mode}. Available modes: includes, excludes")
        if presence_mode.startswith("include"):
            self.presence_mode = "includes"
        if presence_mode.startswith("exclude"):
            self.presence_mode = "excludes"
        if search_mode not in ["all", "any"]:
            raise ValueError(f"Invalid search mode: {search_mode}. Available modes: all, any")
        self.search_mode = search_mode

    def validate(self, data: str):
        lem = None
        if self.lemmatize:
            from nltk.stem import WordNetLemmatizer

            lem = WordNetLemmatizer()
        wl = set(self.words)
        result = False
        if data is None or (isinstance(data, float)):
            return False
        words = re.sub("[^A-Za-z0-9 ]+", "", data).split()
        for word_ in words:
            word = word_.lower()
            if lem is not None:
                word = lem.lemmatize(word)
            if word in wl:
                if (self.presence_mode, self.search_mode) in (("includes", "all"), ("excludes", "any")):
                    wl.remove(word)
                else:
                    result = True
        if (self.presence_mode, self.search_mode) in (("includes", "all"), ("excludes", "any")):
            result = len(wl) == 0
        if self.presence_mode == "excludes":
            result = not result
        if not result:
            raise GuardException(f"{self.presence_mode} {self.search_mode} words")


class IncludesWords(WordsPresence):
    def __init__(self, words: List[str], mode: str = "all", lemmatize: bool = False):
        super().__init__(words=words, presence_mode="includes", search_mode=mode, lemmatize=lemmatize)
