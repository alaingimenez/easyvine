

import routine_gps

class Parcelle:
    def __init__(self):

        #self.lat = 0
        #self.lon = 0

        #self.point = (self.lat, self.lon)
        #self.name =""
        self.largeur_rang = float(0)
        self.distance_souche = float(0)
        self.cepage = ""
        self.tour = [] # liste des points qui compose la parcelle

        self.quoi = "AMMARE" # par default
        self.an_plant = 0 # c'est l'année ou la souche est planté
        self.hauteur = 0 # c'est la hauteur de la greffe

        self.arroser = False # par default il ne faut pas arroser

        self.travail = "AUCUN"   # AUCUN par default

        self.position = [(.0,.0),self.quoi, self.an_plant, self.hauteur,self.arroser,self.travail]
        self.rang = [] # liste des quoi qui compose les rang | ammare - piquet - souche | il peuvent avoir un travail lié
        self.vigne = [] # liste des rangs et evenement qui compose la vigne

        self.name_evenement = ""
        self.position_evenement = [(0,0),""]
        self.evenement = []
        

    def affiche(self):
        print(self.largeur_rang)
        print(self.distance_souche )
        print(self.cepage)
        print(self.tour)

    def reverse_vigne(self,pos_robot):
        print("pos robot ", pos_robot)
        if pos_robot == 1: # le robot est a cote de la premiere amarre premiere rangé
            pass
        elif pos_robot == 2: # le robot est a coté de la derniere amarre premiere rangé > inverser le sens des souches
            for self.rang in self.vigne:
                self.rang.reverse()

        elif pos_robot == 3: #le robot est a coté de la derniere amarre derniere rangé > inverser le sens rang et souche
            self.vigne.reverse()
            for self.rang in self.vigne:
                self.rang.reverse()

        elif pos_robot == 4: # le robot est a coté de la premiere amarre derniere rangé > inverser le sens des rangs
            self.vigne.reverse()

    def vigne_setend(self):
        """
        permet de savoir si la vigne s'éetend a droite ou a gauche du premier rang
        si il n'y a qu'une seul rang return -1
        :param vigne:
        :return: 0 s'étend a gauche     1 s'étend a droite  -1 il n'y a qu'une seule rangé
        """
        if len(self.vigne) == 1: # il n'y a qu'un seul rang
            return -1
        else:    # il y a plusieur rang
            rang = self.vigne[0]
            depart_rang,quoi,an,hauteur,arrosage,travail = rang[0]
            arrive_rang,quoi,an,hauteur,arrosage,travail = rang[-1]
            cap_rang = routine_gps.get_angle(depart_rang, arrive_rang)
            cap_a_droite = cap_rang + 90
            cap_a_gauche = cap_rang - 90
            point_a_droite = routine_gps.new_pointgpt(depart_rang, cap_a_droite, 0.10)
            point_a_gauche = routine_gps.new_pointgpt(depart_rang, cap_a_gauche, 0.10)

            rang_dernier = self.vigne[-1]
            depart_rang_dernier,quoi,an,hauteur,arrosage,travail = rang_dernier[0]
            distance_droite = routine_gps.get_distance_gps(point_a_droite,depart_rang_dernier)
            distance_gauche = routine_gps.get_distance_gps(point_a_gauche, depart_rang_dernier)

            if distance_droite > distance_gauche:
                cote = 0
            else:
                cote = 1
        return cote

    def cap_rang(self, rang):
        pos_debut,quoi,an,hauteur,arrosage,travail = rang[0]
        pos_fin,quoi,an,hauteur,arrosage,travail = rang[-1]
        cap = routine_gps.get_angle(pos_debut, pos_fin)
        cap_inverse = cap + 180
        if cap_inverse > 360:
            cap_inverse = cap_inverse - 360
        return cap, cap_inverse



"""        
class NewParcelle:
    def __init__(self):

        #self.lat = 0
        #self.lon = 0

        #self.point = (self.lat, self.lon)
        #self.name =""
        self.largeur_rang = float(0)
        self.distance_souche = float(0)
        self.cepage = ""
        self.tour = [] # liste des points qui compose la parcelle

        self.quoi = "AMMARE" # par default
        self.an_plant = 0 # c'est l'année ou la souche est planté
        self.hauteur = 0 # c'est la hauteur de la greffe

        self.arroser = False # par default il ne faut pas arroser

        self.travail = "AUCUN"   # AUCUN par default

        self.position = [(.0,.0),self.quoi, self.an_plant, self.hauteur,self.arroser,self.travail]
        self.rang = [] # liste des quoi qui compose les rang | ammare - piquet - souche | il peuvent avoir un travail lié
        self.vigne = [] # liste des rangs et evenement qui compose la vigne

        self.name_evenement = ""
        self.position_evenement = [(0,0),""]
        self.evenement = []
"""
    

