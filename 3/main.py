import string
import operator

from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import nltk
from sumy.parsers.plaintext import PlaintextParser
from sumy.summarizers.luhn import LuhnSummarizer
from sumy.nlp.tokenizers import Tokenizer

import telebot
from langdetect import detect

bot = telebot.TeleBot('token')

@bot.message_handler(commands=['start', 'help'])
def start_message(message):
    mess = 'Выберите метод:\n' \
           '/Sentence_extraction\n' \
           '/ML\n'
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('/Sentence_extraction', '/ML')

    bot.send_message(message.from_user.id, text=mess, reply_markup=keyboard)

@bot.message_handler(commands=['Sentence_extraction'])
def call_Sentence_extraction(message):
    bot.send_message(message.from_user.id, text='Отправьте текст')
    bot.register_next_step_handler(message, get_summary)


@bot.message_handler(commands=['ML'])
def call_ML(message):
    bot.send_message(message.from_user.id, text='Отправьте текст')
    bot.register_next_step_handler(message, ml)


def get_summary(message):
    max_sentences = 10
    input = message.text
    sentences_original = sent_tokenize(input)
    if max_sentences > len(sentences_original):
        print("Error, number of requested sentences exceeds number of sentences inputted")
    s = input.strip('\t\n')

    words_chopped = word_tokenize(s.lower())

    sentences_chopped = sent_tokenize(s.lower())

    stop_words = set(stopwords.words("spanish") + stopwords.words('german'))
    punc = set(string.punctuation)

    filtered_words = []
    for w in words_chopped:
        if w not in stop_words and w not in punc:
            filtered_words.append(w)
    total_words = len(filtered_words)

    word_frequency = {}
    output_sentence = []

    for w in filtered_words:
        if w in word_frequency.keys():
            word_frequency[w] += 1.0  # increment the value: frequency
        else:
            word_frequency[w] = 1.0  # add the word to dictionary

    for word in word_frequency:
        word_frequency[word] = (word_frequency[word] / total_words)

    tracker = [0.0] * len(sentences_original)
    for i in range(0, len(sentences_original)):
        for j in word_frequency:
            if j in sentences_original[i]:
                tracker[i] += word_frequency[j]



    for i in range(0, len(tracker)):
        index, value = max(enumerate(tracker), key=operator.itemgetter(1))
        if (len(output_sentence) + 1 <= max_sentences) and (sentences_original[index] not in output_sentence):
            output_sentence.append(sentences_original[index])
        if len(output_sentence) > max_sentences:
            break

        tracker.remove(tracker[index])

    sorted_output_sent = sort_sentences(sentences_original, output_sentence)
    for output in sorted_output_sent:
        bot.send_message(message.from_user.id, text=output)

def sort_sentences(original, output):
    sorted_sent_arr = []
    sorted_output = []
    for i in range(0, len(output)):
        if output[i] in original:
            sorted_sent_arr.append(original.index(output[i]))
    sorted_sent_arr = sorted(sorted_sent_arr)

    for i in range(0, len(sorted_sent_arr)):
        sorted_output.append(original[sorted_sent_arr[i]])
    return sorted_output


def ml(message):
    input = message.text
    print(input)
    if detect(input) == 'es':
        parser = PlaintextParser.from_string(input, Tokenizer('spanish'))
    elif detect(input) == 'de':
        parser = PlaintextParser.from_string(input, Tokenizer('german'))

    summarizer_1 = LuhnSummarizer()
    summary_1 = summarizer_1(parser.document, 10)

    for text in summary_1:
        bot.send_message(message.from_user.id, text=text)


if __name__ == "__main__":
    print("Start")

bot.polling()
