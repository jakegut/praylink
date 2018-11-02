import os
from groupy import Bot
bot = Bot.list().first

def add_to_groupme(prayer_content):
    return bot.post(prayer_content)