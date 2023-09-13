


import pygame
pygame.init()

import os
import windowfichier
import windowscan
import windowmain
import windowview
import windowrecherch

from gps import *
import threading





class GpsPoller(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
    self.gpsd = gps(mode=WATCH_ENABLE) #starting the stream of info
    self.current_value = None
    self.running = True #setting the thread running to true

  def run(self):
    while self.running:
      self.gpsd.next() #this will continue to loop and grab EACH set of gpsd info to clear the buffer


gpsp = GpsPoller() # create the thread
gpsp.start() # start it up


def print_hi(name):
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


if __name__ == '__main__':
    print_hi('PyCharm')

    # definir le screen
    width = 1000
    heigh = 1000
    #deb_x = 0
    #fin_y = 0
    #fin_x, deb_y = width, heigh
    screen = pygame.display.set_mode((width, heigh))

    window_main = windowmain.WindowMain(screen) # je cree un objet window_main

    #action = 3 # les action sont decrite dans windowmain
    is_running = True
    while is_running:

        #print (gpsp.gpsd.fix.latitude)

        try:
            pass
            #holdcompas = 0
            #compascmps = read_compas_cmps(holdcompas)
            #pitch = read_pitch()
            #roll = read_roll()
            #print("compas cmps : " ,compascmps, "   pitch : ", pitch, "   roll : ", roll)
            
        except KeyboardInterrupt:
            is_running = False
        except IOError:
            pass
            #erreurio +=1
        #print ("index_action : " + str (window_main.index_action))
        if window_main.index_action == 0: # fichier
            action = windowfichier.gestion(window_main)

        elif window_main.index_action == 1: # creat
            pass

        elif window_main.index_action == 2: # scan
            action = windowscan.gestion(window_main)

        elif window_main.index_action == 3: # VIEW
            window_view = windowview.WindowView(window_main)
            action = window_view.gestion()

        elif window_main.index_action == 4: # RECHERCHE
            action = windowrecherch.gestion(window_main)

        if window_main.index_action == -99: # il faut arreter le prg
            is_running = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if window_main.bouton_action_gRect.collidepoint(event.pos): # a supprimer quand toute les fenetre seront ok car je recrer c'est objet dans chaque fentre
                    action = window_main.dec_action_actuelle()
                elif window_main.bouton_action_dRect.collidepoint(event.pos):
                    action = window_main.inc_action_actuelle()


        pygame.display.update()

    
    print ("\nKilling Thread...")
    gpsp.running = False
    gpsp.join() # wait for the thread to finish what it's doing
    pygame.quit()
    print('quitter le prg' )
    quit()
    
    
    
    


