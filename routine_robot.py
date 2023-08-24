
# CETTE ROUTINE N'EST PLUS UTILISER
#routine_robot
import routine_gps


def robot_a_cote(position_robot,vigne):
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
    distance_depart_rang1 = routine_gps.get_distance_gps(depart_rang1, position_robot)
    distance_arrive_rang1 = routine_gps.get_distance_gps(arrive_rang1,position_robot)

    if len(vigne) == 1: # 1 seule rangé
        dico_distance = ((distance_depart_rang1, 1),(distance_arrive_rang1, 2))

    else:   # cas normal ou la vigne a plusieur rang
        rang = vigne[-1]
        depart_rang_dernier,quoi,an,hauteur,arrosage,travail = rang[0]
        arrive_rang_dernier,quoi,an,hauteur,arrosage,travail = rang[-1]
        distance_depart_rang_dernier = routine_gps.get_distance_gps(depart_rang_dernier, position_robot)
        distance_arrive_rang_dernier = routine_gps.get_distance_gps(arrive_rang_dernier, position_robot)
        dico_distance = ((distance_depart_rang1, 1), (distance_arrive_rang1, 2), (distance_depart_rang_dernier, 4) , (distance_arrive_rang_dernier, 3))

    dico_distance = sorted(dico_distance)
    pos , offset_position = dico_distance[0]
    return offset_position
        