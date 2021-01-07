import pyttsx3
from winsound import *
import tkinter as tk
from tkinter import *
from tkinter import messagebox as mb
import speech_recognition as speech_recog

window = tk.Tk()
window.title("Звук")
window.rowconfigure(0, minsize=400, weight=1)
window.columnconfigure(1, minsize=400, weight=1)

language = ''

def sayEnglish():
    global language
    language = "en"
    voice_id = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0"
    say(voice_id)


def sayFrench():
    global language
    language = "fr"
    voice_id = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_FR-FR_HORTENSE_11.0"
    say(voice_id)


def say(voice_id):
    text = txt_edit.get(1.0, END)
    engine = pyttsx3.init()
    engine.setProperty('voice', voice_id)
    engine.setProperty('rate', 150)
    engine.save_to_file(text, "Voice.wav")
    engine.runAndWait()
    mb.showinfo("Информация", "Текст записан в файл Voice.wav")


play = lambda: PlaySound('Voice.wav', SND_FILENAME)


def toText():
    sample_audio = speech_recog.AudioFile('Voice.wav')
    recog = speech_recog.Recognizer()
    with sample_audio as audio_file:
        audio_content = recog.record(audio_file)
    global language
    if language == "fr":
        text = recog.recognize_google(audio_content, language="fr-FR")
    else:
        text = recog.recognize_google(audio_content)
    mb.showinfo("Информация", text)

def info():
    mb.showinfo("Информация", "English text\French text - перевод текста в звук\n"
                              "Play sound - проиграть звуковой файл\n"
                                "Voice to text - синтеза речи\n")


txt_edit = tk.Text(window)
fr_buttons = tk.Frame(window)
btn_1 = tk.Button(fr_buttons, text="English text", command=sayEnglish)
btn_2 = tk.Button(fr_buttons, text="French text", command=sayFrench)
btn_3 = tk.Button(fr_buttons, text="Play sound", command=play)
btn_4 = tk.Button(fr_buttons, text="Voice to text", command=toText)
btn_5 = tk.Button(fr_buttons, text="Info", command=info)

btn_1.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
btn_2.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
btn_3.grid(row=2, column=0, sticky="ew", padx=5, pady=5)
btn_4.grid(row=3, column=0, sticky="ew", padx=5, pady=5)
btn_5.grid(row=4, column=0, sticky="ew", padx=5, pady=5)

fr_buttons.grid(row=0, column=0, sticky="ns")
txt_edit.grid(row=0, column=1, sticky="nsew")

window.mainloop()
