#robot
import routine_gps

class Robot:
    def __init__(self):
        self.empattement = 1 # longueur
        self.voie = 1 # largeur
        self.longueur = 1.5
        self.largeur  = 1
        self.hauteur = 0.8
        self.distance_gps_essieux_avant = 0 # en metre si positif vers l'avant si negatif vers l'arriere
        self.distance_gps_centre = 0 # en metre si positif vers la droite si negatif vers la gauche
        self.largeur_travail = 0.20 # en metre
        self.travail_decalage = 0 # en metre  si positif le traval est decale a droite si negatif decalé a gauche
        self.distance_outil_rang = 0.05 
        self.position = (0,0) # position actuelle du robot

        self.parcour = [] # liste de tuple 

    def robot_a_cote(self, vigne): # vigne
        """
        rechercher de quel cote de la vigne le robot est le plus pret

        :param position_robot: latitude,longitude
        :param vigne: liste des rangs de la vigne avec adresse de depart et d'arrive de chaque rang
        :return:
        1 le robot est a coté du debut de la digitalisation de la vigne
        2 le robot est a coté de la fin de la premiere rangé  digitalisée
        3 le robot est a coté du debut de la derniere rangé  digitalisée
        4 le robot est a coté de la fin de la derniere rangé  digitalisée
        """
        rang = vigne[0]
        depart_rang1,quoi,an,hauteur,arrosage,travail = rang[0]
        arrive_rang1,quoi,an,hauteur,arrosage,travail = rang[-1]
        distance_depart_rang1 = routine_gps.get_distance_gps(depart_rang1, self.position)
        distance_arrive_rang1 = routine_gps.get_distance_gps(arrive_rang1, self.position)

        if len(vigne) == 1: # 1 seule rangé
            dico_distance = ((distance_depart_rang1, 1),(distance_arrive_rang1, 2))

        else:   # cas normal ou la vigne a plusieur rang
            rang = vigne[-1]
            depart_rang_dernier,quoi,an,hauteur,arrosage,travail = rang[0]
            arrive_rang_dernier,quoi,an,hauteur,arrosage,travail = rang[-1]
            distance_depart_rang_dernier = routine_gps.get_distance_gps(depart_rang_dernier, self.position)
            distance_arrive_rang_dernier = routine_gps.get_distance_gps(arrive_rang_dernier, self.position)
            dico_distance = ((distance_depart_rang1, 1), (distance_arrive_rang1, 2), (distance_depart_rang_dernier, 4) , (distance_arrive_rang_dernier, 3))

        dico_distance = sorted(dico_distance)
        pos , offset_position = dico_distance[0]
        return offset_position
