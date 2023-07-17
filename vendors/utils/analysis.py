import keras
import pandas as pd
from keras.preprocessing.text import Tokenizer
from keras.utils import pad_sequences
from .cleaning import text_cleaning
from .tg_scraper import start_scraping, get_posts

df = pd.read_csv('data/data.csv')
df['comment'] = df['comment'].apply(str)

train_features = df['comment']
train_labels = df['toxic']

vocab_size = 20000
max_seq_len = 20
vector_size = 300

tokenizer = Tokenizer(oov_token="<OOV>", num_words=vocab_size)
tokenizer.fit_on_texts(train_features)

def get_toxic_rate(comments):
    clear_comments = []
    for comment in comments:
        clear_comments.append(text_cleaning(comment))
    test_sequences = tokenizer.texts_to_sequences(clear_comments)
    model = keras.models.load_model('data/main_model')
    test_padded_sequences = pad_sequences(test_sequences, padding='post', maxlen=max_seq_len)
    predictions = model.predict(test_padded_sequences)  # type: ignore
    return predictions


def get_data(is_post, post_count, channel, post):
    if is_post:
        return start_scraping(channel, post)
    else:
        comments = []
        posts = get_posts(channel, post_count)
        for post_id in posts:
            for comment in start_scraping(channel, post_id):
                comments.append(comment)
        return comments


def get_analysis(is_post, post_count, channel, post):
    data = get_data(is_post, post_count, channel, post)
    data_for_analysis = []
    for comment in data:
        data_for_analysis.append(comment['comment'])
    predictions = get_toxic_rate(data_for_analysis)
    statistics = {}
    for idx in range(len(data)):
        data[idx]['toxic_rate'] = str(predictions[idx][0])
    toxic_rate = 0
    for rate in predictions:
        if rate[0] > 0.75:
            toxic_rate += 1
    statistics['toxic'] = toxic_rate
    statistics['all'] = len(predictions)
    statistics['group'] = '@' + channel
    statistics['non_toxic'] = statistics['all'] - statistics['toxic']
    statistics['toxic_rate'] = str(round((statistics['toxic'] * 100) / statistics['all']))
    return [statistics, data]

# test_comments = [
#     'Какой хороший день, чтобы проверить работу только что обученной нейронной сети',
#     'Кажется, у тебя реально недостаточно мозгов'
# ]

# print(get_toxic_rate(test_comments))

# Output
# [ [0.04016769], [0.92218596] ]
