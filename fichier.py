"""

"""


import os
import pickle

class Fichier:
    def __init__(self):

        self.chemin_disk = "vigne/"
        self.list = os.listdir(self.chemin_disk)  # liste des noms des fichier parcelle qu'il y a sur le disk
        # enlever le .prc
        l = []
        for i in self.list:
            i = (i[:-4])
            l.append(i)
        self.list = l
        self.list.sort()

    def get_list(self):
        return self.list

    def add_name_file_in_list(self, name_file):
        self.list.append(name_file)
        self.list.sort()

    def del_name_file_in_list(self, name_file):
        self.list.remove(name_file)


    def save_file(self,name, parcelle):
        file = open(self.chemin_disk + name + ".prc","wb")
        pickle.dump(parcelle, file)
        file.close()

        """
        with open(self.chemin_disk + name + ".prc","wb") as file:
            pickle.dump(parcelle, file)
        """

    def load_parcelle(self, name):
        file = open(self.chemin_disk + name + ".prc", "rb")
        parcel = pickle.load(file)
        file.close()
        return parcel

    def delete_file(self,name):
        os.remove(self.chemin_disk + name + ".prc")

    def ancien_V_parcel_load(self, name): # permet de reprendre les donne des ancienne version de EasyVine
        with open(self.chemin_disk + name + ".vig", "rb") as file:
            list = pickle.load(file)
            return list
        
    def save_essai(self,name, essai):
        file = open(self.chemin_disk + name + ".prc","wb")
        pickle.dump(essai, file)
        file.close()

    def load_essai(self, name):
        file = open(self.chemin_disk + name + ".prc", "rb")
        essai = pickle.load(file)
        file.close()
        return essai