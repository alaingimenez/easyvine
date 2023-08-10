
# from read_i2ca_cmps14 import *
import smbus as smbus  # ,smbus2
import time
import os


# Slave Addresses
# inferieur a 0x64 le registre ser a lire des données // si superieur ou== a 0x64 le registre dit qu'il va envoyer des donné
# adrresse arduino et registre

I2C_ADDRESS_ARDUINO = (0x68)  # adresse de l'arduino
REGISTRE_STICK0 = 0             # lecture stick 0 de la radio commande
REGISTRE_STICK1 = 1         # lecture stick 1 de la radio commande
REGISTRE_STICK4 = 4
REGISTRE_STICK7 = 7
#
REGISTRE_MOVE = 101        # permet d'envoyer a l'arduino la valeur pour regler l'avancement comparable a stick1
REGISTRE_ROTATE = 100        # permet d'envoyer a l'arduino la valeur pour regler la rotation comparable a stick0
#

#
# addresse CMPS14
I2C_ADDRESS_CMPS14 = 0x060  #
COMPAS = 0x02               # 02 registre de lecture compas
PITCH_ANGLE = 0x04
ROLL_ANGLE = 0x05

erreur = 0
bus = smbus.SMBus(1)  # on creer un objet I2C bus

def read_i2c_word_stick(I2C_SLAVE_ADDRESS, registre):
    value = bus.read_word_data(I2C_SLAVE_ADDRESS, registre)
    if 1 < value < 1800:
        return value
    else:
        return 0


def read_i2ca_stick(I2C_SLAVE_ADDRESS, registre):
    high = bus.read_byte_data(I2C_SLAVE_ADDRESS, registre)
    low = bus.read_byte_data(I2C_SLAVE_ADDRESS, registre + 1)
    value = (high << 8) + low
    if 289 < value < 1700:
        return value
    else:
        return 0
def read_i2ca(I2C_SLAVE_ADDRESS ,registre):

    # Read the data from the registers
    high = bus.read_byte_data(I2C_SLAVE_ADDRESS, registre)
    # time.sleep(0.02)
    low = bus.read_byte_data(I2C_SLAVE_ADDRESS, registre + 1)

    value = (high << 8) + low

    if (value >= 0x8000):
        return -((65535 - value) + 1)
    else:
        return value



def read_stick0(hold_stick):
    val = read_i2c_word_stick(I2C_ADDRESS_ARDUINO ,REGISTRE_STICK0)
    if val == 0:
        return hold_stick
    else:
        return val

def read_stick1(hold_stick):
    val = read_i2c_word_stick(I2C_ADDRESS_ARDUINO ,REGISTRE_STICK1)
    if val == 0:
        return hold_stick
    else:
        return val

def read_stick4(hold_stick):
    val = read_i2c_word_stick(I2C_ADDRESS_ARDUINO ,REGISTRE_STICK4)
    if val == 0:
        return hold_stick
    else:
        return val

def read_stick7(hold_stick):
    val = read_i2c_word_stick(I2C_ADDRESS_ARDUINO ,REGISTRE_STICK7)
    if val == 0:
        return hold_stick
    else:
        return val
def read_compas_cmps(hold_compas) :
    compas = read_i2ca(I2C_ADDRESS_CMPS14 ,COMPAS)
    if compas < 0 or compas > 3600:
        compas = hold_compas
    return compas

def read_pitch():
    pitch = bus.read_byte_data(I2C_ADDRESS_CMPS14, PITCH_ANGLE)
    if pitch > 127:
        pitch = pitch - 255
    return pitch

def read_roll():
    roll = bus.read_byte_data(I2C_ADDRESS_CMPS14, ROLL_ANGLE)
    if roll > 127:
        roll = roll - 255
    return roll


def write_i2ca(I2C_SLAVE_ADDRESS, registre ,value):

    # ici transformer les valeur en byte

    bus.write_word_data(I2C_SLAVE_ADDRESS ,registre ,value)

def write_move(value):
    try:
        write_i2ca(I2C_ADDRESS_ARDUINO, REGISTRE_MOVE ,value)
    except:
        pass
def write_rotate(value):
    try:
        write_i2ca(I2C_ADDRESS_ARDUINO, REGISTRE_ROTATE ,value)
    except:
        pass

"""    
# tableau = bytearray(5)  # contient 4 valeur de 0 a 3
val_1 = bytes(3)
bl = 1
stick0 = 0
stick1 = 0
stick4 = 0
stick7 = 0
compas = 0
erreur = 0
t = 0.02
print("bonjour programe lancé")
while True:

    os.system("clear")
    print("STICK0  : " + str(stick0))
    print("STICK1  : " + str(stick1)) 
    print("STICK4  : " + str(stick4)) 
    print("STICK7  : " + str(stick7))  
    print(" COMPAS   : " + str(compas))
    print(" erreur  : " + str(erreur))

    try:


        #print("ca devrais fonctionner")

        stick0 = read_stick0(stick0)
        time.sleep(t)

        stick1 = read_stick1(stick1)
        time.sleep(t)

        stick4 = read_stick4(stick4)
        time.sleep(t)

        stick7 = read_stick7(stick7)        
        time.sleep(t)                    

        compas = read_compas_cmps03()
        time.sleep(t)

        if stick1 > 1200:  # arriere
            move = 1400
        elif stick1 < 800: # avant
            move = 600
        else:
            move = 1000    
        if stick0 > 1200:  # a droite
            rotate = 1400
        elif stick0 < 800: # gauche
            rotate = 600
        else:
            rotate = 1000        

        write_move(move)
        time.sleep(t)
        write_rotate(rotate)


        # time.sleep(0.05)
        time.sleep(0.1)

    except KeyboardInterrupt:
        print("il y a eu  : "+str(erreur)+" erreur")
        break
    except IOError:
        #print("ERREUR" + str(ValueError.args))
        erreur +=1
        #time.sleep(1)
"""




