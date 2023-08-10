



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
        

