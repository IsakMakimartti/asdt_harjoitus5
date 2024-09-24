import tkinter as tk
import threading as td
from tkinter import PhotoImage
import time

# Alustus
window = tk.Tk()
window.title("Harjoitus5")
window.geometry("640x480")

# Muuttujat
mannerX = 570

# Tuodaan kuvat
imageSaari = PhotoImage(file="saari.png")
imageManner = PhotoImage(file="manner.png")
imageApina = PhotoImage(file="apina.png")

# Tehdään Labelit
labelImageSaari = tk.Label(window, image=imageSaari)
labelImageManner = tk.Label(window, image=imageManner)
labelImageApina = tk.Label(window, image=imageApina)
labelImageApinaErnesti = tk.Label(window, image=imageApina)
labelImageApinaKernesti = tk.Label(window, image=imageApina)

# Apinoiden liikkeellepano
def moveMonkey(whoIsSending):

    if whoIsSending == True:
        print("Ernesti lähetti apinan matkaan")
        kahva_moveMonkeyErnesti.start() 
    else:
        print("Kernesti lähetti apinan matkaan")
        kahva_moveMonkeyKernesti.start()

# Apinoiden liike toiminnallisuus
def moveMonkeyErnesti():
    global mannerX
    print("Ollaan moveMonkeyErnesti funktiossa")
    movementRate = 5
    xAxel = 70
    yAxel = 100
    counter = 0
    while xAxel < mannerX:
        labelImageApinaErnesti.place(x=xAxel, y=yAxel, anchor="n")
        xAxel +=movementRate
        counter +=1
        print("Ernestin apinan matka:", counter,"KM")
        time.sleep(0.05)

def moveMonkeyKernesti():
    global mannerX
    print("Ollaan moveMonkeyKernesti funktiossa")
    movementRate = 5
    xAxel = 70
    yAxel = 345
    counter = 0

    while xAxel < mannerX:
        labelImageApinaKernesti.place(x=xAxel, y=yAxel, anchor="n")
        xAxel +=movementRate
        counter +=1
        print("Kernestin apinan matka: ",counter,"KM")
        time.sleep(0.05)

# Tehdään threadit
kahva_moveMonkeyErnesti = td.Thread(target=moveMonkeyErnesti)
kahva_moveMonkeyKernesti = td.Thread(target=moveMonkeyKernesti)

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
buttonSendMonkeyErnesti.place(relx=0.25, rely=0.9)
buttonSendMonkeyKernesti.place(relx=0.65, rely=0.9)

# Avataan ikkuna
window.mainloop()