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

LIST_TYPE_TRACTEUR = ["TRACTEUR 2 R_AV 2 R_AR", "TRACTEUR 2 R_AV 1 R_AR" ,"TRACTEUR 1 R_AV 2 R_AR", "ENJAMBEUR 2R_AV 2R_AR", "ENJAMBEUR 2R_AV 1R_AR", "ENJAMBEUR 1R_AV 2R_AR", "TRACTEUR CHENILLE"]
LIST_DIRECTION_TRACTEUR = ["CHENILLE", "AVANT", "AV et AR", "ARRIERE"]

LIST_TYPE_OUTILS = ["CAISSON", "TRAVAUX SOL POINTES", "TRAVAUX SOL CHARRUES", "TRAVAUX SOL DISQUES", "TRAVAUX SOL ROTAVATOR", 
                    "DECAVAILLONEUSE", "LAME INTERCEP",
                    "TONDEUSE AXE HORIZONTAL", "TONDEUSE AXE VERTICAL","DESHERBAGE PHYTO", "TRAITEMENT FOLIAIRE",
                      "DISTRIBUTEUR EAU", "DISTRIBUTEUR ANGRAIS"]
OUTIL_OBLIGATOIRE = "SANS OUTIL"

PARTIE_TRAVAILLE_PAR_LOUTIL = ["RIEN", "RANG", "INTERCEP", "PARCELLE"]
LIST_NON_OUI = ["NON", "OUI" ]
OUI = "OUI"
NON="NON"
LIST_DEPORT = ["CENTRE", "DROITE", "GAUCHE"]
CENTRE = "CENTRE"
GAUCHE = "GAUCHE"
DROITE = "DROITE"

# dossier pour les outils et le materiel
MATERIEL = "materiel"
# extension des outils
EXT_OUTILS = "otl"
# extension pour les porteur
EXT_PORTEUR = "por"