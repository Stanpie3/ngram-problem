import re
from prerprocessing import preprocessing


def parse_txt(input_dir):
    """Парсит текст по адресу. Удаляет примечания и побочные символы"""
    parsed_lines = list()
    with open(input_dir) as f:
        for line in f:
            if len(line) > 2:
                line = re.sub("[\[].*?[\]]", "", line) # Очищаем от примечаний редактора
                for r in (("\xa0", " "), ("–", ""), ("\"", ""), ("«", ""), ("»", ""), (",", "")): # Очищаем от избыточной пунктуации
                    line = line.replace(*r)
                parsed_lines.append(line.strip().lower())
    return parsed_lines


def gram_model(words, n):
    """n-gram модель, берем n>1"""
    ngram_dict = dict()
    prevgram_dict = dict()
    for i in range(len(words) - n):
        prevgram = tuple(words[i:n-1])
        ngram = tuple(words[i:n])
        if prevgram in prevgram_dict.keys():
            prevgram_dict[prevgram] += 1.0
        else:
            prevgram_dict[prevgram] = 1.0

        if ngram in ngram_dict.keys():
            ngram_dict[ngram] += 1.0
        else:
            ngram_dict[ngram] = 1.0
    return ngram_dict, prevgram_dict


class NGramModel(object):
    def __init__(self, data_train, n):
        self.n = n
        self.words_tok, self.words_dict, self.corpus = preprocessing(data_train)
        self.model = self.create_model()

    def create_model(self):
        ngram_dict, prevgram_dict = gram_model(self.words_tok, self.n)
        corpus_size = len(self.corpus)

        def laplase_count(ngram, ncount):
            prevgram = ngram[:-1]
            prevcount = prevgram_dict[prevgram]
            return (ncount+1)/(prevcount + corpus_size)

        return {ngram : laplase_count(ngram, ncount) for ngram, ncount in ngram_dict.items()}
