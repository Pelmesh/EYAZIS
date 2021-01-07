import pyttsx3
import telebot
import speech_recognition as speech_recog


token = 'token'
bot = telebot.TeleBot('token')

text = ''
voice_id = ''

def say(message):
    global text
    global voice_id
    newVoiceRate = message.text
    engine = pyttsx3.init()
    engine.setProperty('voice', voice_id)
    engine.setProperty('rate', newVoiceRate)
    engine.save_to_file(text, "Voice.wav")
    engine.runAndWait()
    audio = open('D:\УЧОБА\ЕЯЗИС\\5\Voice.wav', 'rb')
    bot.send_audio(message.chat.id, audio)
    audio.close()

@bot.message_handler(commands=['start', 'help'])
def start_message(message):
    mess = 'Выберите язык:\n' \
           '/Русский\n' \
           '/Английский\n'\
            '/Голос в текс'

    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('/Русский', '/Английский', '/Голос')
    bot.send_message(message.from_user.id, text=mess, reply_markup=keyboard)

def setText(message):
    global text
    text = message.text
    bot.send_message(message.from_user.id, text='Отправьте скорость воспроизведения')
    bot.register_next_step_handler(message, say)

@bot.message_handler(commands=['Русский'])
def rus(message):
    global voice_id
    voice_id = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_RU-RU_IRINA_11.0"
    bot.send_message(message.from_user.id, text='Отправьте текст')
    bot.register_next_step_handler(message, setText)


@bot.message_handler(commands=['Английский'])
def eng(message):
    global voice_id
    voice_id = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0"
    bot.send_message(message.from_user.id, text='Отправьте текст')
    bot.register_next_step_handler(message, setText)

@bot.message_handler(commands=['Голос'])
def setVoice(message):
    sample_audio = speech_recog.AudioFile('D:\УЧОБА\ЕЯЗИС\\5\Voice.wav')
    recog = speech_recog.Recognizer()
    with sample_audio as audio_file:
        audio_content = recog.record(audio_file)
    global  voice_id
    if('HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_RU-RU_IRINA_11.0' == voice_id):
        text = recog.recognize_google(audio_content, language="ru-RU")
    else:
        text = recog.recognize_google(audio_content)
    bot.send_message(message.from_user.id, text=text)

if __name__ == "__main__":
    print("Start")

bot.polling()





