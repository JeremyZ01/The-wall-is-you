from random import randint
from collections import deque
from laby import *
from fltk import *
from media import *
import time
from random import choice

aventurier = {
    'position':(0,0),
    'niveau':1 
    }
dragon1 = {
    'position': None,
    'niveau':1}
dragon2 = {
    'position': None,
    'niveau':2}
dragon3 = {
    'position': None,
    'niveau':3}
treasure = {
    'position': None,
    'niveau': 0
    }
lst_dragons = [dragon1,dragon2,dragon3]
dragons_accessibles = []

def pivoter(donjon,position):
    """
    Effectue une rotation des éléments de la salle située à la position donnée 
    dans le sens horaire.

    """
    salle = donjon[position[0]][position[1]]
    donjon[position[0]][position[1]] = (salle[-1],salle[0],salle[1],salle[2])

def connecte(donjon, p1, p2):
    """
    Vérifie si deux salles dans le donjon sont connectées.
    """
    a1, a2 = p1
    b1, b2 = p2
    d_p1 = donjon[a1][a2]
    d_p2 = donjon[b1][b2]
    if a1 < b1:
        if d_p1[2] and d_p2[0]:
            return True
    elif a2 < b2:
        if d_p1[1] and d_p2[-1]:
            return True
    elif b1 < a1:
        if d_p2[2] and d_p1[0]:
            return True
    elif b2 < a2:
        if d_p2[1] and d_p1[-1]:
            return True
    return False

def les_voisins(position,donjon):
    """
    Renvoie une liste des positions des salles voisines dans le donjon, 
    à partir d'une position donnée.

    """
    
    x,y = position
    deplacements = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    positions = []
    for dx, dy in deplacements:
        new_x, new_y = x + dx, y + dy
        if 0 <= new_x < len(donjon) and 0 <= new_y < len(donjon[0]):
            positions.append((new_x, new_y))
    return positions

def intention(donjon, position, dragons, visite):
    '''
    Détermine l'intention de déplacement à partir d'une position donnée 
    dans le donjon, en prenant en compte la présence de dragons et les 
    connexions entre les salles.    

    '''
    for dragon in dragons:
        if position == dragon['position']:
            return ([position], dragon['niveau'])
    
    if position in visite:
        return None

    visite.add(position)
    res = []
    if position != None:
        for cible in les_voisins(position, donjon):
            if connecte(donjon, position, cible):
                chemin = intention(donjon, cible, dragons, visite)
                if chemin is not None:
                    res.append(chemin)
    if not res:
        return None
    meilleur_chemin = max(res, key=lambda x: x[1])
    return ([position] + meilleur_chemin[0], meilleur_chemin[1])

def rencontre(aventurier,dragons):
    """
    Simule une rencontre entre un aventurier et des dragons, 
    en vérifiant si l'aventurier est capable de les vaincre.
    """
    for dragon in dragons:
        if aventurier['niveau'] < dragon['niveau']:
            return False
        if aventurier['niveau'] >= dragon['niveau']:
            dragons.remove(dragon)
            return True

def applique_chemin(aventurier,dragons,chemin):
    """
    Applique un chemin donné à un aventurier en rencontrant des dragons le long du chemin.
    """
    for position in chemin:
        aventurier['position'] = position
        for dragon in dragons:
                if dragon['position'] == aventurier['position']:
                    rencontre(aventurier,dragons)
def fin_partie(aventurier,dragons):
    """
    Vérifie les conditions de fin de partie dans un jeu d'aventure avec des dragons.
    """
    dragon_vivant = 0
    for dragon in dragons:
        if dragon['position'] != None:
            dragon_vivant+=1
        if dragon['position'] == aventurier['position']:
            if aventurier['niveau'] < dragon['niveau']:
                return -1
            else:
                return 0
    if dragon_vivant == 0:
        return 1

donjon_graph = []
def creation_donjon(donjon_graph,maps):
        maps = maps.replace(' ','')
        print(maps)
        l = []
        mmaps = True
        compteur = 0
        for element in range(len(maps)):
            if maps[element] == '╬':
                l.append((True,True,True,True))
            elif maps[element] == '╠':
                l.append((True,True,True,False))
            elif maps[element] == '╣':
                l.append((True,False,True,True))
            elif maps[element] == '╩':
                l.append((True,True,False,True))
            elif maps[element] == '╦':
                l.append((False,True,True,True))
            elif maps[element] == '╔':
                l.append ((False,True,True,False))
            elif maps[element] == '╗':
                l.append((False,False,True,True))
            elif maps[element] == '╝':
                l.append((True,False,False,True))
            elif maps[element] == '╚':
                l.append((True,True,False,False))
            elif maps[element] == '═':
                l.append((False,True,False,True))
            elif maps[element] == '║':
                l.append((True,False,True,False))   
            elif maps[element] == '╨':
                l.append((True,False,False,False))
            elif maps[element] == '╞':
                l.append((False,True,False,False))
            elif maps[element] == '╥':
                l.append((False,False,True,False))  
            elif maps[element] == '╡':
                l.append((False,False,False,True))            
            elif maps[element] == '\n' and mmaps == True:
                donjon_graph.append(l)
                l= []
            elif maps[element] == 'A':
                aventurier['position'] = (int(maps[element+1]),int(maps[element+2]))
                mmaps = False
            elif maps[element] == 'D':
                lst_dragons[compteur]['position'] = (int(maps[element+1]),int(maps[element+2]))
                compteur += 1

def taille_donjon(maps):
    """
    Détermine la taille du donjon à partir de la carte.
    """
    ligne = 0
    colonne = 0
    for i in range(len(maps)):
        if maps[i] == '\n':
            ligne += 1
        if ligne == 0:
            colonne+=1
        elif maps[i] == 'A':
            return ligne,colonne



largeur = 500
hauteur = 500
largeur_bouton = 100
hauteur_bouton = 50
ouvrir_map = False
tc = 100
lst_png = [aventurier,dragon1,dragon2,dragon3]
etat_aventurier = 'vivant'
nombre_diamant = 1
diamant =False
def bouton_maps(x):
    '''
    Crée des boutons pour les différentes maps du jeu.
    '''
    compteur = 0
    for bouton in range(x):
        rectangle(largeur/2 - largeur_bouton, hauteur/5 * bouton, 
                  largeur/2 + largeur_bouton, 
                  hauteur/5 * bouton  + hauteur_bouton , couleur = 'black', 
                  tag = 'bouton'+ str(bouton))
        if compteur == 0:
            texte(largeur/2-largeur/10,hauteur/5 * bouton , 'Map_test')
        else:
            texte(largeur/2-largeur/10,hauteur/5 * bouton ,
                  'Map '+ str(compteur))
        compteur+=1

def detection_bouton(x,y):
    '''
    detecte si le joueur clique sur le bouton
    '''
    if x >= largeur/2 - largeur_bouton and x <= largeur/2 + largeur_bouton:
        numero_map = y - y%hauteur_bouton
        if numero_map % 100 == 0:
            return True
    return False

def choix_map(x,y):
    numero_map = y - y%hauteur_bouton
    if numero_map == 0:
        lamap = 'map_test'
    else:
        lamap = 'map'+str(int(numero_map/100))
    return lamap

def donjon_graphique(colonnes,lignes):
    lst = ['herbe','room']
    texture = choice(lst)
    for ligne in range(lignes):
        for colonne in range(colonnes):
            image(colonne*tc + tc//2,ligne*tc +tc//2, 'media/'+texture+'.png',
                  largeur = 100 ,hauteur = 100)

def mur_gauche(x,y):
    x1 = x - x%100
    y1 = y - y%100
    rectangle(x1, y1, x1+15, y1 + 100 ,remplissage='black',
              tag= 'mur'+str(x//100)+str(y//100))
    
def mur_droite(x,y):
    x1 = x + (100-x%100)
    y1 = y - y %100
    rectangle(x1 - 15, y1, x1, y1 + 100 ,remplissage = 'black',
              tag= 'mur'+str(x//100)+str(y//100))

def mur_haut(x,y):
    x1 = x - x % 100
    y1 = y - y % 100
    rectangle(x1 , y1 , x1 + 100 , y1 + 15, remplissage = 'black',
              tag = 'mur'+str(x//100)+str(y//100))

def mur_bas(x,y):
    x1 = x - x % 100
    y1 = y + (100 - y % 100)
    rectangle(x1,y1-15,x1+100, y1, remplissage = 'black',
              tag= 'mur'+str(x//100)+str(y//100))

def dessine_chemin(lst):
    """
    Dessine un chemin sur l'écran en reliant les positions de la liste donnée.
    """
    compteur = 0
    for (x, y), (x1, y1) in zip(lst, lst[1:]):
        compteur+=1
        x, y = int(x) * tc + (tc // 2), int(y) * tc + (tc // 2)
        x1 , y1 = int(x1) * tc + (tc // 2), int(y1) * tc + (tc // 2)
        ligne(y, x, y1, x1, couleur='red', epaisseur = 5, tag ='trait')



def placement_mur(lst):
    tc = 100
    for l in range(len(lst)):
        for c in range(len(lst[l])):
            if lst[l][c][0] != True:
                mur_haut(c*tc, l*tc)
            if lst[l][c][1] != True:
                mur_droite(c*tc,l*tc)
            if lst[l][c][2] != True:
                mur_bas(c*tc, l*tc)
            if lst[l][c][3] != True:
                mur_gauche(c*tc, l*tc)

def pivote_mur(donjon,x,y):
    efface('mur'+ str(x) + str(y))
    pivoter(donjon,(y,x))
    if donjon[y][x][0] != True:
        mur_haut(x*tc, y*tc)
    if donjon[y][x][1] != True:
        mur_droite(x*tc,y*tc)
    if donjon[y][x][2] != True:
        mur_bas(x*tc, y*tc)
    if donjon[y][x][3] != True:
        mur_gauche(x*tc, y*tc)
def mouvement_aventurier(lst):
    """
    Anime le mouvement de l'aventurier le long du chemin donné.
    """
    debut=lst[0]
    fin = lst[-1]
    compteur = 0
    for x,y in lst:
        efface('trait')
        dessine_chemin(lst[compteur:])
        compteur+=1
        x,y = int(x)*tc+(tc//2),int(y)*tc+(tc//2)
        efface('aventurier')
        image(y,x,'media/Knight_s.png',largeur=(tc//2),
              hauteur=(tc//2),tag='aventurier')
        texte(y+15,x-35,aventurier['niveau'],taille=16 ,tag='aventurier')
        time.sleep(0.3)
        mise_a_jour()
    for dragon in lst_dragons:
        if dragon['position'] == lst[-1]:
            efface(str('dragon'+str(dragon['niveau'])))
            efface('aventurier')
            if dragon['niveau'] <= aventurier['niveau']:
                aventurier['niveau'] += 1
            image(y,x,'media/Knight_s.png',largeur=(tc//2),
                  hauteur=(tc//2),tag='aventurier')
            texte(y+15,x-35,aventurier['niveau'],taille=16 ,tag='aventurier')
            return lst[-1]
def placement_png(lst):
    """
    Place les images des personnages (aventurier et dragons) 
    sur les positions spécifiées dans la liste donnée
    """
    for i in range(len(lst)):
        if lst[i]['position'] == None:
            continue
        if lst[i]['position'] != None:

            x,y = lst[i]['position'][0],lst[i]['position'][1]
            x,y = int(x)*tc+(tc//2),int(y)*tc+(tc//2)
        if lst[i] == aventurier:
            image(y,x,'media/Knight_s.png',largeur=(tc//2),hauteur=(tc//2),
                  tag='aventurier')
            texte(y+15,x-35,str(i+1),taille=16 ,tag='aventurier')
        else:
            image(y, x, 'media/Dragon_s.png',largeur=(tc//2),hauteur=(tc//2),
                  tag='dragon'+str(lst_dragons[i-1]['niveau']))
            texte(y+15,x-35,str(lst_dragons[i-1]['niveau']),taille=16,
                  tag='dragon'+str(lst_dragons[i-1]['niveau']))















