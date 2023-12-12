# coding=utf-8
import os
import platform
import subprocess
import random
import glob
import sys
import _io
from typing import NewType

try:
    import isnotebook
    _is_notebook = isnotebook.isnotebook()
    if _is_notebook:
        print("is notebook")
        import IPython.display
except Exception:
    _is_notebook = False

#from random import randrange

if sys.hexversion < 3 << 24:
    print("bibgraphes ne fonctionne qu'avec idle3 (python3), pas avec idle (python)")
    sys.exit(1)


# Attention, eviter que les deux noms globaux qui suivent
# aient meme prefixe que les noms "publics"
# proposes par Idle (completion de nom);
# on pourrait evidemment ajouter un _ en tete


__plateforme = platform.system ()
if __plateforme != 'Windows':
    import resource

def _getGraphViz():
    if __plateforme == 'Windows':
        liste = glob.glob('C:/Program Files*/Graphviz*/bin/dot.exe')
        if liste == []:
            print("Graphviz non trouve, la fonction dessiner utilisera le site web GraphvizOnline")
            return ""
        path = liste[0]
        return path[0:-7]
    liste = glob.glob('/usr/bin/dot')
    if liste == []:
        liste = glob.glob('/usr/local/bin/dot')
        if liste == []:
            liste = glob.glob('/opt/local/bin/dot')
            if liste == []:
                print("Graphviz non trouve, la fonction dessiner utilisera le site web GraphvizOnline")
                return ""
    path = liste[0]
    return path[0:-3]


__pathGraphviz = _getGraphViz()


def _errMaj(wrong, right):
    raise Exception("Attention aux majuscules/minuscules: la fonction " + wrong + " n'existe pas, c'est la fonction " + right + " qui existe")

def _errS(wrong, right):
    raise Exception("Attention aux s: la fonction " + wrong + " n'existe pas, c'est la fonction " + right + " qui existe")

def _errOrtho(wrong, right):
    raise Exception("Attention à l'orthographe: la fonction " + wrong + " n'existe pas, c'est la fonction " + right + " qui existe")

def _errAccents(wrong, right):
    raise Exception("Attention à ne pas utiliser d'accent dans Python : la fonction " + wrong + " n'existe pas, c'est la fonction " + right + " qui existe")

################ PRIMITIVES GENERIQUES SUR LES LISTES   ##############

def melange (u: list) -> list:
    """ retourne une copie mélangée aléatoirement de la liste u
    Exemple d'utilisation :

    >>> l2 = melange(l)"""
    v = u[:] # v est une copie de u, Python c'est fun
    random.shuffle (v)
    return v

def elementAleatoireListe(u: list):
    """ Retourne un élément choisi aléatoirement dans la liste
    Exemple d'utilisation :

    >>> x = elementAleatoireListe(range(6))"""
    if u.__class__.__name__ == 'range':
        u = list(u)
    if u.__class__.__name__ != 'list':
        raise __ErreurParametre(u, "une liste")
    # u est une liste
    # La fonction renvoie un element pris au hasard de la liste u si 
    # elle est non-vide. Si u est vide, la fonction renvoie une 
    # erreur (exception IndexError)
    return random.choice(u)



# Changelog JB
#   Ete 2009
#     Grand nettoyage et adaptation a Python 3
#   Septembre 2009: variable globale __plateforme
#     evite deux appels systeme a chaque dessin
#     simplification des fonctions Graphviz et dessinerGraphe
#     (suggestions Jean-Claude Ville)
#   Octobre 2009: utilisation de la mise en forme de chaines
#     (format % valeurs) pour simplifier les representations de classes
#     (methodes __repr__) et la fonction '__dotify'
#   Janvier 2010: fonction 'voisinPar' -> 'sommetVoisin'

################ Classes ########################

class __c_graph:
    def __init__(self, label = '', drawopts = ''):
        self.nodes = []
        self.label = label
        self.drawopts = drawopts    # pour Graphviz
    def __repr__(self):
        return "<graphe: '%s'>" % self.label
graphe = __c_graph

class __c_node:
    def __init__(self, label = '', color = 'white', mark = False, drawopts = ''):
        self.label = label
        self.color = color
        self.mark = mark
        self.edges = []
        self.drawopts = drawopts    # pour Graphviz
    def __repr__(self):
        c = "'" + self.color + "'"
        return "<sommet: '%s', %s, %s>" % (self.label, c, self.mark)
sommet = __c_node

class __c_edge:
    def __init__(self, label = '', start = None, end = None, mark = False, drawopts = ''):
        self.label = label
        self.start = start
        self.end = end
        self.mark = mark
        self.drawopts = drawopts    # pour Graphviz
    def __repr__(self):
        return "<arete: '%s' %s--%s>" % (self.label, self.start.label, self.end.label)
arete = __c_edge

################ PRIMITIVES GRAPHE   #################################

def nomGraphe(G: graphe) -> str:
    """ Retourne le nom du graphe G:
    Exemple d'utilisation :

    >>> nom = nomgraphe(G)"""
    __verif_type_graphe(G)
    return G.label

def listeSommets(G: graphe) -> list:
    """ Retourne la liste des sommets du graphe G:
    Exemple d'utilisation :

    >>> l = listeSommets(G)"""
    __verif_type_graphe(G)
    return G.nodes

def listesommets(G: graphe) -> list:
    _errMaj("listesommets", "listeSommets")
def ListeSommets(G: graphe) -> list:
    _errMaj("ListeSommets", "listeSommets")
def listeSommet(G: graphe) -> list:
    _errS("listeSommet", "listeSommets")
def listesommet(G: graphe) -> list:
    _errS("listesommet", "listeSommets")

def nbSommets(G: graphe) -> int:
    """ Retourne le nombre de sommets du graphe G:
    Exemple d'utilisation :

    >>> n = nbSommets(G)"""
    __verif_type_graphe(G)
    return len(listeSommets(G))

def nbsommets(G: graphe) -> int:
    _errMaj("nbsommets", "nbSommets")
def NbSommets(G: graphe) -> int:
    _errMaj("NbSommets", "nbSommets")
def nbSommet(G: graphe) -> int:
    _errS("nbSommet", "nbSommets")
def nbsommet(G: graphe) -> int:
    _errS("nbsommet", "nbSommets")

def sommetNom(G: graphe, etiquette: str) -> sommet:
    """ Retourne le sommet de G désigné par son nom etiquette
    Exemple d'utilisation :

    >>> s = sommetNom(mongraphe, "Bordeaux")"""
    __verif_type_graphe(G)
    __verif_type_nomsommet(etiquette)
    for s in listeSommets(G):
        if s.label== etiquette:
            return s
    for s in listeSommets(G):
        if s.label.lower() == etiquette.lower():
            raise Exception("le graphe " + nomGraphe(G) + " ne possède pas de sommet d'étiquette '" + etiquette + "'."\
                             " En revanche il possède un sommet d'étiquette '" + s.label + "'. Remarquez la différence majuscule/minuscule.")
    raise Exception("le graphe " + nomGraphe(G) + " ne possède pas de sommet d'étiquette '" + etiquette + "'.")

def sommetnom(G: graphe, etiquette: str) -> sommet:
    _errMaj("sommetnom", "sommetNom")
def SommetNom(G: graphe, etiquette: str) -> sommet:
    _errMaj("SommetNom", "sommetNom")
def sommetsNom(G: graphe, etiquette: str) -> sommet:
    _errS("sommetsNom", "sommetNom")
def sommetsnom(G: graphe, etiquette: str) -> sommet:
    _errS("sommetsnom", "sommetNom")

def sommetNumero(G: graphe, i: int) -> sommet:
    __verif_type_graphe(G)
    return listeSommets(G)[i]

################# PRIMITIVES SOMMET   ###################################

def nomSommet(s: sommet) -> str:
    """ Retourne le nom (l'étiquette) du sommet s
    Exemple d'utilisation :

    >>> nom = nomSommet(s)"""
    __verif_type_sommet(s)
    return s.label

def marquerSommet(s: sommet) -> None:
    """ marque le sommet s
    Exemple d'utilisation :

    >>> marquerSommet(s)"""
    __verif_type_sommet(s)
    s.mark = True

def marquersommet(s: sommet) -> None:
    _errMaj("marquersommet", "marquerSommet")
def MarquerSommet(s: sommet) -> None:
    _errMaj("MarquerSommet", "marquerSommet")
def marquerSommets(s: sommet) -> None:
    _errS("marquerSommets", "marquerSommet")
def marquersommets(s: sommet) -> None:
    _errS("marquersommets", "marquerSommet")

def demarquerSommet(s: sommet) -> None:
    """ démarque le sommet s
    Exemple d'utilisation :

    >>> demarquerSommet(s)"""
    __verif_type_sommet(s)
    s.mark = False

def demarquersommet(s: sommet) -> None:
    _errMaj("demarquersommet", "demarquerSommet")
def DemarquerSommet(s: sommet) -> None:
    _errMaj("DemarquerSommet", "demarquerSommet")
def DeMarquerSommet(s: sommet) -> None:
    _errMaj("DeMarquerSommet", "demarquerSommet")
def demarquerSommets(s: sommet) -> None:
    _errS("demarquerSommets", "demarquerSommet")
def demarquersommets(s: sommet) -> None:
    _errS("demarquersommets", "demarquerSommet")

def estMarqueSommet(s: sommet) -> bool:
    """ retourne True si le sommet s est marqué, False sinon
    Exemple d'utilisation :

    >>> return estMarqueSommet(s):"""
    __verif_type_sommet(s)
    return s.mark

def estmarquesommet(s: sommet) -> bool:
    _errMaj("estmarquesommet", "estMarqueSommet")
def estmarqueSommet(s: sommet) -> bool:
    _errMaj("estmarqueSommet", "estMarqueSommet")
def estMarquesommet(s: sommet) -> bool:
    _errMaj("estMarquesommet", "estMarqueSommet")

def EstMarqueSommet(s: sommet) -> bool:
    _errMaj("EstMarqueSommet", "estMarqueSommet")
def Estmarquesommet(s: sommet) -> bool:
    _errMaj("Estmarquesommet", "estMarqueSommet")
def EstmarqueSommet(s: sommet) -> bool:
    _errMaj("EstmarqueSommet", "estMarqueSommet")
def EstMarquesommet(s: sommet) -> bool:
    _errMaj("EstMarquesommet", "estMarqueSommet")

def estmarquesommets(s: sommet) -> bool:
    _errS("estmarquesommets", "estMarqueSommet")
def estmarqueSommets(s: sommet) -> bool:
    _errS("estmarqueSommets", "estMarqueSommet")
def estMarquesommets(s: sommet) -> bool:
    _errS("estMarquesommets", "estMarqueSommet")

def EstMarqueSommets(s: sommet) -> bool:
    _errS("EstMarqueSommets", "estMarqueSommet")
def Estmarquesommets(s: sommet) -> bool:
    _errS("Estmarquesommets", "estMarqueSommet")
def EstmarqueSommets(s: sommet) -> bool:
    _errS("EstmarqueSommets", "estMarqueSommet")
def EstMarquesommets(s: sommet) -> bool:
    _errS("EstMarquesommets", "estMarqueSommet")

#def estMarquéSommet(s: sommet) -> bool:
#    _errAccent("estMarquéSommet", "estMarqueSommet")
#
#def estmarquésommet(s: sommet) -> bool:
#    _errMaj("estmarquésommet", "estMarqueSommet")
#def estmarquéSommet(s: sommet) -> bool:
#    _errMaj("estmarquéSommet", "estMarqueSommet")
#def estMarquésommet(s: sommet) -> bool:
#    _errMaj("estMarquésommet", "estMarqueSommet")
#
#def EstMarquéSommet(s: sommet) -> bool:
#    _errMaj("EstMarquéSommet", "estMarqueSommet")
#def Estmarquésommet(s: sommet) -> bool:
#    _errMaj("Estmarquésommet", "estMarqueSommet")
#def EstmarquéSommet(s: sommet) -> bool:
#    _errMaj("EstmarquéSommet", "estMarqueSommet")
#def EstMarquésommet(s: sommet) -> bool:
#    _errMaj("EstMarquésommet", "estMarqueSommet")
#
#def estmarquésommets(s: sommet) -> bool:
#    _errS("estmarquésommets", "estMarqueSommet")
#def estmarquéSommets(s: sommet) -> bool:
#    _errS("estmarquéSommets", "estMarqueSommet")
#def estMarquésommets(s: sommet) -> bool:
#    _errS("estMarquésommets", "estMarqueSommet")
#
#def EstMarquéSommets(s: sommet) -> bool:
#    _errS("EstMarquéSommets", "estMarqueSommet")
#def Estmarquésommets(s: sommet) -> bool:
#    _errS("Estmarquésommets", "estMarqueSommet")
#def EstmarquéSommets(s: sommet) -> bool:
#    _errS("EstmarquéSommets", "estMarqueSommet")
#def EstMarquésommets(s: sommet) -> bool:
#    _errS("EstMarquésommets", "estMarqueSommet")

def estmarquersommet(s: sommet) -> bool:
    _errOrtho("estmarquersommet", "estMarqueSommet")
def estmarquerSommet(s: sommet) -> bool:
    _errOrtho("estmarquerSommet", "estMarqueSommet")
def estMarquersommet(s: sommet) -> bool:
    _errOrtho("estMarquersommet", "estMarqueSommet")

def EstMarquerSommet(s: sommet) -> bool:
    _errOrtho("EstMarquerSommet", "estMarqueSommet")
def Estmarquersommet(s: sommet) -> bool:
    _errOrtho("Estmarquersommet", "estMarqueSommet")
def EstmarquerSommet(s: sommet) -> bool:
    _errOrtho("EstmarquerSommet", "estMarqueSommet")
def EstMarquersommet(s: sommet) -> bool:
    _errOrtho("EstMarquersommet", "estMarqueSommet")

def estmarquersommets(s: sommet) -> bool:
    _errOrtho("estmarquersommets", "estMarqueSommet")
def estmarquerSommets(s: sommet) -> bool:
    _errOrtho("estmarquerSommets", "estMarqueSommet")
def estMarquersommets(s: sommet) -> bool:
    _errOrtho("estMarquersommets", "estMarqueSommet")

def EstMarquerSommets(s: sommet) -> bool:
    _errOrtho("EstMarquerSommets", "estMarqueSommet")
def Estmarquersommets(s: sommet) -> bool:
    _errOrtho("Estmarquersommets", "estMarqueSommet")
def EstmarquerSommets(s: sommet) -> bool:
    _errOrtho("EstmarquerSommets", "estMarqueSommet")
def EstMarquersommets(s: sommet) -> bool:
    _errOrtho("EstMarquersommets", "estMarqueSommet")

def colorierSommet(s: sommet, c: str) -> None:
    """ colorie le sommet s avec la couleur c.
    Exemple d'utilisation :

    >>> colorierSommet(s, "red")"""
    __verif_type_sommet(s)
    __verif_type_couleur(c)
    s.color = c

def coloriersommet(s: sommet) -> None:
    _errMaj("coloriersommet", "colorierSommet")
def ColorierSommet(s: sommet) -> None:
    _errMaj("ColorierSommet", "colorierSommet")
def colorierSommets(s: sommet) -> None:
    _errS("colorierSommets", "colorierSommet")
def coloriersommets(s: sommet) -> None:
    _errS("coloriersommets", "colorierSommet")

def couleurSommet(s: sommet) -> str:
    """ retourne la couleur du sommet s
    Exemple d'utilisation :

    >>> c = couleurSommet(s)"""
    __verif_type_sommet(s)
    return s.color

def couleursommet(s: sommet) -> str:
    _errMaj("couleursommet", "couleurSommet")
def CouleurSommet(s: sommet) -> str:
    _errMaj("CouleurSommet", "couleurSommet")
def couleurSommets(s: sommet) -> str:
    _errS("couleurSommets", "couleurSommet")
def couleursommets(s: sommet) -> str:
    _errS("couleursommets", "couleurSommet")

def couleurssommet(s: sommet) -> str:
    _errS("couleurssommet", "couleurSommet")
def CouleursSommet(s: sommet) -> str:
    _errS("CouleursSommet", "couleurSommet")
def couleursSommets(s: sommet) -> str:
    _errS("couleursSommets", "couleurSommet")
def couleurssommets(s: sommet) -> str:
    _errS("couleurssommets", "couleurSommet")


##Dans cette version on ne colorie pas les aretes
##colorier = colorierSommet
##couleur = couleurSommet
    
# Ici les choses serieuses
def listeAretesIncidentes(s: sommet) -> list:
    """ retourne la liste des arêtes incidentes au sommet s
    Exemple d'utilisation :

    >>> l = listeAretesIncidentes(s)"""
    __verif_type_sommet(s)
    return s.edges

def areteNumero(s: sommet, i: int) -> arete:
    return listeAretesIncidentes(s)[i]

def degre(s: sommet) -> int:
    """ retourne le degré du sommet s
    Exemple d'utilisation :

    >>> d = degre(s)"""
    __verif_type_sommet(s)
    return len(listeAretesIncidentes(s)) 

def Degre(s: sommet) -> int:
    _errMaj("Degre", "degre")
def degres(s: sommet) -> int:
    _errS("degres", "degre")
def Degres(s: sommet) -> int:
    _errS("Degres", "degre")
#def degré(s: sommet) -> int:
#    _errAccents("degré", "degre")
#def Degré(s: sommet) -> int:
#    _errAccents("Degré", "degre")
#def degrés(s: sommet) -> int:
#    _errAccents("degrés", "degre")
#def Degrés(s: sommet) -> int:
#    _errAccents("Degrés", "degre")

def listeVoisins(s: sommet) -> list:
    """ retourne la liste des voisins du sommet s
    Exemple d'utilisation :

    >>> l = listeVoisins(s)"""
    __verif_type_sommet(s)
    inc = listeAretesIncidentes(s)
    v = []
    for a in inc:
        if a.start == s:
            v.append (a.end)
        elif a.end == s:
            v.append (a.start)
    return v

def listevoisins(s: sommet) -> list:
    _errMaj("listevoisins", "listeVoisins")
def ListeVoisins(s: sommet) -> list:
    _errMaj("ListeVoisins", "listeVoisins")
def listeVoisin(s: sommet) -> list:
    _errS("listeVoisin", "listeVoisins")
def listevoisin(s: sommet) -> list:
    _errS("listevoisin", "listeVoisins")

def voisinNumero(s: sommet, i: int) -> sommet:
    return listeVoisins(s)[i]

def sommetVoisin(s: sommet, a: arete) -> sommet:
    """ retourne le sommet voisin du sommet s en suivant l'arêt a
    Exemple d'utilisation :

    >>> t = sommetvoisin(s,a)"""
    __verif_type_sommet(s)
    __verif_type_arete(a)
    if a.start == s:
        return a.end
    if a.end == s:
        return a.start
    raise Exception("\n\nle sommet '" + nomSommet(s) + "' n'est pas une extremite de l'arete ('" + nomSommet(a.start) +"', '"+ nomSommet(a.end) + "').")

################ PRIMITIVES arete ########################

def nomArete(a: arete) -> str:
    """ retourne le nom de l'arête a
    Exemple d'utilisation :

    >>> nom = nomArete(a)"""
    __verif_type_arete(a)
    return a.label

def marquerArete(a: arete) -> None:
    """ marque l'arête a
    Exemple d'utilisation :

    >>> marquerArete(a)"""
    __verif_type_arete(a)
    a.mark = True

def demarquerArete(a: arete) -> None:
    """ démarque l'arête a
    Exemple d'utilisation :

    >>> demarquerArete(a)"""
    __verif_type_arete(a)
    a.mark = False

def estMarqueeArete(a: arete) -> bool:
    """ retourne True si l'arête a est marquée, False sinon
    Exemple d'utilisation :

    >>> return estMarqueeArete(a)"""
    __verif_type_arete(a)
    return a.mark

def numeroterArete(a: arete, n: int) -> None:
    __verif_type_arete(a)
    a.label = str(n)

################ Verifications de types ########################

def __verif_type_graphe(G):
    if G.__class__.__name__ != '__c_graph':
        if isinstance(G, str):
            raise TypeError("'" + G + "' est une chaine de caracteres alors que la fonction attend un graphe. Peut-etre voulez-vous utiliser la fonction ouvrirGraphe(G)?")
        if isinstance(G, _io.TextIOWrapper):
            raise TypeError("'" + str(G) + "' est un fichier ouvert alors que la fonction attend un graphe. Peut-etre voulez-vous utiliser la fonction ouvrirGraphe(G)?")
        raise __ErreurParametre(G, "un graphe")
    
def __verif_type_sommet(s):
    if s.__class__.__name__ != '__c_node':
        if isinstance(s, str):
            raise TypeError("'" + s + "' est une chaine de caracteres alors que la fonction attend un sommet. Peut-etre voulez-vous utiliser la fonction sommetNom(G, etiquette)?")
        raise __ErreurParametre(s, "un sommet")

def __verif_type_arete(a):
    if a.__class__.__name__ != '__c_edge':
        raise __ErreurParametre(a, "une arete")

def __verif_type_nomfichier(s):
    if not isinstance(s, str):
        raise __ErreurParametre(s, 'un nom de fichier, par exemple "tgv2005.dot"')

def __verif_type_nomsommet(s):
    if not isinstance(s, str):
        raise __ErreurParametre(s, 'un nom de sommet, par exemple "Paris"')

def __verif_type_couleur(s):
    if not isinstance(s, str):
        raise __ErreurParametre(s, 'une chaine de caracteres représentant une couleur comme par exemple : "red", "green", "blue", "white", "cyan" ou "yellow".')


class __ErreurParametre (TypeError):
    def __init__(self, arg, param):
        super().__init__(arg)
        self.arg = arg
        self.param = param
    def __str__(self):
        # affichage discutable
        if isinstance (self.arg, str):
            strArg = "'" + self.arg + "'"
        else:
            strArg = str (self.arg)
        return "\n\n" + strArg + " n'est pas " + self.param

############### Construction de graphes  #####################
    
def _add_edge (G, label, i, j):
    a = __c_edge(label, G.nodes[i], G.nodes[j])
    G.nodes[i].edges.append(a)
    G.nodes[j].edges.append(a)
    return a

# retourne le numero du sommet
def _find_add_node (G, nom):
    i = 0
    for s in G.nodes:
        if s.label == nom:
            return i
        i = i + 1
    G.nodes.append (__c_node (nom))
    return i

# Un chemin p est une liste de noms de sommets ['A', 'B', 'C', ...]
# Le parametre booleen 'chemins' indique si les aretes sont:
#   A-B, B-C, etc. (chemin classique)
#   A-B, A-C, etc. (etoile: le sommet initial est suivi de ses voisins)
# B, C, etc. peuvent aussi etre des couples [nom de sommet, nom d'arete]
# lorsqu'on veut etiqueter explicitement les aretes
# (etiquetees par defaut 'e0', 'e1', etc. dans l'ordre de leur creation)

# Attention: l'etiquette d'un graphe (label) sert aussi de nom de fichier
# pour les dessins, eviter les blancs, etc

def construireGraphe (paths, label, chemins = True) -> graphe:
    G = __c_graph(label)
    
    # Numeroter les aretes a partir de 0 ou 1 en l'absence
    # d'etiquette explicite?
    # On choisit 1 car les dessins du poly adoptent cette convention
    # mais ce choix est incoherent avec celui pour les sommets:
    # la fonction sommetNumero impose que les sommets des graphes
    # generiques (grilles, etc) soient etiquetes 's0', 's1', etc.
    
    nba = 1
    for p in paths:
        labelsource = p[0]
        i = _find_add_node (G, labelsource)
        
        # ne pas utiliser 'for a in p' car il faut maintenant ignorer p[0]  
        for k in range (1, len(p)):
            a = p[k]
            edge_with_label = isinstance(a, list)
            if edge_with_label:
                labeldestination = a[0]
                labeledge = a[1]
            else:
                labeldestination = a
                labeledge = 'e' + str(nba)
                nba = nba + 1
            j = _find_add_node(G, labeldestination)
            _add_edge(G, labeledge, i, j)
            if chemins:
                i = j
    return G

############### Dessin du graphe  #####################

# fonction necessaire a cause par exemple des 'Pays Bas' (blanc dans label)
def _proteger (label):
    return '"' + label + '"'

# La fonction '__dotify' transforme le graphe en un fichier texte
# qui servira de source (suffixe .dot) pour les programmes de Graphviz.
# Cette fonction ne depend pas du systeme d'exploitation.

def __dotify (G, etiquettesAretes = True, colormark = 'Black', suffixe = 'dot', path = None):
    if __plateforme != 'Windows':
        (soft,maximum) = resource.getrlimit(resource.RLIMIT_NOFILE)
        if soft == 0:
            resource.setrlimit(resource.RLIMIT_NOFILE, (maximum,maximum))

    # graphe non oriente, il faut eviter de traiter chaque arete deux fois
    for s in G.nodes:
        for a in s.edges:
            a.ecrite = False

    if G.label == '':
        nom_graphe = 'G'
    else:
        nom_graphe = G.label

    if path:
        graph_dot = path
    else:
        graph_dot = 'tmp/' + nom_graphe + '-' + str(__dotify.num) + '.' + suffixe
        __dotify.num = __dotify.num + 1

    try:
        f = open (graph_dot, 'w')
    except IOError:
        os.mkdir ('tmp')
        f = open (graph_dot, 'w')
        
    f.write ('graph "' + nom_graphe + '" {\n' + G.drawopts + '\n')

    for s in G.nodes:
        d = len (s.edges)
        snom = _proteger (s.label)
        for a in s.edges:
            if not a.ecrite:
                a.ecrite = True
                if a.start == s:
                    t = a.end
                else:
                    t = a.start
                f.write ('  ' + snom + ' -- ' + _proteger (t.label))
                if etiquettesAretes:
                    f.write (' [label = ' + _proteger (a.label) + ']')
                if a.mark:
                    f.write (' [style = bold, color = orange]')
                # Semicolons aid readability but are not required (dotguide.pdf)
                f.write (a.drawopts + ';\n')
        bord = 'black'
        if s.mark:
            entoure = 2
            bord = colormark
        else:
            entoure = 1
        if s.color:
            if s.color[0:4] == "dark" or s.color in [ "black", "blue", "blue1", "blue2", "blue3", "blue4", "mediumblue", "blueviolet", "indigo", "navy", "navyblue", "purple4", "brown4", "gray", "grey" ]:
                fontcolor = "white"
            else:
                fontcolor = "black"
            f.write ('  %s %s [style = filled, peripheries = %s, fillcolor = %s, fontcolor = %s, color = %s];\n' %
                     (snom, s.drawopts, entoure, s.color, fontcolor, bord))
        elif s.mark:
            # f.write ('  ' + snom + ' [peripheries = 2, color = ' + bord + ']' +
            #          s.drawopts + ';\n');
            f.write ('  %s %s [peripheries = 2, color = %s];\n' %
                     (snom, s.drawopts, bord))
        elif d == 0 or s.drawopts:
            f.write ('  ' + snom + s.drawopts + ';\n')
            
    f.write ('}\n')
    f.close ()
    if __plateforme != 'Windows':
        if soft == 0:
            resource.setrlimit(resource.RLIMIT_NOFILE, (0,maximum))
    return graph_dot


__dotify.num = 0

# La fonction 'Graphviz' lance l'execution d'un programme
# de la distribution Graphviz (dot, neato, twopi, circo, fdp)
# pour transformer un fichier texte source de nom 'racine.suffixe'
# en une image de nom 'racine.format' (peut-etre un fichier PostScript)

def __Graphviz (source, algo = 'dot', fileFormat = 'svg', suffixe = 'dot'):
    if __plateforme != 'Windows':
        (soft,maximum) = resource.getrlimit(resource.RLIMIT_NOFILE)
        if soft == 0:
            resource.setrlimit(resource.RLIMIT_NOFILE, (maximum,maximum))
    image = source.replace ('.' + suffixe, '.' + fileFormat)
    algo = __pathGraphviz + algo
    if __plateforme == 'Windows':
        algo = algo + '.exe'
    subprocess.call ([algo, '-T' + fileFormat, source, '-o', image])
    if __plateforme != 'Windows':
        if soft == 0:
            resource.setrlimit(resource.RLIMIT_NOFILE, (0,maximum))
    return image


# Enchaine dotify et Graphviz avec des arguments standard adaptes au systeme
# et lance le programme ad hoc pour afficher l'image

def dessinerGraphe (G: graphe, etiquettesAretes = False, algo = 'dot', colormark = 'Black') -> None:
    """ dessine le graphe G
    Exemple d'utilisation :

    >>> dessinerGraphe(G)"""
    __verif_type_graphe (G)
    if nbSommets(G) > 100:
        print("Attention, le graphe a "+str(nbSommets(G))+" sommets, le dessin va prendre du temps...")
    if __pathGraphviz == "":
        dessinerGraphe2(G, etiquettesAretes, algo, colormark)
        return
    if __plateforme == 'Windows':
        # eviter toute embrouille avec les modeles de document de MS Word
        graph_dot = __dotify (G, etiquettesAretes, colormark, 'txt')
        image = __Graphviz (graph_dot, algo, suffixe = 'txt')
        image = image.replace ('/', '\\')
        os.startfile (image)
        return

    graph_dot = __dotify (G, etiquettesAretes, colormark)
    image = __Graphviz (graph_dot, algo)
    if nbSommets(G) > 100:
        print("Le dessin est enfin fini.")
    if _is_notebook:
        IPython.display.display(IPython.display.SVG(filename=image))
    elif __plateforme == 'Linux':
        #subprocess.call (['firefox', image])
        subprocess.Popen (['firefox ' + image + ' &'], shell=True)
    elif __plateforme == 'Darwin':
        subprocess.call (['open', '-a', 'Safari', image])
    else:
        print("Systeme " + __plateforme + " imprevu, abandon du dessin")
        

import webbrowser
import urllib.parse
def dessinerGraphe2(G: graphe, etiquettesAretes = False, algo = 'dot', colormark = 'Black') -> None:
        graph_dot = __dotify (G, etiquettesAretes, colormark)
        with open (graph_dot, "r") as myfile:
            data=myfile.readlines()
        my_str = ''
        for line in data:
            my_str += line
        parametre = urllib.parse.quote(my_str)
        webbrowser.open("https://dreampuf.github.io/GraphvizOnline/#" + parametre)


afficherGraphe = dessinerGraphe
dessiner = dessinerGraphe

# Cela pourrait être mieux écrit avec des règles standards de lexing/parsing, mais cela évite des dépendances

def _charclass (c):
    if ('a' <= c <= 'z') or ('A' <= c <= 'Z') or \
     ('0' <= c <= '9') or c in  ('_', '.'):
        return 'a'
    if c in ('-', '>'):
        return '-'
    return c

# Lexing. On commence à regarder à la position i
# Retourne le mot et la position à laquelle on est arrivé
def _mot (s, debut):
    while debut < len(s) and (s[debut] == ' ' or s[debut] == '\t' or s[debut] == '\n' or s[debut] == '\r'):
        debut+=1

    if debut >= len(s):
        return "",debut

    if s[debut:debut+2] == '/*':
        fin = debut + 2
        while s[fin:fin+2] != '*/':
            fin+=1
        return _mot(s, fin+2)

    fin = debut
    if s[debut] == '"':
        fin+=1
        echappe = False
        while fin < len(s):
            if echappe:
                echappe = False
            else:
                if s[fin] == '"':
                    #print(s[debut:fin+1],fin+1)
                    return s[debut:fin+1],fin+1
                if s[fin] == '\\':
                    echappe = True
            fin+=1
        raise SyntaxError("Fichier incorrect: \" not terminé à la fin du fichier")

    charclass = _charclass(s[fin])
    while fin < len(s) and (s[fin] != ' ' and s[fin] != '\t' and s[fin] != '\n' and s[fin] != '\r'):
        if s[fin] == '#':
            # Commentaire, ignore jusqu'à la fin de ligne
            fin2 = fin
            while fin2 < len(s) and (s[fin2] != '\n' and s[fin2] != '\r'):
                fin2+=1
            if debut == fin:
                # Pas de mot avant le commentaire, on recommence à lire à la ligne suivante
                return _mot(s, fin2)
            return s[debut:fin],fin2

        if _charclass(s[fin]) != charclass:
            # On change de class de caractère, cela découpe le mot
            #print(s[debut:fin],fin)
            return s[debut:fin],fin

        if s[fin] == '"':
            raise SyntaxError("Fichier incorrect: \" au milieu d'un mot à "+str(debut))
        fin+=1
    #print(s[debut:fin],fin+1)
    return s[debut:fin],fin+1

def _mot_int(s, i):
    mot,i = _mot(s, i)
    return int(mot), i

# Parsing

# Lit le contenu d'attributs. Le [ initial a déjà été consommé. On commence à regarder à la position i
# Retourne un dictionnaire des attributs et la position à laquelle on est arrivé
def _attributs(s,i):
    nom,i = _mot(s,i)
    attributs = {}
    while nom != ']':
        if nom == "":
            raise SyntaxError("Fichier incorrect: pas de crochet fermant à "+str(i))
        if nom == ",":
            nom,i = _mot(s,i)
        egal,i = _mot(s,i)
        if egal != '=':
            raise SyntaxError("Fichier incorrect: trouvé "+egal+" au lieu d'un '=' à "+str(i))
        val,i = _mot(s,i)
        #print("attribut "+nom+" défini à "+val+" .")
        attributs[nom] = val
        nom,i = _mot(s,i)
        if nom == ']':
            nom2,j = _mot(s,i)
            if nom2 == '[':
                # Fermer la porte, pour la rouvrir aussitôt...
                nom,i = _mot(s,j)
    return attributs,i

def _drawopts(attributs):
    drawopts = "["
    for x in attributs:
        v = x + "=" + attributs[x]
        if drawopts == "[":
            drawopts += v
        else:
            drawopts += ", " + v
    drawopts += "]"
    return drawopts

# Lit une définion de graphe, en commançant par son nom à la position i
# Retourne une liste de chemins et la nouvelle position
def _litgrapheDOT(s,i):
    chemins = []
    couleurs = []
    marks = []
    nodeattr = []
    edgeattr = []
    defattr = []
    nom,i = _mot(s,i)
    if nom[0] == '"':
        nom = nom[1:-1]
    accolade,i = _mot(s,i)
    if accolade != "{":
        raise SyntaxError("Fichier incorrect: trouvé "+accolade+" au lieu d'une accolade ouvrante à "+str(i))

    mot,i = _mot(s,i)
    while mot != "}":
        #print("starting new read with "+mot+" "+str(i))
        if mot == "":
            raise SyntaxError("Fichier incorrect: pas d'accolade fermante terminale à la fin du fichier")

        if mot in ("graph", "node", "edge"):
            # attributs par défaut
            crochet,j = _mot(s,i)
            if crochet != '[':
                raise SyntaxError("Fichier incorrect: trouvé "+crochet+" au lieu d'un crochet ouvrant à "+str(i)+' '+str(j))
            i = j
            attr,i = _attributs(s,i)
            defattr += [ mot + _drawopts(attr) ]
            mot,i = _mot(s,i)

        elif mot in ("start", "rankdir", "ratio"):
            # attribut d'un graphe
            equal,j = _mot(s,i)
            if equal != '=':
                raise SyntaxError("Fichier inccorect: pour "+mot+", trouvé "+equal+" au lieu d'un = à "+str(i))
            i = j
            val,i = _mot(s,i)
            defattr += [ mot + '=' + val ]
            mot,i = _mot(s,i)
        elif mot == "subgraph":
            # récursion!
            # idéalement il faudrait séparer les espaces de noms de sommets
            _,chemins_sousgraphe,couleurs_sousgraphe,marks_sousgraphe,nodeattr_sousgraphe,edgeattr_sousgraphe,defattr_sousgraphe,i = _litgrapheDOT(s,i)
            couleurs = couleurs_sousgraphe + couleurs
            marks = marks_sousgraphe + marks
            chemins = chemins_sousgraphe + chemins
            nodeattr = nodeattr_sousgraphe + nodeattr
            edgeattr = edgeattr_sousgraphe + edgeattr
            defattr = defattr_sousgraphe + defattr
            mot,i = _mot(s,i)
        else:
            # Nom d'un sommet
            if mot[0] == '"':
                mot = mot[1:-1]
            mot2,i = _mot(s,i)
            chemins += [[mot]]
            if mot2 == '[':
                # attributs d'un nœud
                attr,i = _attributs(s,i)
                if "fillcolor" in attr:
                    c = attr.pop("fillcolor")
                    couleurs += [(mot, c)]
                if "peripheries" in attr:
                    c = attr.pop("peripheries")
                    if c == "2":
                        marks += [mot]
                nodeattr += [ ( mot, _drawopts(attr) ) ]
                mot,i = _mot(s,i)
            elif mot2 in ('--', '->'):
                # Un chemin
                chemin = [mot]
                mot = mot2
                while mot in ('--', '->'):
                    mot,i = _mot(s,i)
                    if mot[0] == '"':
                        mot = mot[1:-1]
                    chemin = [mot] + chemin
                    mot,i = _mot(s,i)
                chemins += [chemin]
                if mot == '[':
                    # attributs d'un chemin
                    attr,i = _attributs(s,i)
                    attrs = _drawopts(attr)
                    last = chemin[0]
                    for x in chemin[1:]:
                        edgeattr += [ (last, x, attrs) ]
                        last = x
                    mot,i = _mot(s,i)
            elif mot2 == '=':
                # attribut par défaut
                mot3,i = _mot(s,i)
                if mot != 'fillcolor':
                    defattr += [ mot + '=' + mot3 ]
                mot,i = _mot(s,i)
            elif mot2 == ';':
                # Rien d'intéressant, en fait
                mot = mot2
            else:
                raise SyntaxError("Fichier non supporté: trouvé "+mot2+" à "+str(i))
        while mot == ';':
            mot,i = _mot(s,i)
    return nom,chemins,couleurs,marks,nodeattr,edgeattr,defattr,i

def _litgrapheGML(s,i):
    chemins = []
    couleurs = []
    noms = {}
    graph,i = _mot(s,i)
    if graph != "graph":
        raise SyntaxError('Attendu "graph", trouvé '+graph+' à la place')
    mot,i = _mot(s,i)
    if mot != '[':
        raise SyntaxError('Attendu "[", trouvé '+mot+' à la place')
    mot,i = _mot(s,i)
    while mot != ']':
        if mot == "directed":
            _,i = _mot(s,i) #oriente,i
            mot,i = _mot(s,i)
        elif mot == "node":
            # un sommet
            mot,i = _mot(s,i)
            if mot != '[':
                raise SyntaxError('Attendu "[", trouvé '+mot+' à la place')
            mot,i = _mot(s,i)
            ID = -1
            nom = ""
            while mot != ']':
                if mot == 'id':
                    ID,i = _mot(s,i)
                    mot,i = _mot(s,i)
                elif mot == 'label':
                    nom,i = _mot(s,i)
                    if nom[0] == '"':
                        nom = nom[1:-1]
                    mot,i = _mot(s,i)
                elif mot in ('value', 'source'):
                    # ignore
                    _,i = _mot(s,i)
                    mot,i = _mot(s,i)
                else:
                    raise SyntaxError('mot-clé de sommet '+mot+' non supporté à '+str(i))
            if nom == "":
                nom = str(ID)
            #print("sommet "+nom)
            noms[ID] = nom
            chemins += [[nom]]
            mot,i = _mot(s,i)
        elif mot == "edge":
            # une arête
            mot,i = _mot(s,i)
            if mot != '[':
                raise SyntaxError('Attendu "[", trouvé '+mot+' à la place')
            mot,i = _mot(s,i)
            src = ''
            dst = ''
            while mot != ']':
                if mot == 'source':
                    src,i = _mot(s,i)
                    mot,i = _mot(s,i)
                elif mot == 'target':
                    dst,i = _mot(s,i)
                    mot,i = _mot(s,i)
                elif mot == 'value':
                    _,i = _mot(s,i) #value,i
                    mot,i = _mot(s,i)
                else:
                    raise SyntaxError('mot-clé de sommet '+mot+' non supporté à '+str(i))
            if src == '':
                raise SyntaxError("source de l'arête manquante")
            if dst == '':
                raise SyntaxError("destination de l'arête manquante")
            #print("arête "+noms[src]+"-"+noms[dst])
            chemins += [[noms[src],noms[dst]]]
            mot,i = _mot(s,i)
        else:
            raise SyntaxError('mot-clé '+mot+' non supporté à '+str(i))

    return "graphe",chemins,couleurs,i

def _litgraphePAJ(s,i):
    chemins = []
    couleurs = []
    noms = {}

    mot,i = _mot(s,i)
    if mot != "Vertices":
        raise SyntaxError('Attendu Vertices, trouvé '+mot+' à la place')

    _,i = _mot(s,i) # nbvert,i

    mot,i = _mot(s,i)
    while mot != "*":
        # un sommet
        ID = mot
        nom,i = _mot(s,i)
        if nom[0] == '"':
            nom = nom[1:-1]
        noms[ID] = nom
        chemins += [[nom]]
        #print("sommet "+nom)
        mot,i = _mot(s,i)

    mot,i = _mot(s,i)
    if mot in ("Edges", "Arcs"):
        raise SyntaxError('Attendu Edges ou Arcs, trouvé '+mot+' à la place')

    mot,i = _mot(s,i)
    while mot != "":
        # une arête
        src = mot
        dst,i = _mot(s,i)
        chemins += [[noms[src],noms[dst]]]
        #print("arête "+noms[src]+"-"+noms[dst])
        mot,i = _mot(s,i)

    return "graphe",chemins,couleurs,i

def _litgrapheGRF(s,i):
    chemins = []
    couleurs = []
    noms = {}

    nbvert,i = _mot_int(s,i)
    _,i = _mot_int(s,i) # nbedge,i

    # 0 ou 1
    _,i = _mot_int(s,i) #base,i
    options,i = _mot_int(s,i)
    # vertwei = options % 10 != 0
    options /= 10
    # edgewei = options % 10 != 0
    options /= 10
    labels = options % 10 != 0

    for line in range(nbvert):
        if labels:
            nom,i = _mot(s,i)
        else:
            nom = str(line)
        noms[nom] = nom
        deg,i = _mot_int(s,i)
        for _ in range(deg):
            neigh,i = _mot(s,i)
            chemins += [[nom,neigh]]

    return "graphe",chemins,couleurs,i

# Parsing
def ouvrirGraphe(nom: str) -> graphe:
    """ ouvre le fichier nom et retourne le graphe contenu dedans
    Exemple d'utilisation :

    >>> g = ouvrirGraphe("fichier.dot")"""
    __verif_type_nomfichier(nom)
    try:
        f = open(nom)
    except FileNotFoundError as e:
        raise Exception("Attention, le fichier " + nom + " n'existe pas, peut-être le nom est mal écrit, ou bien ce fichier n'est pas dans le même répertoire que le fichier .py ?")
    s = f.read()
    i = 0

    graph,i = _mot(s,i)
    if graph == "Creator":
        # .gml format
        _,i = _mot(s,i) # creator,i
        nom,chemins,couleurs,i = _litgrapheGML(s,i)
        marks = []
        nodeattr = []
        edgeattr = []
        defattr = []
    elif graph == "*":
        # .paj format
        nom,chemins,couleurs,i = _litgraphePAJ(s,i)
        marks = []
        nodeattr = []
        edgeattr = []
        defattr = []
    elif graph == "0":
        # .grf format
        nom,chemins,couleurs,i = _litgrapheGRF(s,i)
        marks = []
        nodeattr = []
        edgeattr = []
        defattr = []
    else:
        if graph == "strict":
            graph,i = _mot(s,i)
        if graph not in ("digraph", "graph") :
            raise SyntaxError("Fichier graphe de type "+graph+" non supporté")

        nom,chemins,couleurs,marks,nodeattr,edgeattr,defattr,i = _litgrapheDOT(s,i)
    #print("construction")
    g = construireGraphe(chemins, nom)
    #print("coloration")
    for (s,c) in couleurs:
        colorierSommet(sommetNom(g,s),c)
    for s in marks:
        marquerSommet(sommetNom(g,s))
    for (s,attrs) in nodeattr:
        sommetNom(g,s).drawopts += attrs
    for (n1,n2,attrs) in edgeattr:
        s1 = sommetNom(g,n1)
        for a in listeAretesIncidentes(s1):
            s2 = sommetVoisin(s1,a)
            if nomSommet(s2) == n2:
                a.drawopts += " " + attrs
    for attrs in defattr:
        g.drawopts += attrs + ";\n"
    #print("fini")
    return g

def ouvrirgraphe(nom: str) -> graphe:
    _errMaj("ouvrirgraphe", "ouvrirGraphe")
def OuvrirGraphe(nom: str) -> graphe:
    _errMaj("OuvrirGraphe", "ouvrirGraphe")
def ouvrirGraphes(nom: str) -> graphe:
    _errS("ouvrirGraphes", "ouvrirGraphe")
def OuvrirGraphes(nom: str) -> graphe:
    _errS("OuvrirGraphes", "ouvrirGraphe")

def ecrireGraphe(G: graphe, nom: str) -> None:
    """ sauvegarde le graphe G dans le fichier nom
    Exemple d'utilisation :

    >>> ecrireGraphe(G, "fichier.dot")"""
    __dotify(G, path = nom)

# fig32 = construireGraphe (
#     [ ['A', 'B', 'A', 'C', 'D'],
#       ['B', 'B'], # boucle
#       ['D', 'D', 'D'] # boucles
#     ], "fig32")

# Construction ad hoc pour indiquer a Graphviz (algo 'neato')
# les longueurs des aretes
def _makePetersen ():
    g = construireGraphe (
        [ ['A', 'B', 'C', 'D', 'E', 'A'],
          ['a', 'c', 'e', 'b', 'd', 'a'],
          ['A', 'a'],
          ['B', 'b'],
          ['C', 'c'],
          ['D', 'd'],
          ['E', 'e']
        ], "Petersen")
    # Semicolons aid readability but are not required (dotguide.pdf)
    # start = germe du generateur aleatoire pour le placement initial des sommets
    # valeurs OK au CREMI [0, 12, 16, 18, 23, 24, 30, 33]
    # start = 4 interessant aussi
    if __plateforme == 'Windows':
        g.drawopts = 'edge [len = 2]'
    else:
        g.drawopts = 'start = 23; edge [len = 2]'
    for i in range (5):
        s = sommetNumero (g, i)
        a = areteNumero (s, 2)
        a.drawopts = '[len = 1]'
    return g

#Petersen = _makePetersen ()

# Koenigsberg = construireGraphe (
#     [ ['A', 'B', 'C', 'D', 'B', 'A', 'D'],
#       ['B', 'C']
#     ], "Koenigsberg")
# Koenigsberg.drawopts = 'rankdir=LR'





# Construction en etoile: Paris, Nantes, Lyon, etc. sont les voisins de Lille
# -> dernier parametre = False
# Les etiquettes des aretes ne servent a rien mais ne mangent pas de pain
# tgv2005 = construireGraphe (
#     [["Lille",
#       ["Paris", "1h00"], ["Nantes", "4h10"], ["Lyon", "2h50"],
#       ["Bordeaux", "5h00"], ["Toulouse", "8h20"],
#       ["Marseille", "4h30"], ["Montpellier", "4h40"]],
#      ["Paris",
#       ["Nantes", "2h00"], ["Lyon", "1h55"], ["Bordeaux", "2h55"],
#       ["Marseille", "2h56"], ["Montpellier", "3h15"],
#       ["Toulouse", "5h14"]],
#      ["Nantes", ["Lyon", "4h20"], ["Marseille", "6h20"]],
#      ["Lyon",
#       ["Toulouse", "4h30"], ["Marseille", "1h20"],
#       ["Montpellier", "1h45"]],
#      ["Bordeaux", ["Toulouse", "2h10"]],
#      ["Toulouse", ["Montpellier", "2h16"]],
#      ["Strasbourg"]
#     ], "tgv2005", chemins = False)


# hypercubeDim3 = construireGraphe (
#     [['v0', 'v1', 'v3', 'v2', 'v0', 'v4', 'v5', 'v6', 'v7', 'v4'], 
#     ['v1', 'v5'],
#     ['v3', 'v6'],
#     ['v2', 'v7']], "hypercubeDim3")


# hypercubeDim3 = construireGraphe ([
#  ["v0", "v1"]
#  ["v0", "v2"]
#  ["v0", "v4"]
#  ["v1", "v5"]
#  ["v1", "v3"]
#  ["v2", "v3"]
#  ["v2", "v7"]
#  ["v3", "v6"]
#  ["v6", "v5"]
#  ["v5", "v4"]
#  ["v4", "v7"]
#  ["v7", "v6"]],
# "hypercubeDim3", chemins = False)



# Construction en etoile: Espagne, Belgique, etc. sont les voisins de France
# -> dernier parametre = False
# Attention: Graphviz ne supporte pas les lettres accentuees !
# Les numeros des couches font reference a l'algorithme 'dot'
# Europe = construireGraphe ( [
#     ["Portugal","Espagne"],     # couches 0 et 1
#     ["France", "Espagne"],      # couche 2
#     ["Belgique", "France"],     # couche 3
#     ["Pays Bas", "Belgique"],   # couche 4
#     ["Allemagne", "France", "Belgique", "Pays Bas"],    # couche 5
#     ["Danemark", "Allemagne"],  # couche 6
#     ["Pologne", "Allemagne"],   # couche 6
#     ["Italie", "France"],       # couche 3
#     ["Autriche", "Allemagne", "Italie"],    #couche 6
#     ["Tchequie", "Pologne", "Allemagne", "Autriche"],   # couche 7
#     # ce qui suit est la verite, mais 'dot' fait alors plonger
#     # le Danemark au milieu du graphe, too bad
#     ["Slovaquie", "Tchequie", "Autriche", "Pologne"],   # couche 8
#     ["Hongrie", "Autriche", "Slovaquie"],   # couche 9
#     ["Ukraine", "Pologne", "Slovaquie", "Hongrie"], # couche 10
#     ["Roumanie", "Hongrie", "Ukraine"],     # couche 11
#     ["Angleterre", "Pays de Galles", "Ecosse"],
#     ["Irlande"],
#     ["Finlande", "Suede", "Norvege"],
#     ["Suede", "Norvege"] ], "Europe", chemins = False)

# Europe.drawopts = 'rankdir=LR ratio=.5 node[shape=box style=rounded]'

# listeGraphes = [tgv2005, fig32, Europe, Koenigsberg, Petersen, hypercubeDim3]

############# A partir d'ici graphes graphes parametres ###########
#############   construits sur des modeles reguliers    ###########

# Exemple: __prefixer ([0, 1, 2, ...], 's') = ['s0', 's1', 's2', ...]
# Fonctionne aussi bien pour les listes de listes

# Attention: le premier sommet doit etre 's0'
# a cause de la fonction sommetNumero

def __prefixer (paths, prefix):
    e = []
    for p in paths:
        if isinstance (p, list):
            e.append (__prefixer (p, prefix))
        else:
            e.append (prefix + str (p))
    return e

# Graphes complets

def _complet (n):
    a = []
    for i in range (1, n):
        a.append (list (range (i, -1, -1)))
    return a

def construireComplet (n: int) -> graphe:
    """ retourne le graphe complet K_n
    Exemple d'utilisation :

    >>> g = construireComplet(5)"""
    g = __prefixer (_complet (n), 's')
    # le 'nom' d'un graphe (label) sert aussi de nom de fichier
    # pour les dessins, eviter les blancs, etc
    nom = 'K' + str (n)
    g = construireGraphe (g, nom, chemins = False)
    # pour l'algo 'neato' (mais le bon algo ici est 'circo')
    g.drawopts = 'edge [len = 2]'
    return g

# Graphes bipartis complets
def _biclique (m, n):
    a = []
    for i in range (m):
        a.append ([i] + list(range (m, m + n)))
    return a

def construireBipartiComplet (m: int, n: int) -> graphe:
    """ retourne le graphe K_m,n
    Exemple d'utilisation :

    >>> g = construireBipartiComplet(2, 5)"""
    g = __prefixer (_biclique (m, n), 's')
    # le 'nom' d'un graphe (label) sert aussi de nom de fichier
    # pour les dessins, eviter les blancs, etc
    nom = 'K' + str (m) + 'x' + str(n)
    g = construireGraphe (g, nom, chemins = False)
    # pour l'algo 'neato'
    g.drawopts = 'edge [len = 2]'
    return g

# Grilles

def _grille (m, n):
    lignes = []
    debut = 0
    for _ in range (m):
        fin = debut + n
        lignes.append (list(range (debut, fin)))
        debut = fin
    for j in range (n):
        lignes.append (list(range (j, fin, n)))
    return lignes

def construireGrille (m: int, n: int) -> graphe:
    """ retourne la grille rectangulaire d'ordre n
    Exemple d'utilisation :

    >>> g = construireGrille(4)"""
    g = __prefixer (_grille (m, n), 's')
    # le 'nom' d'un graphe (label) sert aussi de nom de fichier
    # pour les dessins, eviter les blancs, etc
    nom = 'grille' + str (m) + 'x' + str(n)
    g = construireGraphe (g, nom)
    return g

# Triangles

def _triangle (n):
    lignes = []
    debut = 0
    for i in range (n):
        fin = debut + i + 1
        u = list (range (debut, fin))
        lignes.append (u)
        debut = fin
    debut = -1
    for i in range (n - 1):
        u = []
        debut = debut + i + 1
        k = debut
        for j in range (i, n):
            u.append (k)
            k = k + j + 1
        lignes.append (u)
    debut = 0
    for i in range (n - 1):
        u = []
        debut = debut + i
        k = debut
        for j in range (i, n):
            u.append (k)
            k = k + j + 2
        lignes.append (u)
    return lignes

def construireTriangle (n: int) -> graphe:
    """ retourne la grille triangulaire d'ordre n
    Exemple d'utilisation :

    >>> g = construireTriangle(4)"""
    g = __prefixer (_triangle (n), 's')
    # le 'nom' d'un graphe (label) sert aussi de nom de fichier
    # pour les dessins, eviter les blancs, etc
    nom = 'triangle' + str (n)
    g = construireGraphe (g, nom)
    # specifier le rapport hauteur / largeur pour l'algo 'dot'
    # perturbe legerement l'algo 'neato' 
    g.drawopts = "ratio=1.155"  # 2 / sqrt(3)
    return g

# Arbres (complets)

def _arbre (deg, hauteur, origine = 0):
    a = []
    if hauteur == 0:
        return []
    d = deg ** hauteur
    d = (d - 1) // (deg - 1)
    j = origine + 1
    for _ in range (deg):
        a.append ([origine, j])
        a = a + _arbre (deg, hauteur - 1, j)
        j = j + d
    return a

def construireArbre (deg: int, hauteur: int):
    """ retourne l'arbre de hauteur h dont chaque sommet possède d fils
    Exemple d'utilisation :

    >>> g = construireArbre(2, 3)"""
    g = __prefixer (_arbre (deg, hauteur), 's')
    # le 'nom' d'un graphe (label) sert aussi de nom de fichier
    # pour les dessins, eviter les blancs, etc
    nom = 'arbre' + str (deg) + 'x' + str(hauteur)
    g = construireGraphe (g, nom)
    return g


# Solides platoniciens

# autre description de K4
tetraedre = construireGraphe (
    [ ['A', 'B', 'C', 'A', 'D', 'B'], ['C', 'D'] ],
    'tetraedre')

# 6 faces, 8 sommets et 12 aretes
cube = construireGraphe (
    [ ['A', 'B', 'C', 'D', 'A'],
      ['a', 'b', 'c', 'd', 'a'],
      ['A', 'a'],
      ['B', 'b'],
      ['C', 'c'],
      ['D', 'd']
    ], 'cube')
cube.drawopts = 'edge [len = 2]'

octaedre = construireGraphe (
    [ ['A', 'B', 'C', 'D', 'A'],
      ['A', 'E', 'C', 'F', 'A'],
      ['B', 'E', 'D', 'F', 'B']
    ], 'octaedre')
octaedre.drawopts = 'edge [len = 2]'

# 12 faces, 20 sommets et 30 aretes
def _dodecaedre ():
    u = [list (range (20))]
    u = u + [[1, 9], [2, 11], [3, 13], [4, 0, 7]]
    u = u + [[5, 14], [6, 16], [8, 17], [10, 18], [12, 19, 15]]
    return u


dodecaedre = construireGraphe (
    __prefixer (_dodecaedre (), 's'), 'dodecaedre')
dodecaedre.drawopts = 'edge [len = 2]'

def _icosaedre ():
    u = [list (range (12))]
    u.append ([2, 0, 3, 8, 11, 6, 1, 5, 0, 4, 9, 3])
    u = u + [[1, 7, 2, 8], [4, 10, 5], [6, 10], [7, 11, 9]]
    return u


icosaedre = construireGraphe (
    __prefixer (_icosaedre (), 's'), 'icosaedre')
icosaedre.drawopts = 'edge [len = 2]'

_graphesPlanairesReguliers = [tetraedre, cube, octaedre, dodecaedre, icosaedre]


print("bibgraphes.py")
