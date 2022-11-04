import os
import telebot
from telebot import types
from dotenv import load_dotenv
from get_Single import fetch_data_for_a_resourceID
from quotes.quotes import random_quote


load_dotenv()

TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN,  parse_mode="HTML")

resource_IDs = [1, 2, 12, 26, 63, 73, 93, 102, 126, 136]

def printdetails(text, callback_query):
    data, website = fetch_data_for_a_resourceID(int(text))

    if data:
        i = 1
        for s in data:
            bot.send_message(callback_query.message.chat.id,
                             f'{i}. <b>{s["name"]}</b>\n    Start Time: {s["start_time"]}\n    Starts in: <b>{s["starts_in"]}</b>\n    Duration: {s["duration"]}\n    Link: <a href= "{s["link"]}">{s["link"]}</a>')
            i = i + 1
    else:
        bot.send_message(callback_query.message.chat.id,
                         f'Looks like there are <b>NO</b> upcoming contests for <b>{website}</b>. Use this time to learn more concepts and algorithms.',
                         parse_mode="HTML")


def fetch_data_from_all(callback_query):
    var = []
    i = 1
    for rID in resource_IDs:
        inner, website = fetch_data_for_a_resourceID(rID)
        if inner:
            for s in inner:
                bot.send_message(callback_query.message.chat.id,
                                 f'{i}. <b>{s["name"]}</b>\n    Start Time: {s["start_time"]}\n    Starts in: <b>{s["starts_in"]}</b>\n    Duration: {s["duration"]}\n    Link: <a href= "{s["link"]}">{s["link"]}</a>')
                i = i + 1
        else:
            bot.send_message(callback_query.message.chat.id,
                        f'No Upcoming contests on <b>{website}</b> in next 7 days.',
                        parse_mode="HTML")
            # var.append(each)
    
    if i==1:
        bot.send_message(callback_query.message.chat.id, f'There are not any upcoming contests in the next seven days on any platforms. Enjoy this Week <3')



@bot.message_handler(commands=['start'])
def send_hello(message):

    print('Customer',end=" ")
    print(message.chat.first_name,end="\t")
    print(message.chat.username)


    b1 = types.InlineKeyboardButton(text = 'Codeforces', callback_data=1)
    b2 = types.InlineKeyboardButton(text = 'Codechef', callback_data=2)
    b3 = types.InlineKeyboardButton(text = 'AtCoder', callback_data=93)
    b4 = types.InlineKeyboardButton(text = 'Leetcode', callback_data=102)
    b5 = types.InlineKeyboardButton(text = 'GeelsforGeeks', callback_data=126)
    b6 = types.InlineKeyboardButton(text = 'Spoj', callback_data=26)
    b7 = types.InlineKeyboardButton(text = 'TopCoder', callback_data=12)
    b8 = types.InlineKeyboardButton(text = 'HackerEarth', callback_data=73)
    b9 = types.InlineKeyboardButton(text = 'HackerRank', callback_data=63)
    b10 = types.InlineKeyboardButton(text = 'CodingNinja', callback_data=136)
    b11 = types.InlineKeyboardButton(text = 'All of these', callback_data='All of these')

    markup = types.InlineKeyboardMarkup()

    markup.row(b1,b2)
    markup.row(b3,b4)
    markup.row(b5,b6,b7)
    markup.row(b8,b9,b10)
    markup.row(b11)


    qote = random_quote()

    bot.send_message(message.chat.id, qote)

    text = "Click on any website name to get the list of upcoming contests details over next 7 days."
    bot.send_message(message.chat.id, text, reply_markup=markup)


@bot.callback_query_handler(func = lambda message:True)
def answer(callback_query):

    text = callback_query.data

    if text != "All of these" :
        printdetails(text, callback_query)
    else:
        bot.send_message(callback_query.message.chat.id, f'Just give me a minute while I fetch the contest details for you.\n')
        fetch_data_from_all(callback_query)


@bot.message_handler(commands=['time'])
def time(message):
    msg = """<b>24-Hour Time format</b> is used here to remove any kind of confusion between AM/PM.\n<i>Start Time</i> is <b>{YYYY-MM-DD}</b>T<b>{HH:MM:SS}</b>\n<i>Starts in</i> is <b>{Day}</b>,<b>{HH:MM:SS}</b>\n<i>Duration</i> is <b>{HH:MM}</b>"""

    bot.send_message(message.chat.id,msg)
    

@bot.message_handler(commands=['info'])
def info(message):
    data = """All the data shown here is fetched using CLIST API and they allow only <b>10 requests/minute</b>, so in case anything not works as they should Just wait for <u><b>1</b> minute</u> to get the result. Fetching all these data one by one from each websites would have been a lot of work so a special thanks to <a href = "https://clist.by/api/v2/doc/">CLIST API</a> for making this easy."""
    bot.send_message(message.chat.id,data)


@bot.message_handler(commands=['list'])
def list_all(message):
    lists = """
1. /start - Get Contest Details
2. /list  - List of commands
3. /time  - Time Conventions
4. /info  - How do I work?
5. /help  - Facing any ISSUE
    """

    bot.send_message(message.chat.id, lists, parse_mode='HTML')

@bot.message_handler(commands=['help'])
def help_message(message):
    display = """If you are facing any issue in accessing the services. There are possibly two reasons for this to happen either the source from where these data are fetched is not working properly or I'm currently under maintenance. Whatever the reason is, <b>SORRY</b> for the trouble. For the time being please visit <a href = "https://clist.by">Clist.by</a> to get contest details."""
    bot.send_message(message.chat.id, display)

@bot.message_handler(func = lambda message:True)
def invalid(message):
    bot.send_message(message.chat.id, f'Invalid Command! Please use /list to see the list of supported commands.')


print('Bot is alive')

bot.infinity_polling()