# Tableau : structure de données séquentielle
<script type="text/javascript" charset="utf-8" src="
https://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML,
https://vincenttam.github.io/javascripts/MathJaxLocal.js"></script>

<div class="alert alert-warning" role="alert"><b>Définition: </b><br>
Un tableau à une dimension est une structure de données qui permet de stocker un certain nombre d’éléments repérés par un indice encore appelé clé (index). Les tableaux vérifient généralement les propriétés suivantes :
    <ul>
        <li> Tous les éléments ont le même type de base.</li>
        <li> le nombre maximum d’éléments que l'on peut stocker est fixé.</li> 
        <li> La **taille** d’un tableau est le nombre de cases mémoire qui le composent.</li>
        <li>L’accès et la modification d'un l’élément d'index donné est en temps constant (noté $\Theta(1))$, indépendamment de l'indice et de la taille du tableau.</li>
    </ul>
    </div>

## Déclaration d'un tableau

La déclaration d'un tableau comprend deux informations : 
* le nombre maximum d'éléments
* le type de valeurs prises par ses éléments 

### De taille fixe

* Java : ```int[] tableau``` Définit un tableau d'entiers non encore initialisé. Nombre d'éléments pas encore connu.
* C : ```int tableau[10]``` Définit un tableau prêt à recevoir 10 valeurs entières.
* Python : ```tableau = zeros(10)``` Définit un tableau contenant 10 zéros avec le package ```numpy```.

### De taille variable

Pour simuler un tableau de taille variable, on peut:
    
* réserver une quantité de mémoire strictement supérieure à celle nécéssaire pour les éléments de départ,
* et ranger les éléments au début du tableau.

**Attention** la bibliothèque principale de Python fournit des objets de type: 
* ```list```, équivalent Python d'un tableau, mais cet objet est redimensionnable et peut contenir des éléments de différents types.
* ```array``` très similaire aux objets de type *list* mais ne peut contenir des éléments que d'un seul type définit au moment de la déclaration : https://docs.python.org/fr/3/library/array.html

## Tableau en mémoire

Les tableaux forment une suite de variables de même type associées à des emplacements consécutifs de la mémoire. Puisque tous les emplacements sont de même type, ils occupent tous la même taille mémoire $d$. Connaissant l’adresse $a$ de la première case du tableau, on accède en coût constant à l’adresse de la case d’indice $k$ en calculant $a + kd$.


```python
from array import *
l = array('i', [0]*10)
print(f'item_size = {l.itemsize} octets') #La longueur en octets d'un élément du tableau dans la représentation interne.
print(f'memory_size = {l.buffer_info()[1]*l.itemsize} octets')
```

    item_size = 4 octets
    memory_size = 40 octets


### Problème de la taille maximum

On essaye d’insérer un élément dans un tableau qui ne contient plus de place disponible.

Comportements possibles :

* Erreur (arrêt du programme, exception)
* Allocation d'un nouveau bloc mémoire, puis recopie des éléments de l'ancien tableau dans le nouveau.

Extrait des sources du langage Python, fichier listobject.c, lignes 61-70: https://github.com/python/cpython/blob/main/Objects/listobject.c

``` 
    /*This over-allocates proportional to the list size, making room
     * for additional growth.  The over-allocation is mild, but is
     * enough to give linear-time amortized behavior over a long
     * sequence of appends() in the presence of a poorly-performing
     * system realloc().
     * Add padding to make the allocated size multiple of 4.
     * The growth pattern is:  0, 4, 8, 16, 24, 32, 40, 52, 64, 76, ...
     * ...
     */
```

Pour les objets Python de type ```list``` l'algorithme permettant d'étendre la taille travaille en **temps constant amortis**. C’est une situation très classique : dans de nombreux problèmes, il est possible d’aller plus vite en utilisant plus de mémoire

## Opérations sur les tableaux

Soient $N\in\mathbb{N}$ le nombre d'éléments dans le tableau et $i\in\mathbb{N}$ l'indice de position d'un élément dans le tableau

### Opérations élémentaires

* Initialiser un tableau $\Theta(N)$
* accéder au premier élément $\Theta(1)$
* accéder à un élément d'indice i $\Theta(1)$
* accéder au dernier élément $\Theta(1)$
* Afficher les éléments d’un tableau $\Theta(N)$
* Rechercher si une valeur est dans un tableau ($O(N)$ au pire, $O(1)$ au mieux)
* Échanger le contenu de 2 cases du tableau $\Theta(1)$
* Insérer/supprimer un nouvel élément dans un tableau $\Theta(N-i)$ (insister sur la complexité de l'insertion suivant la place de l'élément à insérer)
* Pour tous les éléments du tableau faire...
* Existe-t-il un élément du tableau qui...?

### Trier un tableau

Ce sont des algorithmes n'utilisant aucun paradigme ni aucune structure de données élaborée.

* Tri sélection
* Tri insertion
* Tri bulles


## Les tableaux avec Python
Plusieurs possibilités:
* dans les types natifs
    * les objets de type ```list```,
    * les objets de type ```array```,
* package ```numpy```
    * les objets de type ```ndarray```.

Dans ce cours d'algorithmique nous utiliserons les objets de type `array` comme `tableau` mais nous limiterons les possibilités offertes par Python sur cet objet pour se rapprocher le plus possible des types tableaux disponibles dans d'autres langages de programmation. L'aspect uniquement déclaratif d'une variable n'existe pas en Python, il faut l'associer à son initialisation.

**Remarque :** Attention ce cours est un **cours d'algorithmique** et ne vise pas à être un cours de programmation en Python ; il n'aborde pas les spécificités de ce langage, et les notions présentées s'efforcent de rester valables dans la majorité des autres langages de programmation.

### Initialiser un tableau avec array

La doc officielle : https://docs.python.org/fr/3/library/array.html
    
Ces tableaux ont la particularité de posséder un type:


```python
import array as arr
tableau = arr.array('l', [1, 2, 3, 4])
print(type(tableau))
print(tableau.typecode)
print(tableau.itemsize)
print(tableau.buffer_info())
```

    <class 'array.array'>
    l
    8
    (140475163192816, 4)


**Initialiser un tableau de type array de taille fixe**


```python
tab1 = arr.array('l', [0]*10) # avec 10 éléments
print(tableau[0])
```

    0


**Le genre d'erreur que vous allez rencontrer**


```python
tableau = arr.array('l', ['a'])
```


    ---------------------------------------------------------------------------

    TypeError                                 Traceback (most recent call last)

    /tmp/ipykernel_378887/3427128909.py in <module>
    ----> 1 tableau = arr.array('l', ['a'])
    

    TypeError: an integer is required (got type str)



```python
tableau = arr.array('I', [-2])
```


    ---------------------------------------------------------------------------

    OverflowError                             Traceback (most recent call last)

    /tmp/ipykernel_378887/75693290.py in <module>
    ----> 1 tableau = arr.array('I', [-2])
    

    OverflowError: can't convert negative value to unsigned int


**Ce que vous ne pouvez pas faire**


```python
tableau = arr.array([1, "bonjour"])
```


    ---------------------------------------------------------------------------

    TypeError                                 Traceback (most recent call last)

    /tmp/ipykernel_378887/3890430680.py in <module>
    ----> 1 tableau = arr.array([1, "bonjour"])
    

    TypeError: array() argument 1 must be a unicode character, not list


## Exercices:

Écrire un algorithme pour résoudre les problèmes suivants ;

1. afficher les éléments d'un tableau
2. insertion d’un élément à la fin ;
3. insertion d’un élément en position i ;
4. insertion d’un élément au début ;
5. suppression d’un élément à la fin ;
6. suppression d’un élément en position i ;
7. suppression d’un élément au début ;
8. Étant donné un entier n, trouver un l’entier le plus proche de n dans le tableau.
9. Le tableau est-il trié ?

christophe.casseau@u-bordeaux.fr
