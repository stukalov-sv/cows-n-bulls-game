import random
import requests
import io
from telegram import Update, Bot, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, Filters, MessageHandler, ConversationHandler, Filters
from config import TOKEN


def random_line(afile):
    line = next(afile)
    for num, aline in enumerate(afile, start=1):
        if random.randrange(num) == 0: 
            line = aline
    return line


def check_word(word: str, word_len: int) -> str:
    sign_check = True
    while sign_check:
        for i in word:
            if (('.' or '-' or 'None' or ' ') in i):
                return check_word(random_line(io.open('.russian.txt', encoding='utf-8')), word_len)
        sign_check = False
    
    if len(word) > word_len + 1:
        word = random_line(io.open('.russian.txt', encoding='utf-8'))
        return check_word(word, word_len)
    word = word.lower()
    return word


def help(update, context):
    context.bot.send_message(update.effective_chat.id, '/help - помощь\n'
                                                       '/start - начало игры\n')


def unknown(update, context):
    context.bot.send_message(update.effective_chat.id, f'Incorrect command. Try /help')


def start(update, context):
    reply_keyboard = [["Let's play?"], ['/play', '/close']]
    markup_key = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True, one_time_keyboard=True)
    update.message.reply_text("Choose your game", reply_markup=markup_key)


def cl_start(update, _):
    update.message.reply_text('See you later', reply_markup=ReplyKeyboardRemove())


def p_vs_bot(update, _):
    update.message.reply_text(
        "Hello! It's Cows & Bulls game.\nPlayer 1, what's your name?\nOr /cancel to exit game", 
        reply_markup=ReplyKeyboardRemove())
    return FIRST_P


def first_p(update, _):
    global game_choose, first_name
    first_name = update.message.text
    update.message.reply_text(
        f"OK, {update.message.text}.\nWhat max length of guessed word?\nAnd waiting, please, while I choose the word.\nOr /cancel to exit game")
    return WORD_LEN


def word_len(update, _):    
    global word, word_length, counter
    word_length = None
    counter = 0
    if str(update.message.text).isnumeric():
        word_length = int(update.message.text)
        word_search = random_line(io.open('.russian.txt', encoding='utf-8'))
        word_search = check_word(word_search, word_length)
        word = word_search.split()
        word = ''.join(word)
        print(word) # чтобы быстро проверить программу
        word_length = len(word)
        update.message.reply_text(
            f"Good. Finally, length of word is {len(word)}.\nLet's try to guess. Write your first word with this word length.\nOr /cancel to exit game")
        return PLAYER_TURN
    else:
        update.message.reply_text(
            f"Incorrect data {update.message.text} - not number. Try again /start")
        return ConversationHandler.END


def player_turn(update, _):
    global word_length, first_name, counter
    guess_word = update.message.text.split()
    guess_word = ''.join(guess_word)

    if len(guess_word) == word_length:
        counter += 1                                     
        bulls = 0 
        cows = 0                          
        for i in range(word_length):             
            if word[i] == guess_word[i]:                       
                bulls += 1                             
            elif guess_word[i] in word:                         
                cows += 1
        if bulls == word_length:                                
            update.message.reply_text(
                'You are win the game for ' + str(counter) + ' turns! Congratulations! Try again /start')    
            return ConversationHandler.END 
        reply_keyboard = [['Yes', 'No']]
        markup_key = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True, one_time_keyboard=True)                           
        update.message.reply_text(
            guess_word + ' includes ' + str(bulls) + ' bulls & ' + str(cows) + ' cows.' + '\nReady to enter new word?', reply_markup=markup_key)
        return PLAYER_GUESS                
    else:
        reply_keyboard = [['Yes', 'No']]
        markup_key = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True, one_time_keyboard=True)
        update.message.reply_text(
            f"Incorrect data {update.message.text}.\nReady to enter new word?", reply_markup=markup_key)
        return PLAYER_GUESS


def player_guess(update, _):
    if update.message.text == 'Yes':
        update.message.reply_text(
            f"Good. Write your next word.\nOr /cancel to exit game", reply_markup=ReplyKeyboardRemove())
        return PLAYER_TURN
    else:
        update.message.reply_text(
            'Good bye', reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END


def cancel(update, _):
    update.message.reply_text('Good luck')
    return ConversationHandler.END


global word, word_length, first_name, counter

response = requests.get('https://raw.githubusercontent.com/danakt/russian-words/master/russian.txt')

text = response.content.decode('cp1251')

with open('.russian.txt', 'wb') as ru:
    ru.write(text.encode('utf-8'))

FIRST_P, WORD_LEN, PLAYER_TURN, PLAYER_GUESS = range(4)
