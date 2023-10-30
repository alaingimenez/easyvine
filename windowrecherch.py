# windowrecherch

import config
import parcelle
import sys
import pygame
pygame.init()

import windowrecherchevenement
import windowrecherchtravaux


class Module: # permet de choisir le module qui vas etre utiliser    EVENEMENT / TRAVAUX
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font('freesansbold.ttf', 33)
        

        self.list_module = ["EVENEMENT", "TRAVAUX"] # pour rajouter un module il faut rajouter sa window qui le gere
        self.nb_module = len(self.list_module) # quantité de module
        self.index = 0

        self.mode_simulation = True
        self.indice_vitesse = 1
        self.simulation_arret = False #  si  self.simulation_arret = True on est plus en mode simulation

        self.flag_parcours = False # si = True le parcour est en cours

        self.buton_g = self.font.render("<< :", True, config.YELLOW, config.GRAY)
        self.buton_gRect = self.buton_g.get_rect()
        self.buton_gRect.x = 10
        self.buton_gRect.y = 15

        self.module = self.font.render(str(self.list_module[self.index]), True, config.GREEN, config.BLUE)
        self.moduleRect = self.module.get_rect()
        self.moduleRect.x = 70
        self.moduleRect.y = 15

        self.buton_d = self.font.render(": >>", True, config.YELLOW, config.GRAY)
        self.buton_dRect = self.buton_d.get_rect()
        self.buton_dRect.x = 285
        self.buton_dRect.y = 15

        self.buton_simu = self.font.render("|SIMU|", True, config.YELLOW, config.RED)
        self.buton_simuRect = self.buton_simu.get_rect()
        self.buton_simuRect.x = 350
        self.buton_simuRect.y = 15

        self.buton_parcours = self.font.render("|PARCOURS|", True, config.YELLOW, config.GRAY)
        self.buton_parcoursRect = self.buton_parcours.get_rect()
        self.buton_parcoursRect.x = 460
        self.buton_parcoursRect.y = 15

        self.buton_libelle_vitesse = self.font.render(str(self.indice_vitesse), True, config.YELLOW, config.GRAY)
        self.buton_libelle_vitesseRect = self.buton_libelle_vitesse.get_rect()
        self.buton_libelle_vitesseRect.x = 720
        self.buton_libelle_vitesseRect.y = 15

        self.buton_plus_vite = self.font.render("|+|", True, config.YELLOW, config.GRAY)
        self.buton_plus_viteRect= self.buton_plus_vite.get_rect()
        self.buton_plus_viteRect.x = 680
        self.buton_plus_viteRect.y = 15

        self.buton_moins_vite = self.font.render("|-|", True, config.YELLOW, config.GRAY)
        self.buton_moins_viteRect= self.buton_moins_vite.get_rect()
        self.buton_moins_viteRect.x = 760
        self.buton_moins_viteRect.y = 15

        self.buton_clear = self.font.render("|CLEAR|", True, config.YELLOW, config.GRAY)
        self.buton_clearRect = self.buton_clear.get_rect()
        self.buton_clearRect.x = 800
        self.buton_clearRect.y = 15

        self.buton_repare = self.font.render("|REPARER|", True, config.YELLOW, config.GRAY)
        self.buton_repareRect = self.buton_repare.get_rect()
        self.buton_repareRect.x = 1300
        self.buton_repareRect.y = 200

        self.buton_valid_repare = self.font.render("|VALIDER LES REPARATIONS|", True, config.YELLOW, config.GRAY)
        self.buton_valid_repareRect = self.buton_valid_repare.get_rect()
        self.buton_valid_repareRect.x = 1000
        self.buton_valid_repareRect.y = 15

        self.buton_hd = self.font.render("O", True, config.YELLOW, config.GRAY)
        self.buton_hdRect = self.buton_hd.get_rect()
        self.buton_hdRect.x = 970
        self.buton_hdRect.y = 5

        self.buton_hg = self.font.render("O", True, config.YELLOW, config.GRAY)
        self.buton_hgRect = self.buton_hg.get_rect()
        self.buton_hgRect.x = 942
        self.buton_hgRect.y = 5

        self.buton_bg = self.font.render("O", True, config.YELLOW, config.GRAY)
        self.buton_bgRect = self.buton_bg.get_rect()
        self.buton_bgRect.x = 942
        self.buton_bgRect.y = 40

        self.buton_bd = self.font.render("O", True, config.YELLOW, config.GRAY)
        self.buton_bdRect = self.buton_bd.get_rect()
        self.buton_bdRect.x = 970
        self.buton_bdRect.y = 40

        


        self.update()

    def update(self):
        self.module = self.font.render(str(self.list_module[self.index]), True, config.GREEN, config.BLUE)

        if self.mode_simulation:
            self.buton_simu = self.font.render("|SIMU|", True, config.YELLOW, config.RED)
        else:
            self.buton_simu = self.font.render("|SIMU|", True, config.YELLOW, config.GRAY)

        if self.flag_parcours: # le mode parcour est enclenché
            self.buton_parcours = self.font.render("|PARCOURS|", True, config.YELLOW, config.RED)
        else:
            self.buton_parcours = self.font.render("|PARCOURS|", True, config.YELLOW, config.GRAY)


        self.screen.blit(self.buton_g, self.buton_gRect)
        self.screen.blit(self.module, self.moduleRect)
        self.screen.blit(self.buton_d,self.buton_dRect)
        self.screen.blit(self.buton_simu, self.buton_simuRect)
        self.screen.blit(self.buton_parcours, self.buton_parcoursRect)

        if self.simulation_arret: # True arrete
            self.buton_libelle_vitesse = self.font.render(str(self.indice_vitesse), True, config.YELLOW, config.GRAY)
        else:
            self.buton_libelle_vitesse = self.font.render(str(self.indice_vitesse), True, config.YELLOW, config.RED)

        self.screen.blit(self.buton_libelle_vitesse, self.buton_libelle_vitesseRect)
        self.screen.blit(self.buton_moins_vite, self.buton_moins_viteRect)
        self.screen.blit(self.buton_plus_vite, self.buton_plus_viteRect)
        self.screen.blit(self.buton_repare, self.buton_repareRect)
        self.screen.blit(self.buton_valid_repare, self.buton_valid_repareRect)
        self.screen.blit(self.buton_clear, self.buton_clearRect)
        self.screen.blit(self.buton_hd, self.buton_hdRect)
        self.screen.blit(self.buton_hg, self.buton_hgRect)
        self.screen.blit(self.buton_bd, self.buton_bdRect)
        self.screen.blit(self.buton_bg, self.buton_bgRect)

    def chang_module(self, ofset):
        self.index = self.index + ofset
        if self.index < 0:
         self.index = self.nb_module - 1
        elif self.index == self.nb_module:
         self.index = 0


def gestion(window_m):
    screen = window_m.screen
    module = Module(screen)  # 0 = parcelle   1 = rang   2 = evenement
    parcel = parcelle.Parcelle


    while True:
        if module.index == 0:
            print("recherche evenement")
            window = windowrecherchevenement.WindowRecherchEvenement(window_m, module,parcel)
            ofset = window.gestion()
            del(window)
            module.chang_module(ofset)

        elif module.index == 1:
            print("recherche travaux ")
            window = windowrecherchtravaux.WindowRecherchTravaux(window_m, module, parcel)
            ofset = window.gestion()
            del(window)
            module.chang_module(ofset)






        # teste si l'action n'est plus de rechercher a ce moment la return au main.py pour aller sur la nouvelle action
        if window_m.index_action != 4: # permet de sortir de la windowrecherche
            del(module)
            del(parcel)
            print("window_m.index_action " + str(window_m.index_action))
            return # return a main