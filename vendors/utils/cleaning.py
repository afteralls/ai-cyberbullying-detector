import pymorphy2
import re
from nltk.corpus import stopwords

TOKEN_RE = re.compile(r'[а-яё]+')
russian_stopwords = stopwords.words("russian")
morph = pymorphy2.MorphAnalyzer(lang='ru')


def tokenize_text(txt, min_lenght_token=2):
    txt = txt.lower()
    all_tokens = TOKEN_RE.findall(txt)
    return [token for token in all_tokens if len(token) >= min_lenght_token]


def remove_stopwords(tokens):
    return list(filter(lambda token: token not in russian_stopwords, tokens))


def lemmatizing(tokens):
    return [morph.parse(token)[0].normal_form for token in tokens] # type: ignore


def text_cleaning(txt):
    tokens = tokenize_text(txt)
    tokens = lemmatizing(tokens)
    tokens = remove_stopwords(tokens)
    return ' '.join(tokens)

# my_string = """
#     Эту строчку я пишу для тестирования функции очистки текста, 
#     после чего результат попадёт прямиком в дипломную работу, 
#     которая в данный момент пишется :D
# """

# print(text_cleaning(my_string))

# Output:
# строчка писать тестирование функция очистка текст 
# результат попасть прямиком дипломный работа 
# который данный момент писаться