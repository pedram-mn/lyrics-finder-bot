# Developed by Pedram Monazami
# GitHub link to project : https://github.com/pedram-mn/lyrics-finder-bot
# My Email: pedram.monazzami@gmail.com


from uuid import uuid4
from telegram import Update, error, InputTextMessageContent, InlineQueryResultArticle
from telegram.ext import Updater, CommandHandler, CallbackContext, InlineQueryHandler
from lyricsgenius import Genius as Gn

# Enter your own telegram bot token you get from @botfather bot
updater = Updater('5742251747:AAGm4qI-mYZ4aPv7PRANt8xdXTtsggij2fA')

# You can get your own genius token from https://docs.genius.com
gn = Gn("t1H9TF03VUJlzlF1QX1gtuO-UO3q29IyYtr9dSp21X0Q3vVHIQ4uB2-YSLrzJ1D6")
gn.excluded_terms = ["(Remix)", "(Live)"]


def start(update: Update, context: CallbackContext):
    update.message.reply_photo(open('start photo.jpg', 'rb'), caption="""
🎆Welcome to lyrics finder bot dear {}🎆

🟡🟡🟡🟡🟡🟡🟡🟡🟡🟡
You can find lyrics of any songs here easily just by typing its name and its singer seperated with comma
🟡🟡🟡🟡🟡🟡🟡🟡🟡🟡

🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴
Don't forget to use /lyrics command first
🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴

🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣
We have also inline bot feature that you can send lyrics in any chat directly by typing bot username and detail of song after in in chat box
🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣

⚪️⚪️⚪️⚪️⚪️⚪️⚪️⚪️⚪️⚪️
In bot example:
/lyrics Dream On , Aerosmith
Inline example
@lyrics_finderr_bot Dream On , Aerosmith
Note that for better results write song name before the singer
⚪️⚪️⚪️⚪️⚪️⚪️⚪️⚪️⚪️⚪️

🔵🔵🔵🔵🔵🔵🔵🔵🔵🔵
Btw, this is an open-source project and you can find my source code at https://github.com/pedram-mn/lyrics-finder-bot
🔵🔵🔵🔵🔵🔵🔵🔵🔵🔵""".format(update.message.chat.first_name))


def get_lyrics(song_name, singer_name):
    singer = gn.search_artist(singer_name, max_songs=0)
    song = singer.song(song_name)
    lyric = song.lyrics
    title = song.title + " by " + singer.name

    # some edit on the output
    lyric = lyric[:len(song.title)+7] + "\n" + lyric[len(song.title)+7:]
    if "Embed" in lyric:
        lyric = lyric[:-5]

    return title, lyric


def lyrics(update: Update, context: CallbackContext):
    data = " ".join(context.args).split(",")
    try:
        if len(data) != 2:
            raise IndexError
    except IndexError:
        update.message.reply_text(
            "Provide both name of music and artist seperated by only one \',\' and don\'t use comma in song or artist "
            "name")
        return
    lyrics_data = get_lyrics(data[0], data[1])
    update.message.reply_text(lyrics_data[1])


def inline_lyrics(update: Update, context: CallbackContext):
    query = update.inline_query.query
    data = query.split(",")
    if len(data) != 2:
        result = InlineQueryResultArticle(id=uuid4(),
                                          title="Provide both name of music and artist seperated by only one ','",
                                          input_message_content=InputTextMessageContent(
                                              "Provide both name of music and artist seperated by only one ','"))
        update.inline_query.answer([result])
        return

    lyrics_data = get_lyrics(data[0], data[1])
    result = InlineQueryResultArticle(id=uuid4(), title=lyrics_data[0],
                                      input_message_content=InputTextMessageContent(lyrics_data[1]))
    try:
        update.inline_query.answer([result])
    except error as e:
        pass


start_command = CommandHandler('start', start, pass_args=True)
lyrics_command = CommandHandler('lyrics', lyrics, pass_args=True)
inline_lyrics_command = InlineQueryHandler(inline_lyrics)

updater.dispatcher.add_handler(lyrics_command)
updater.dispatcher.add_handler(start_command)
updater.dispatcher.add_handler(inline_lyrics_command)

try:
    updater.start_polling()
    updater.idle()
except error.NetworkError:
    print("Network connection failed! Please check your connection or turn on your vpn")
