from laby import *

cree_fenetre(largeur, hauteur)
image(largeur//2, hauteur//2, 'media/room.png',largeur=largeur*2 , hauteur=hauteur*2)
while True:
    ev = donne_ev()
    tev = type_ev(ev)
    message = 'WALL IS YOU'
    texte(largeur//2 - len(message)*10,hauteur//2 - len(message)*2,message,couleur = 'red')
    if tev == 'Quitte':
        ferme_fenetre()
    if tev != None:
        ferme_fenetre()
        cree_fenetre(largeur, hauteur)
        bouton_maps(5) 
        while True:
            ev = donne_ev()
            tev = type_ev(ev)
            if tev == 'ClicGauche':
                if detection_bouton(abscisse_souris(),ordonnee_souris()) == True :
                    map_choisi = choix_map(abscisse_souris() , ordonnee_souris())
                    with open('maps/'+str(map_choisi)+'.txt', encoding='utf-8') as f:
                        maps = f.read()
                    lignes,colonnes = taille_donjon(maps)
                    ferme_fenetre()
                    cree_fenetre(colonnes*100, lignes*100)
                    creation_donjon(donjon_graph, maps)
                    donjon_graphique(colonnes, lignes)
                    placement_mur(donjon_graph)
                    placement_png(lst_png)
                    while True:
                        ev = donne_ev()
                        tev = type_ev(ev)
                        if tev == 'ClicGauche':
                            x,y = abscisse_souris() ,ordonnee_souris()
                            x,y = x - x % 100, y - y% 100
                            pivote_mur(donjon_graph,x//100,y//100)
                        if tev == 'ClicDroit':
                            if nombre_diamant > 0:
                                nombre_diamant -=1
                                x,y = abscisse_souris() ,ordonnee_souris()
                                x,y = x - x % 100, y - y% 100
                                treasure['position'] = x//tc,y//tc
                                image(x+tc//2, y+tc//2, 'media/treasure.png',tag = 'treasure')
                                diamant = True
                        if tev == 'Quitte':
                            ferme_fenetre() 
                        visite=set()
                        visite_d = set()
                        res = intention(donjon_graph,aventurier['position'] , lst_dragons,visite)
                        if diamant:
                            res_d = intention(donjon_graph,aventurier['position'] ,[treasure],visite)
                            visite_d.clear()
                            if res_d != None:
                                    aventurier['position'] = res[0][-1]
                                    lst_dragons[0]['position'] = mouvement_aventurier(res_d[0])
                                    applique_chemin(aventurier, [treasure] , res_d[0])
                        visite.clear()
                        
                        if res != None:
                            if etat_aventurier == 'vivant':
                                aventurier['position'] = res[0][-1]
                                lst_dragons[0]['position'] = mouvement_aventurier(res[0])
                                applique_chemin(aventurier, lst_dragons , res[0])
                        etat_partie = fin_partie(aventurier, lst_dragons)
                        if etat_partie == 0:
                            continue
                        if etat_partie == 1:
                            message = 'Victory!'
                            efface('aventurier')
                            rectangle(colonnes*tc/2 - len(message)*10,
                                      lignes*tc/2 - len(message)*3, 
                                      colonnes*tc/2 + len(message)*5, 
                                      lignes*tc/2  + len(message)*1.5,remplissage='white' ,
                                      couleur= 'green' )
                            texte(colonnes*tc/2 - len(message)*10,lignes*tc/2- len(message)*3,
                                  message)
                        if etat_partie == -1:
                            message = 'You died!'
                            efface('aventurier')
                            etat_aventurier = 'mort'
                            rectangle(colonnes*tc/2 - len(message)*10,
                                      lignes*tc/2 - len(message)*3, 
                                      colonnes*tc/2 + len(message)*5, 
                                      lignes*tc/2  + len(message)*1.5,remplissage='white' ,
                                      couleur= 'red' )
                            texte(colonnes*tc/2 - len(message)*10,lignes*tc/2- len(message)*3,
                                  message)
                            image(aventurier['position'][1]*tc+tc//2, 
                                  aventurier['position'][0]*tc+tc//2,
                                  'media/tombstone.png' ,largeur=(tc//2),hauteur=(tc//2))
                        mise_a_jour()
            if tev == 'Quitte':
                ferme_fenetre()
            mise_a_jour()
    mise_a_jour()

        
    