# This is a sample Python script.

# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import sys
import pygame



pygame.init()

import fichier
import windowfichier
import windowscan
import windowfichierdelete
import windowfichiercreate
import windowscan
import windowalerte
import windowmain
from gps import *
import threading




#gpsd = None # seting the global variable
class GpsPoller(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
    #global gpsd #bring it in scope
    self.gpsd = gps(mode=WATCH_ENABLE) #starting the stream of info
    self.current_value = None
    self.running = True #setting the thread running to true

  def run(self):
    #global gpsd
    while gpsp.running:
      self.gpsd.next() #this will continue to loop and grab EACH set of gpsd info to clear the buffer


gpsp = GpsPoller() # create the thread
gpsp.start() # start it up


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

    # definir le screen
    width = 1000
    heigh = 1000
    #deb_x = 0
    #fin_y = 0
    #fin_x, deb_y = width, heigh
    screen = pygame.display.set_mode((width, heigh))





    #fichier = fichier.Fichier()
    #window_fichier = windowfichier.WindowFichier(screen)
    #window_fichier_create = windowfichiercreate.WindowFichierCreate(screen,fichier)
    #window_fichier_delete = windowfichierdelete.WindowFichierDelete(screen, fichier)
    #window_scan = windowscan.WindowScan(screen)
    window_main = windowmain.WindowMain(screen) # je cree un objet window_main

    #print("window_main " , windowmain)



    action = 0 # les action sont decrite dans windowmain
    

    is_running = True
    while is_running:
        """
        latitude =  gpsp.gpsd.fix.latitude
        
        longitude = gpsd.fix.longitude
        speed = gpsd.fix.speed
        altitude = gpsd.fix.altitude
        jourheure = gpsd.fix.time
        status =  gpsd.fix.status  #gpsd.fix.status  ou mode
        mode = gpsd.fix.mode
        track = gpsd.fix.track   # Degrees from true north
        climb = gpsd.fix.climb
        """

        #print(latitude)

        if action == 0: # fichier
           pass
           #action = windowfichier.gestion(window_main)
        elif action == 1: # creat
            pass
        elif action == 2: # scan
           pass
           # action = windowscan.gestion(window_main)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
                

            if event.type == pygame.MOUSEBUTTONDOWN:
                if window_main.bouton_action_gRect.collidepoint(event.pos): # a supprimer quand toute les fenetre seront ok car je recrer c'est objet dans chaque fentre
                    action = window_main.dec_action_actuelle()

                    print(" click bouton boutonboutno gazuche outil : ", action)
                elif window_main.bouton_action_dRect.collidepoint(event.pos):
                    action = window_main.inc_action_actuelle()
                    print(" click bouton boutonboutno gazuche outil", action)



        pygame.display.update()

    print ("\nKilling Thread...")
    gpsp.running = False
    gpsp.join() # wait for the thread to finish what it's doing
    pygame.quit()
    print('quitter le prg' )



