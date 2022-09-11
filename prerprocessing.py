import re
import numpy as np


def parse_sentences(lns):
    """Получает на вход массив строк, разделяет их на предложения, чистит от пустых элементов"""
    sts = list()
    for ln in lns:
        split_sentence = re.split("[.!?;:]", ln)
        split_sentence[:] = [x for x in split_sentence if x]
        sts.extend(split_sentence)
    return sts


def split_sentences(sts):
    """В полученном массиве предложений проиводит разделение на слова, добавляет токены начала и конца предложения"""
    splt_sts = list()
    for sentence in sts:
        words = list(['/start'])
        words.extend(re.split(" ", sentence))
        words.extend(['/end'])
        words[:] = [x for x in words if x]
        if len(words) > 2:
            splt_sts.extend(words)
    return splt_sts


def get_corpus(sts):
    """Создает корпус текста (совокупность всех слов, хоть раз в нем встретившихся)"""
    corp = set()
    for sentence in sts:
        corp.update(re.split(" ", sentence))
    return corp


def word_dict(words):
    """Создает словарь, в котором хранится число употреблений каждого из слов в тексте"""
    result = dict()
    for word in words:
        if word in result.keys():
            result[word] += 1.0
        else:
            result[word] = 1.0
    return result


def replace_unique(words, wrd_dict):
    """Заменяет уникальные слова специальным токеном.
    Позволяет модели адекватно реагировать на имена и другие редкие слова в тексте
    """
    for i in range(len(words)):
        if wrd_dict[words[i]] == 1.0:
            words[i] = '/undef'
    return words


def preprocessing(parsed_lines):
    """Объединяет все этапы препроцессинга кроме считывания файла"""
    sentences = parse_sentences(parsed_lines)
    words_tok = split_sentences(sentences)
    words_dict = word_dict(words_tok)
    words_tok = replace_unique(words_tok, words_dict)
    corp = get_corpus(sentences)
    return words_tok, words_dict, corp
