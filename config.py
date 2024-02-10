#config

import gpiozero

BLACK = (0, 0, 0)
GRAY = (190, 190, 190) #(127, 127, 127)
WHITE = (255, 255, 255)

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)

ALEZAN = (167, 103, 38)
AMBRE = (240, 195, 0)
FER = (132, 132, 132)
CHROME = (255, 255, 5)
CITROUILLE = (223, 109, 20)
BLEU = (0, 0, 255)

couleur_arbre = WHITE
couleur_racine = MAGENTA
couleur_mort = CHROME
couleur_americain = GREEN
couleur_espalier = FER
couleur_pulve = ALEZAN
couleur_rabassier = BLEU

PIN_NO_RTK = 25 # GPIO 25
PIN_ARDUINO_OK = 24
PIN_BUTON_SCAN = 26
PIN_RASPI_OK = 18 # GPIO 18


# no_rtk = gpiozero.Button(PIN_NO_RTK, pull_up= False)  dans se cas pull_up est DOWN
NO_RTK = gpiozero.Button(PIN_NO_RTK, pull_up= True)
BUTON_SCAN = gpiozero.Button(PIN_BUTON_SCAN, pull_up= True)
RASPI_OK = gpiozero.LED(PIN_RASPI_OK)
