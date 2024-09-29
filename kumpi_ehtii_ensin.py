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
data['messageCountErnesti'] = 0
data['messageCountKernesti'] = 0

# Jaetaan kokonainen string osiin, tässä otettu mallia seuraavasta lähteestä: https://www.geeksforgeeks.org/python-program-to-split-the-string-and-convert-it-to-dictionary/
fullString = "Ernesti ja Kernesti tässä terve! Olemme autiolla saarella, voisiko joku tulla sieltä sivistyneestä maailmasta hakemaan meidät pois! Kiitos!"
delim = " "
tempString = fullString.split(delim)

for message, ele in enumerate(tempString):
    data[message] = ele

# Muuttujat
mannerX = 570
saariX = 70
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
imageCoastGuardNorth = PhotoImage(file="pohteri.png")
imageCoastGuardSouth = PhotoImage(file="eteteri.png")
imageShip = PhotoImage(file="ship.png")

# Tehdään Labelit kuvista
labelImageSaari = tk.Label(window, image=imageSaari)
labelImageManner = tk.Label(window, image=imageManner)
labelImageApina = tk.Label(window, image=imageApina)
labelImageCoastGuardNorth = tk.Label(window, image=imageCoastGuardNorth)
labelImageCoastGuardSouth = tk.Label(window, image=imageCoastGuardSouth)
labelImageShipErnesti = tk.Label(window, image=imageShip)
labelImageShipKernesti = tk.Label(window, image=imageShip)
labelPohteri = tk.Label(window, text="Pohteri")
labelEteteri = tk.Label(window, text="Eteteri")

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
            data['messageCountErnesti'] += 1
            labelMessage = tk.Label(window, text=data[messageNumber])
            labelMessage.place(x=mannerX, y=yAxel, anchor="n")
            print("ErnestiMessageCount", data['messageCountErnesti'])
            time.sleep(0.1)
            labelMessage.destroy()
    else: 
        if messageNumber > 17:
            messageCounterKernesti = 0
            messageNumber = 0
            messageSender(messageNumber, yAxel, False)
        else:
            print("Kernestin viestit:", data[messageNumber])
            data['messageCountKernesti'] += 1
            labelMessage = tk.Label(window, text=data[messageNumber])
            labelMessage.place(x=mannerX, y=yAxel, anchor="n")
            print("KernestiMessageCount", data['messageCountKernesti'])
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

    # Randomisoidaan 50% chance sille että apina tulee syödyksi
    sharkRandomizer = np.random.randint(0, 2)

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
        eatenRandomizer = np.random.random()
        playSound(400, 100)
        labelImageApinaErnesti.place(x=xAxel, y=yAxel, anchor="n")
        xAxel +=movementRate
        counter +=1
        window.update()

        # Toteutus sille että noin 50% mahdollisuus että apina jää hain suuhun toinen tarkistaa sen alkuasetetun arvon 
        # ja eatenrandomizer tarkistaa joka kilometrin välillä 1 % mahdollisuuden tulla syödyksi
        if sharkRandomizer == 1 and eatenRandomizer > 0.99:
            print("Ernestis monkey got eaten by a shark!")
            time.sleep(1.0)
            winsound.Beep(5000, 100)
            time.sleep(1.0)
            labelImageApinaErnesti.destroy()
            time.sleep(0.1)
            break
            
        # 2Pistettä osa 1 "toiminto, joka määrittelee apinan, jolle on opetettu yksi sana Ernestin ja Kernestin luomasta hätäviestistä"
        if apina_number == 'e4' and xAxel == mannerX:
            labelMessage = tk.Label(window, text=data[0])
            labelMessage.place(x=mannerX, y=yAxel, anchor="n")
            print("Ernestis singular monkey message:", data[0])
            time.sleep(0.1)
            labelMessage.destroy()
        #print("Ernestin apinan matka: ",counter,"KM")
        # 2Pistettä osa 2 toiminto "-luo toiminto säikeistystä (threading) käyttäen, jolla Ernesti voi lähettää yksittäisen apinan mukanaan yksi sana kohti manteretta.
        #  Ilmaise sopivalla äänimerkillä uimaääniä jokaisen "kilometrin" kohdalla. Ja, mikäli apina pääsee perille, ilmaise tämä sopivalla äänimerkillä."
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

    # Randomisoidaan 50% chance sille että apina tulee syödyksi
    sharkRandomizer = np.random.randint(0, 2)

    data['monkeyCountKernesti'] += 1
    apina_id_kernesti = data['monkeyCountKernesti']

    data['monkey'][apina_id_kernesti] = {'name': 'Kernestin apina'}
    data['monkey'][apina_id_kernesti]['specificName'] = ''.join(['k', str(apina_id_kernesti)])
    apina_number = data['monkey'][apina_id_kernesti]['specificName']
    labelImageApinaKernesti = tk.Label(window, image=imageApina)

    while xAxel < mannerX:
        eatenRandomizer = np.random.random()
        playSound(400, 100)
        labelImageApinaKernesti.place(x=xAxel, y=yAxel, anchor="n")
        xAxel +=movementRate
        counter +=1
        window.update()

        # Toteutus sille että noin 50% mahdollisuus että apina jää hain suuhun toinen tarkistaa sen alkuasetetun arvon 
        # ja eatenrandomizer tarkistaa joka kilometrin välillä 1 % mahdollisuuden tulla syödyksi
        if sharkRandomizer == 1 and eatenRandomizer > 0.99:
            print("Kernestis monkey got eaten by a shark!")
            time.sleep(1.0)
            winsound.Beep(5000, 100)
            time.sleep(1.0)
            labelImageApinaKernesti.destroy()
            time.sleep(0.1)
            break

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
            time.sleep(1.0)
            playSound(1000, 100)
            time.sleep(1.0)
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

def coastGuardNorth():
    global data
    shipX = 570
    messageCounter = 0
    for i in range(100):
        if messageCounter >= 10:
            while shipX > saariX:
                labelImageShipErnesti.place(x=shipX, y=70, anchor="n")
                shipX -= 1
                time.sleep(0.05)
                if shipX == saariX:
                    print("Ernesti: JES! Laiva saapui! Sain viestin perille!")
                    break
        else:
            messageCounter = data['messageCountErnesti']
            print("Pohjois rajavartiostoon saapuneet viestit:", messageCounter)
            time.sleep(1)

def coastGuardSouth():
    global data
    shipX = 570
    messageCounter = 0
    for i in range(100):
        if messageCounter >= 10:
            while shipX > saariX:
                labelImageShipKernesti.place(x=shipX, y=345, anchor="n")
                shipX -= 1
                time.sleep(0.05)
                if shipX == saariX:
                    print("Kernesti: JES! Laiva saapui! Sain viestin perille!")
                    break
        else:
            messageCounter = data['messageCountKernesti']
            print("Etelä rajavartiostoon saapuneet viestit:", messageCounter)
            time.sleep(1)

def startCoastGuardThreads():
    kahva_coastGuardNorth = td.Thread(target=coastGuardNorth)
    kahva_costGuardSouth = td.Thread(target=coastGuardSouth)
    kahva_coastGuardNorth.start()
    kahva_costGuardSouth.start()

# Tehdään napit Ernestille ja Kernestille, sekä rannikkovartiostolle
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

buttonStartCoastGuards = tk.Button (
    window,
    command = startCoastGuardThreads,
    text="Coastguards",
    anchor="sw"
)

# Sijoitetaan UI-Komponentit, paitsi apina, relx, rely tarkoittaa suhteessa 0-1 todelliseen pixelimäärään
labelImageSaari.place(x=70, y=240, anchor="center")
labelImageManner.place(x=mannerX, y=240, anchor="center")
labelImageCoastGuardNorth.place(x=mannerX, y=20, anchor="n")
labelImageCoastGuardSouth.place(x=mannerX, y=460, anchor="s")
buttonSendMonkeyErnesti.place(relx=0.01, rely=0.9)
buttonSendMonkeyKernesti.place(relx=0.12, rely=0.9)
buttonStartCoastGuards.place(relx = 0.03, rely = 0.1)
labelPohteri.place(x=mannerX, y=20, anchor="n")
labelEteteri.place(x=mannerX, y=460, anchor="s")

# Avataan ikkuna
window.mainloop()