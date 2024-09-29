import tkinter as tk
import threading as td
from tkinter import PhotoImage
import time
import numpy as np
import winsound

# Alustus
window = tk.Tk()
window.title("Harjoitus5")
window.geometry("640x480")

# Dictionary
data = {}
data['monkeyCountErnesti'] = 0
data['monkeyCountKernesti'] = 0
data['monkey'] = {}

# Jaetaan kokonainen string osiin, tässä otettu mallia seuraavasta lähteestä: https://www.geeksforgeeks.org/python-program-to-split-the-string-and-convert-it-to-dictionary/
fullString = "Ernesti ja Kernesti tässä terve! Olemme autiolla saarella, voisiko joku tulla sieltä sivistyneestä maailmasta hakemaan meidät pois! Kiitos!"
delim = " "
tempString = fullString.split(delim)

for message, ele in enumerate(tempString):
    data[message] = ele

# Muuttujat
mannerX = 570
apina_id_ernesti = data['monkeyCountErnesti']
apina_id_kernesti = data['monkeyCountKernesti']
isSwimming = False
isSwimmingErnesti = False
isSwimmingKernesti = False
messageCounterErnesti = 0
messageCounterKernesti = 0

# Tuodaan kuvat
imageSaari = PhotoImage(file="saari.png")
imageManner = PhotoImage(file="manner.png")
imageApina = PhotoImage(file="apina.png")

# Tehdään Labelit
labelImageSaari = tk.Label(window, image=imageSaari)
labelImageManner = tk.Label(window, image=imageManner)
labelImageApina = tk.Label(window, image=imageApina)

# Säikeistetään äänieffektit
def playSound(frequency, duration):
    td.Thread(target=winsound.Beep, args=(frequency, duration)).start()

# Apinoiden liikkeellepano
def moveMonkey(whoIsSending):

    if whoIsSending == True:
        #print("Ernesti lähetti apinan matkaan")
        startThread(True) 
    else:
        #print("Kernesti lähetti apinan matkaan")
        startThread(False)

# Apinoiden viestit
def messageSender(messageNumber, yAxel, whoIsMessaging):
    global messageCounterErnesti, messageCounterKernesti
    if whoIsMessaging == True:
        if messageNumber > 17:
            messageCounterErnesti = 0
            messageNumber = 0
            messageSender(messageNumber, yAxel, True)
        else:
            print("Ernestin viestit:", data[messageNumber])
            labelMessage = tk.Label(window, text=data[messageNumber])
            labelMessage.place(x=mannerX, y=yAxel, anchor="n")
            time.sleep(0.1)
            labelMessage.destroy()
    else: 
        if messageNumber > 17:
            messageCounterKernesti = 0
            messageNumber = 0
            messageSender(messageNumber, yAxel, False)
        else:
            print("Kernestin viestit:", data[messageNumber])
            labelMessage = tk.Label(window, text=data[messageNumber])
            labelMessage.place(x=mannerX, y=yAxel, anchor="n")
            time.sleep(0.1)
            labelMessage.destroy()

# Säikeistys viesteille riippuen onko Ernesti vai Kernesti
def startMessageThread(whoIsMessaging):
    if whoIsMessaging == True:
        kahva_sendMessageErnesti = td.Thread(target=messageSender(messageCounterErnesti, 100, True))
        kahva_sendMessageErnesti.start()
    else: 
        kahva_sendMessageKernesti = td.Thread(target=messageSender(messageCounterKernesti, 345, False))
        kahva_sendMessageKernesti.start()

# Apinoiden liike toiminnallisuus
def moveMonkeyErnesti():
    global mannerX, isSwimmingErnesti, data, apina_id_ernesti, messageCounterErnesti
    isSwimmingErnesti = True
    #print("Ollaan moveMonkeyErnesti funktiossa")

    movementRate = 5
    xAxel = 70
    yAxel = 100
    counter = 0

    # Lasketaan apinat
    data['monkeyCountErnesti'] += 1
    apina_id_ernesti = data['monkeyCountErnesti']

    # Nimetään apinat
    data['monkey'][apina_id_ernesti] = {'name': 'Ernestin apina'}
    data['monkey'][apina_id_ernesti]['specificName'] = ''.join(['e', str(apina_id_ernesti)])
    apina_number = data['monkey'][apina_id_ernesti]['specificName']
    labelImageApinaErnesti = tk.Label(window, image=imageApina)

    # Vertaillaan ollaanko saavuttu mantereelle
    while xAxel < mannerX:
        playSound(400, 100)
        labelImageApinaErnesti.place(x=xAxel, y=yAxel, anchor="n")
        xAxel +=movementRate
        counter +=1
        window.update()
        # 2Pistettä osa 1 "toiminto, joka määrittelee apinan, jolle on opetettu yksi sana Ernestin ja Kernestin luomasta hätäviestistä"
        if apina_number == 'e4' and xAxel == mannerX:
            labelMessage = tk.Label(window, text=data[0])
            labelMessage.place(x=mannerX, y=yAxel, anchor="n")
            print("Ernestis singular monkey message:", data[0])
            time.sleep(0.1)
            labelMessage.destroy()
        #print("Ernestin apinan matka: ",counter,"KM")
        if xAxel == mannerX:
            startMessageThread(True)
            messageCounterErnesti += 1
            time.sleep(0.1)
            playSound(1000, 100)
            labelImageApinaErnesti.destroy()
        time.sleep(0.05)
    killThread(True)

def moveMonkeyKernesti():
    global mannerX, isSwimmingKernesti, data, apina_id_kernesti, messageCounterKernesti
    isSwimmingKernesti = True
    #print("Ollaan moveMonkeyKernesti funktiossa")

    movementRate = 5
    xAxel = 70
    yAxel = 345
    counter = 0

    data['monkeyCountKernesti'] += 1
    apina_id_kernesti = data['monkeyCountKernesti']

    data['monkey'][apina_id_kernesti] = {'name': 'Kernestin apina'}
    data['monkey'][apina_id_kernesti]['specificName'] = ''.join(['k', str(apina_id_kernesti)])
    apina_number = data['monkey'][apina_id_kernesti]['specificName']
    labelImageApinaKernesti = tk.Label(window, image=imageApina)

    while xAxel < mannerX:
        playSound(400, 100)
        labelImageApinaKernesti.place(x=xAxel, y=yAxel, anchor="n")
        xAxel +=movementRate
        counter +=1
        window.update()

        if apina_number == 'k4' and xAxel == mannerX:
            labelMessage = tk.Label(window, text=data[0])
            labelMessage.place(x=mannerX, y=yAxel, anchor="n")
            print("Kernestis singular monkey message:", data[0])
            time.sleep(0.1)
            labelMessage.destroy()
        #print("Kernestin apinan matka: ",counter,"KM")
        if xAxel == mannerX:
            startMessageThread(False)
            messageCounterKernesti += 1
            time.sleep(0.1)
            playSound(1000, 100)
            labelImageApinaKernesti.destroy()
        time.sleep(0.05)
    killThread(False)

# Aloitetaan ja tapetaan säikeet riippuen kuka lähettää apinan
# Käytin koodia täältä avuksi: https://stackoverflow.com/questions/63450516/i-get-this-error-runtimeerror-threads-can-only-be-started-once-when-i-click-c 
def startThread(whoIsSending):
    if whoIsSending == True:
        # not isSwimmingErnesti and 
        kahva_moveMonkeyErnesti = td.Thread(target=moveMonkeyErnesti)
        kahva_moveMonkeyErnesti.start()
    elif whoIsSending == False:
        # not isSwimmingKernesti and 
        kahva_moveMonkeyKernesti = td.Thread(target=moveMonkeyKernesti)
        kahva_moveMonkeyKernesti.start()

def killThread(whoisSending):
    global isSwimmingErnesti, isSwimmingKernesti
    if whoisSending == True:
        isSwimmingErnesti = False
    else:
        isSwimmingKernesti = False

# Tehdään napit Ernestille ja Kernestille
buttonSendMonkeyErnesti = tk.Button (
    window,
    command=lambda: moveMonkey(True),
    text="Ernesti",
    anchor="sw"
)

buttonSendMonkeyKernesti = tk.Button (
    window,
    command=lambda: moveMonkey(False),
    text="Kernesti",
    anchor="se"
)

# Sijoitetaan UI-Komponentit
labelImageSaari.place(x=70, y=240, anchor="center")
labelImageManner.place(x=mannerX, y=240, anchor="center")
buttonSendMonkeyErnesti.place(relx=0.01, rely=0.9)
buttonSendMonkeyKernesti.place(relx=0.12, rely=0.9)

# Avataan ikkuna
window.mainloop()