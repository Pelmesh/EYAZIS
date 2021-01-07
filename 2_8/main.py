import tkinter as tk
from tkinter import *
from tkinter import messagebox
from collections import Counter
from langdetect import detect
from itertools import islice, tee


def any_lan():
    txt = txt_edit.get(1.0, END)
    if detect(txt) == 'es':
        messagebox.showinfo('Заголовок', 'Испанский')
    elif detect(txt) == 'de':
        messagebox.showinfo('Заголовок', 'немецкий')
    else:
        messagebox.showinfo('Заголовок', detect(txt))

def sum_alp(c, arr):
    q = 0
    for i in range(len(arr)):
        q += c[arr[i]]
    return q


def alp():
    txt = txt_edit.get(1.0, END)
    txt.lower()
    print(txt)
    espan = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
           'j', 'k', 'l', 'm', 'n', 'ñ', 'o', 'p', 'q', 'r',
           's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    deu = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
           'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r',
           's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'ä', 'ö', 'ü']
    c = Counter(txt)
    if c['ñ'] + c['á'] + c['é'] + c['í'] + c['ó'] + c['ú'] > 0:
        messagebox.showinfo('Заголовок', 'испанский')
    elif c['ä'] + c['ö'] + c['ü'] > 0:
        messagebox.showinfo('Заголовок', 'немецкий')
    else:
        espanNumber = sum_alp(c, espan)

        deuNumber = sum_alp(c, deu)
        print(espanNumber,deuNumber)
        if espanNumber > deuNumber:
            messagebox.showinfo('Заголовок', 'Испанский')
        elif espanNumber < deuNumber:
            messagebox.showinfo('Заголовок', 'Немецкий')
        else:
            messagebox.showinfo('Заголовок', 'Невозможно распознать')




def ngrams():
    txt = txt_edit.get(1.0, END)
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
    espanL = list_check('espan.html')
    deuL = list_check('deu.html')

    espanNumber = sum_number(espanL, text_list)
    deuNumber = sum_number(deuL, text_list)

    if espanNumber > deuNumber:
        messagebox.showinfo('Заголовок', 'Испанский')
    elif espanNumber < deuNumber:
        messagebox.showinfo('Заголовок', 'Немецкий')
    else:
        messagebox.showinfo('Заголовок', 'Невозможно распознать')

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

window = tk.Tk()
window.title("Простой текстовый редактор")

window.rowconfigure(0, minsize=400, weight=1)
window.columnconfigure(1, minsize=400, weight=1)

txt_edit = tk.Text(window)
fr_buttons = tk.Frame(window)
btn_1 = tk.Button(fr_buttons, text="ngrams", command=ngrams)
btn_2 = tk.Button(fr_buttons, text="alp", command=alp)
btn_3 = tk.Button(fr_buttons, text="any", command=any_lan)


btn_1.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
btn_2.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
btn_3.grid(row=2, column=0, sticky="ew", padx=5)

fr_buttons.grid(row=0, column=0, sticky="ns")
txt_edit.grid(row=0, column=1, sticky="nsew")

window.mainloop()
