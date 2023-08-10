

"""

    CETTE FICHIER C'EST APPELE segmenter_route.py jusqu'au 28/02/2023  depuis elle s'appelle routine_gps.py

"""
#from math import sin, cos, acos, pi,radians,sqrt,atan2,degrees,sqrt,radians,tan,log
import math
from geopy.distance import geodesic
from geopy.point import Point


#################################################################################
def segmenter_route(point_depart, point_arrive, longueur_segment):
    """
    cette routine vas calculer la distance entre le point de depart et le point d'arrivé.
    ensuite elle vas segmenter cette route de point GPS tous les +-longueur_segment demandée
    ELLE AJOUTE DE LE POINT DE VISE QUI SE TROUVE APRES LE DERNIER POINT
    et retourne une liste de tous ces points gps.

    :param latitude_depart:
    :param longitude_depart:
    :param latitude_arrive:
    :param longitude_arrive:
    :param longueur_segment:
    :return: liste_point
    """
    latitude_depart, longitude_depart = point_depart
    latitude_arrive, longitude_arrive = point_arrive

    # calculer la distance entre les 2 points
    pointA = point_depart
    pointB = point_arrive
    distance = distanceGPS(pointA, pointB)
    #print(("DISTANCE   : ") + str(distance))

    # diviser cette distance par longueur_segment pour connaitre le nombre de segment de +-longueur_segment a suivre
    # pour les essai je divise par 1 pour avoir un point tous les mettre
    nb_segment = int(distance / longueur_segment)

    # calculer les coordonnées du point a chaque bout de segment a savoir que le dernier segment a pour point d'arriver latitude_arrive,longitude_arrive
    total_segment = nb_segment
    # print("depar : " + ("   latitude , longitude  : " + str(latitude_depart) + "," + str(longitude_depart)))
    #print(" sous routine total_segment  : " + str(total_segment))
    liste_point = []
    for case in range(1, total_segment):
        latitude = latitude_depart + (latitude_arrive - latitude_depart) * (1/nb_segment)
        longitude = longitude_depart + (longitude_arrive - longitude_depart) * (1/nb_segment)
        liste_point.append(latitude)
        liste_point.append(longitude)

        #print("case  : " + str(case) + ("   latitude , longitude  : " + str(latitude) + "," + str(longitude)))
        nb_segment -= 1
        latitude_depart = latitude
        longitude_depart = longitude
        print(" nb segment : " + str(nb_segment)+ "   case : " + str(case))
    # print("ARRIVE   : " + ("   latitude , longitude  : " + str(latitude_arrive) + "," + str(longitude_arrive)))
    liste_point.append(latitude_arrive)
    liste_point.append(longitude_arrive)
    liste_point = aiming_point(liste_point)  # rajouter le dernier point de vise
    return liste_point # total_segment + 1
#############################################################################

#############################################################################
def distanceGPS(pointA,pointB):
    """Retourne la distance en mètres entre les 2 points A et B connus grâce à
       leurs coordonnées GPS
    """
    latA, longA = pointA
    latB, longB = pointB
    distance = math.acos(math.sin(math.radians(latA))*math.sin(math.radians(latB))+math.cos(math.radians(latA))*math.cos(math.radians(latB))*math.cos(math.radians(longA-longB)))*6371*1000
    # distance entre les 2 points, comptée sur un arc de grand cercle
    return distance
#############################################################################

#############################################################################
def get_distance_gps(pointA, pointB):
    """Retourne la distance en mètres entre les 2 points A et B connus grâce à
       leurs coordonnées GPS
    """

    lat1,lon1 = pointA
    lat2,lon2 = pointB
    R = 6371.0  # Rayon de la terre en km chat GPS donné 6373
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c * 1000  # la distance en mètre
#############################################################################

#############################################################################
def aiming_point(list_point):
    """
    ajoute un point gps a la fin de la liste ce point se trouve apres le dernier point de la liste,
    sa distance avec le dernier point de la liste est = a la distance dernier point a avant dernier point

    :param list_point: la liste doit etre composée de point gps en ligne droite latitude,longitude,etc
    :return: la liste avec le nouveau point
    """
    total_point = len(list_point)
    nb_segement = total_point / 2
    #print("la liste a : " + str(total_point) + " points")
    lat_arrive = list_point[total_point - 2]
    long_arrive = list_point[total_point - 1]
    lat_avant_arrive = list_point[total_point - 4]
    long_avant_arrive = list_point[total_point - 3]
    #print(" latitude et longitude AVANT ARRIVE : " + str(lat_avant_arrive) + "," + str(long_avant_arrive))
    #print(" latitude et longitude d'ARRIVE : " + str(lat_arrive) + "," + str(long_arrive))
    lat_vise = lat_avant_arrive+(lat_arrive - lat_avant_arrive) * 2   # *2 permet de placer le point d'arriver au centre les point avant_arrive et point de vise
    long_vise = long_avant_arrive + (long_arrive - long_avant_arrive) * 2
    #print(" latitude et longitude VISE : " + str(lat_vise) + "," + str(long_vise))
    list_point.append(lat_vise)
    list_point.append(long_vise)
    return list_point
###############################################################################

###############################################################################
# remplacé par new_pointgpt(point_origin, cap, distance)
def rotate(origin, point,angle):# remplacé par new_pointgpt(point_origin, cap, distance)
    """
    C'EST MOI QUI AI CREER CETTE ROUTINE JE PENSE QUE L'ANGLE 90° N'EST PAS BON
    fait tourner le point point autour du point origin d'une angle angle en degré

    il vaut mieux utiliser la routine ci dessou
    new_pointgpt(point_origin, cap, distance)

    :param origin: latitude , longitude
    :param point:  latitude , longitude
    :param angle:  en degré
    :return:  latitude , longitude
    """
    angle = math.radians(angle)
    distance_a_respecter = distanceGPS(origin, point)  # memorise la distance avec le point a rotater
    ox, oy = origin
    px, py = point
    qx = ox +math. cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
    qy = oy + math.sin(angle) * (px - ox) +math. cos(angle) * (py - oy)
    new_point = (qx, qy)
    qx, qy = point_a_distance(origin, new_point, distance_a_respecter) # met le point rotater a la distance memorise
    return qx, qy
#################################################################################

#################################################################################
# remplacé par new_pointgpt(point_origin, cap, distance)
def point_a_distance(origin, point,distance):

    """
    C'EST MOI QUI AI CEER CETTE ROUTINE IL FAUT LA VERIFIER JE NE SUIS PAS SUR
    cree un nouveau point a la distance distance du point origin en direction du point point

    il vaut mieux utiliser la routine ci dessou
    new_pointgpt(point_origin, cap, distance)

    :param origin: latitude , longitude
    :param point:  latitude , longitude
    :param distance: en metre
    :return: latitude , longitude
    """
    d_actuel = distanceGPS(origin, point)

    p_lat, p_long = point
    o_lat, o_long = origin

    lat = o_lat + (p_lat - o_lat) * (distance / d_actuel )
    long = o_long + (p_long - o_long) * (distance / d_actuel )

    return lat, long
#######################################################################################

#################################################################################
def new_pointgpt(point_origin, cap, distance):
    """
    cette routine creer un nouveau point dans la direction cap a la distance distance du point_origin
    :param point_origin:  latitue,longitude
    :param cap:  en °
    :param distance: en metre
    :return:  nouveau point  latidue,longitude
    """

    lat1,long1 = point_origin

    # conversion des angles en radians
    angle_radians = math.radians(cap)

    # conversion de la distance en degrés de latitude et de longitude
    latitude_degrees = float(distance / 111111)
    longitude_degrees = float(distance / (111111 *math. cos(math.radians(lat1))))

    # calcul des nouvelles coordonnées
    lat2 = lat1 + latitude_degrees * math.cos(angle_radians)
    long2 = long1 + longitude_degrees * math.sin(angle_radians)
    return lat2, long2
#######################################################################################

#######################################################################################
def get_angle(point_A, point_B):
    """
    renvoie le cap du point_A vers point_B
    :param lat_point_A:
    :param long_poin_A:
    :param lat_poin_B:
    :param longitudeDest:
    :return:  le cap du point_A vers point_B
    """
    lat_point_A, long_point_A = point_A
    lat_point_B, long_point_B = point_B

    delta_long = long_point_B - long_point_A
    y = math.sin(delta_long) * math.cos(lat_point_B)

    x = math.cos(lat_point_A) * math.sin(lat_point_B) - math.sin(lat_point_A) * math.cos(lat_point_B) *math.cos(delta_long)
    angle = math.degrees(math.atan2(y, x))
    while (angle < 0):
        angle += 360  # angle % 360
    return angle % 360
##########################################################################
##############################################################################


################################
##################################################
#################################################################





#############################
############################################*
##########################################################
#########################################################################


#################################################################################################################
#################################################################################################
######################################################################################################


def calculate_distance(point, segment_start, segment_end):
    # calcule la distance perpendiculaire d'un point a un segment
    # ou si le point est a l'exteiur du segment avec les extrémités du segment
    lat, long = point
    point = Point(latitude=lat, longitude=long)
    lat1, long1 = segment_start
    segment_start = Point(latitude=lat1, longitude=long1)  # Coordonnées du premier point du segment
    lat2, long2 = segment_end
    segment_end = Point(latitude=lat2, longitude=long2)  # Coordonnées du deuxième point du segment



    dist_start = geodesic(point, segment_start).meters
    dist_end = geodesic(point, segment_end).meters

    # Calcul de la distance entre le point et le segment
    segment_distance = geodesic(segment_start, segment_end).meters

    # Si le point est en dehors des extrémités du segment, la distance est la plus petite distance entre le point et les extrémités
    if dist_start >= segment_distance and dist_end >= segment_distance:
        perpendicular_distance = min(dist_start, dist_end)
    else:
        # Calcul de la distance perpendiculaire
        a = geodesic(segment_start, point).meters
        b = geodesic(segment_end, point).meters
        c = geodesic(segment_start, segment_end).meters
        s = (a + b + c) / 2  # Semi-périmètre
        area = math.sqrt(s * (s - a) * (s - b) * (s - c))  # Calcul de l'aire du triangle
        perpendicular_distance = 2 * area / c  # Distance perpendiculaire

    return perpendicular_distance

#####################################################################################################################
##########################################################################################################################
##############################                   SEGMENT QUI SE CROISE                       ###########################

def check_segments_intersection(seg1_start, seg1_end, seg2_start, seg2_end):
    def orientation(p, q, r):
        # Calcul de l'orientation du triplet (p, q, r)
        val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])

        if val == 0:
            return 0  # Les points sont colinéaires
        elif val > 0:
            return 1  # Orientation horaire
        else:
            return -1  # Orientation anti-horaire

    def on_segment(p, q, r):
        # Vérification si le point q se situe sur le segment pr
        if (q[0] <= max(p[0], r[0]) and q[0] >= min(p[0], r[0]) and
                q[1] <= max(p[1], r[1]) and q[1] >= min(p[1], r[1])):
            return True
        return False

    # Calcul des orientations pour les segments et les points d'extrémité
    o1 = orientation(seg1_start, seg1_end, seg2_start)
    o2 = orientation(seg1_start, seg1_end, seg2_end)
    o3 = orientation(seg2_start, seg2_end, seg1_start)
    o4 = orientation(seg2_start, seg2_end, seg1_end)

    # Vérification des cas d'intersection
    if (o1 != o2 and o3 != o4) or (o1 == 0 and on_segment(seg1_start, seg2_start, seg1_end)) or (
            o2 == 0 and on_segment(seg1_start, seg2_end, seg1_end)) or (
            o3 == 0 and on_segment(seg2_start, seg1_start, seg2_end)) or (
            o4 == 0 and on_segment(seg2_start, seg1_end, seg2_end)):
        return True  # Les segments se croisent
    else:
        return False  # Les segments ne se croisent pas



