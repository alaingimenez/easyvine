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

        self.buton_g = self.font.render("<< :", True, config.YELLOW, config.GRAY)
        self.buton_gRect = self.buton_g.get_rect()
        self.buton_gRect.x = 10
        self.buton_gRect.y = 10

        self.module = self.font.render(str(self.list_module[self.index]), True, config.GREEN, config.BLUE)
        self.moduleRect = self.module.get_rect()
        self.moduleRect.x = 70
        self.moduleRect.y = 10

        self.buton_d = self.font.render(": >>", True, config.YELLOW, config.GRAY)
        self.buton_dRect = self.buton_d.get_rect()
        self.buton_dRect.x = 285
        self.buton_dRect.y = 10

        self.buton_simu = self.font.render("|SIMU|", True, config.YELLOW, config.RED)
        self.buton_simuRect = self.buton_simu.get_rect()
        self.buton_simuRect.x = 350
        self.buton_simuRect.y = 10

        self.buton_redo = self.font.render("|-----|", True, config.YELLOW, config.GRAY)
        self.buton_redoRect = self.buton_redo.get_rect()
        self.buton_redoRect.x = 470
        self.buton_redoRect.y = 10

        self.buton_save = self.font.render("|SAVE|", True, config.YELLOW, config.GRAY)
        self.buton_saveRect = self.buton_save.get_rect()
        self.buton_saveRect.x = 610
        self.buton_saveRect.y = 10

        self.buton_del = self.font.render("|DEL|", True, config.YELLOW, config.GRAY)
        self.buton_delRect = self.buton_del.get_rect()
        self.buton_delRect.x = 740
        self.buton_delRect.y = 10

        


        self.update()

    def update(self):
        self.module = self.font.render(str(self.list_module[self.index]), True, config.GREEN, config.BLUE)
        self.screen.blit(self.buton_g, self.buton_gRect)
        self.screen.blit(self.module, self.moduleRect)
        self.screen.blit(self.buton_d,self.buton_dRect)
        self.screen.blit(self.buton_simu, self.buton_simuRect)
        self.screen.blit(self.buton_redo, self.buton_redoRect)
        self.screen.blit(self.buton_save, self.buton_saveRect)
        self.screen.blit(self.buton_del, self.buton_delRect)

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