import telebot
from collections import Counter
from langdetect import detect
from itertools import islice, tee

bot = telebot.TeleBot('token')

@bot.message_handler(commands=['start', 'help'])
def start_message(message):
    mess = 'Выберите метод:\n' \
           '/ngrams - N-грамм\n' \
           '/alphb - алфавитный\n' \
           '/any - свой метод'

    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('/ngrams', '/alphb', '/any')
    bot.send_message(message.from_user.id, text=mess, reply_markup=keyboard)

@bot.message_handler(commands=['ngrams'])
def call_n_grams(message):
    bot.send_message(message.from_user.id, text='Отправьте текст')
    bot.register_next_step_handler(message, n_grams)

@bot.message_handler(commands=['alphb'])
def call_alp(message):
    bot.send_message(message.from_user.id, text='Отправьте текст')
    bot.register_next_step_handler(message, alp)

@bot.message_handler(commands=['any'])
def call_any_lan(message):
    bot.send_message(message.from_user.id, text='Отправьте текст')
    bot.register_next_step_handler(message, any_lan)

def n_grams(message):
    txt = message.text
    txt_2 = zip(*(islice(seq, index, None) for index, seq in enumerate(tee(txt, 2))))
    txt_3 = zip(*(islice(seq, index, None) for index, seq in enumerate(tee(txt, 3))))
    txt_4 = zip(*(islice(seq, index, None) for index, seq in enumerate(tee(txt, 4))))
    text_list = []
    for grams in txt_2:
        text_list.append(grams)
    for grams in txt_3:
        text_list.append(grams)
    for grams in txt_4:
        text_list.append(grams)
    rusL = list_check('rus.html')
    deuL = list_check('deu.html')

    rusNumber = sum_number(rusL, text_list)
    deuNumber = sum_number(deuL, text_list)

    if rusNumber > deuNumber:
        bot.send_message(message.from_user.id, text='русский')
    elif rusNumber < deuNumber:
        bot.send_message(message.from_user.id, text='немецкий')
    else:
        bot.send_message(message.from_user.id, text='Невозможно распознать')

def sum_number(new_l, text_list):
    q = 0
    for i in range(len(text_list)):
        for j in range(len(new_l)):
            if text_list[i] == new_l[j]:
                k = abs(i - j)
                if k > 5:
                    q += 5
                else:
                    q += k
    return q

def list_check(docs):
    l = []
    rus = open(docs, encoding='utf-8')
    rus_txt = rus.read()
    grams_2 = zip(*(islice(seq, index, None) for index, seq in enumerate(tee(rus_txt, 2))))
    grams_3 = zip(*(islice(seq, index, None) for index, seq in enumerate(tee(rus_txt, 3))))
    grams_4 = zip(*(islice(seq, index, None) for index, seq in enumerate(tee(rus_txt, 4))))
    for grams in grams_2:
        l.append(grams)
    for grams in grams_3:
        l.append(grams)
    for grams in grams_4:
        l.append(grams)
    l = Counter(l).most_common()
    new_list = []
    q = 0
    for i in l:
        new_list.append(l[q][0])
        q += 1
        if q > 500:
            return new_list
    return new_list

def sum_alp(c, arr):
    q = 0
    for i in range(len(arr)):
        q += c[arr[i]]
    return q

def alp(message):
    txt = message.text
    txt.lower()
    rus = ['а', 'б', 'в', 'г', 'д', 'е', 'ё', 'ж', 'з', 'и', 'й',
           'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф',
           'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я']
    deu = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
           'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r',
           's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'ä', 'ö', 'ü']
    c = Counter(txt)
    if c['ъ'] + c['ё'] > 0:
        bot.send_message(message.from_user.id, text='русский')
    elif c['ä'] + c['ö'] + c['ü'] > 0:
        bot.send_message(message.from_user.id, text='немецкий')
    else:
        rusNumber = sum_alp(c, rus)
        deuNumber = sum_alp(c, deu)
        if rusNumber > deuNumber:
            bot.send_message(message.from_user.id, text='русский')
        elif rusNumber < deuNumber:
            bot.send_message(message.from_user.id, text='немецкий')
        else:
            bot.send_message(message.from_user.id, text='Невозможно распознать')

def any_lan(message):
    txt = message.text
    if detect(txt) == 'ru':
        bot.send_message(message.from_user.id, text='русский')
    elif detect(txt) == 'de':
        bot.send_message(message.from_user.id, text='немецкий')
    else:
        bot.send_message(message.from_user.id, text=detect(txt))

if __name__ == "__main__":
    print("Start")

bot.polling()