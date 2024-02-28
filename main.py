

 # placer la fenetre en haut de l'ecran
import os
import fichier
"""
x = 10
y = 10
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y)
"""

import pygame
pygame.init()


import windowfichier
import windowcreat
import windowmodify
import windowdelete
import windowscan
import windowmain
import windowview
import windowrecherch
import windowtravail
import windowpassage
import config

import porteur

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

class Main:
    def __init__(self):
        # RECUPERE LA LISTE DES OUTILS ET DU MATERIEL
        self.list_outil = [config.OUTIL_OBLIGATOIRE]  + fichier.charge_list( config.MATERIEL, config.EXT_OUTILS)
        self.list_porteur = fichier.charge_list(config.MATERIEL, config.EXT_PORTEUR)
        
        

        



def print_hi(name):
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


if __name__ == '__main__':
    print_hi('PyCharm')

    

    # definir le screen
    width = 1500
    heigh = 1000

    plein_ecran = False
    if plein_ecran:
        screen = pygame.display.set_mode((width, heigh) , pygame.FULLSCREEN) # permet un mode plein ecran
    else:
        screen = pygame.display.set_mode((width, heigh) )

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

        elif window_main.index_action == 1: # CREATION
            action = windowcreat.gestion(window_main)

        elif window_main.index_action == 2: # MODIFY
            action = windowmodify.gestion(window_main)

        elif window_main.index_action == 3: # DELETE
            action = windowdelete.gestion(window_main)

        elif window_main.index_action == 4: # scan
            action = windowscan.gestion(window_main)

        elif window_main.index_action == 5: # VIEW
            window_view = windowview.WindowView(window_main)
            action = window_view.gestion()

        elif window_main.index_action == 6: # RECHERCHE
            action = windowrecherch.gestion(window_main)

        elif window_main.index_action == 7: # TRAVAIL
            window_travail = windowtravail.WindowTravail(window_main) # creer l'instance
            action = window_travail.gestion()

        elif window_main.index_action == 8: # PASSAGE
            window_passage = windowpassage.WindowPassage(window_main) # creer l'instance
            action = window_passage.gestion()

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
    
    
    
    


