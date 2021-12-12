class cellule(object):
    def __init__(self,valeur=0,suivant=None):
        self.valeur = valeur
        self.suivant = suivant

class liste(object):
    def __init__(self,cell=None):
        self.debut = cell

    def __str__(self):  # renvoie l'objet sous forme de chaine de caractère
        resultat = ""
        ptr = self.debut     # on positionne le pointeur sur la première cellule

        while ptr != None:   # tant que le pointeur pointe sur quelque chose
            resultat = resultat + str(ptr.valeur) + ' -> '
            ptr = ptr.suivant   # on fait avancer le pointeur sur la cellule suivante

        return resultat
    
    def liste_vide(self):
        return self.debut == None

    def tete(self):
        return self.debut.valeur
    
    def corps(self):
        return liste(self.debut.suivant)

def construit_liste(valeur,l):
        return liste(cellule(valeur,l.debut))
        

