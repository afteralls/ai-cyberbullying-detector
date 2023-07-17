from telethon import TelegramClient, types
import snscrape.modules.telegram as tg

api_id # secret
api_hash # secret
client = TelegramClient('main', api_id, api_hash)


async def get_comments(messages, channel, post):
    async for message in client.iter_messages(channel, reply_to=int(post), reverse=True):
        if isinstance(message.sender, types.User):
            messages.append({
                'user': message.sender.first_name,
                'comment': message.text,
                'username': message.sender.username
            })
        else:
            if hasattr(message.sender, 'title'):
                messages.append({
                    'user': message.sender.title,
                    'comment': message.text,
                    'username': message.sender.username
                })
            else:
                messages.append({'user': '—', 'comment': message.text, 'username': message.sender.username})


def start_scraping(channel, post):
    client.start()
    messages = []
    with client:
        client.loop.run_until_complete(get_comments(messages, channel, post))
    client.disconnect()
    return messages


def get_posts(channel, post_count):
    posts = []
    for i, post in enumerate(tg.TelegramChannelScraper(channel).get_items()):
        if i > int(post_count):
            break
        post_id = post.url.split('/')
        post_id.reverse()
        posts.append(post_id[0])
    return posts
