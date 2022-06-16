import math
import operator
import string
from typing import Any, Dict, List


class NaiveBayesClassifier:
    @staticmethod
    def get_words(s: str) -> List[str]:
        translator = str.maketrans("", "", string.punctuation)
        return s.translate(translator).lower().split()

    def __init__(self, alpha: float):
        self.alpha = float(alpha)

        self._words_entries: Dict[str, Dict[Any, int]] = dict()

        self._class_entries: Dict[Any, int] = dict()
        self._words_P: Dict[str, Dict[Any, float]] = dict()
        self._class_P: Dict[Any, float] = dict()

    def fit(self, X: List[str], y: List[Any]) -> None:

        if len(X) != len(y):
            raise ValueError("Lists have different size")

        total_class_entries = 0.0

        for i in range(len(X)):
            x_case = X[i]
            y_case = y[i]

            words = self.get_words(x_case)

            self._class_entries[y_case] = self._class_entries.get(y_case, 0) + len(words)
            total_class_entries += len(words)

            for word in words:
                if word not in self._words_entries:
                    self._words_entries[word] = {"total": 1}
                else:
                    self._words_entries[word]["total"] = self._words_entries[word]["total"] + 1

                self._words_entries[word][y_case] = self._words_entries[word].get(y_case, 0) + 1

        for _class, class_entry in self._class_entries.items():
            self._class_P[_class] = math.log(class_entry / total_class_entries)

        total_word_entries = len(self._words_entries.keys())
        for word, word_entries in self._words_entries.items():
            self._words_P[word] = {}

            for _class in self._class_P:
                self._words_P[word][_class] = math.log(
                    (word_entries.get(_class, 0) + self.alpha)
                    / (word_entries["total"] + self.alpha * total_word_entries)
                )

    def _get_word_p(self, word: str, _class: str) -> float:
        """ Получить вероятность того, что слово относится к определенному классу """
        return 0 if word not in self._words_P else self._words_P[word].get(_class, 0)

    def predict(self, X: List[str]) -> List[Any]:
        y = list()
        for x_case in X:
            words = self.get_words(x_case)
            probabilities = dict()

            for _class, class_p in self._class_P.items():
                probabilities[_class] = class_p + sum(
                    [self._get_word_p(word, _class) for word in words]
                )

            y.append(max(probabilities.items(), key=operator.itemgetter(1))[0])
        return y

    def score(self, X_test: List[str], y_test: List[Any]) -> float:
        if len(X_test) != len(y_test):
            raise ValueError("Lists have different size")

        predict_vector = self.predict(X_test)
        positive, total = 0.0, len(y_test)
        for i in range(total):
            positive += 1 if predict_vector[i] == y_test[i] else 0
        return positive / total
