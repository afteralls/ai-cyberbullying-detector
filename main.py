import eel
from vendors.utils.analysis import get_analysis


@eel.expose
def get_data(is_post, post_count='1', channel='', post=10000):
    result = get_analysis(is_post, post_count, channel, post)
    return result


eel.init('frontend')
eel.start('index.html', size=(1000, 500))
