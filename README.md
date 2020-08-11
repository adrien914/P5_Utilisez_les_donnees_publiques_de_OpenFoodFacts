# P5 Utilisez les donnees publiques de OpenFoodFacts

## Contenu du repo
- le script d'initialisation de la bdd dans database
- le code de l'application dans utils et main.py
- La documentation dans le README.md

## Installation



## Fonctionnalités

#### Choisir entre chercher un produit ou voir les aliments substitués
    Le programme doit afficher les choix disponibles, quelle commande permet
    de faire son choix ( exemple: 0: chercher produit, 1: voir substituts ),
    et qu'on puisse envoyer notre choix a l'application.
    
    Au niveau du code on mettra: 
        - Un print en dur pour les 2 options vu qu'elles 
        sont statiques. 
        - Un input() pour récupérer ce que l'utilisateur envoie.
        - Un dict qui simule un switch statement pour pouvoir accéder
        aux méthodes ciblées par les options plus rapidement qu'avec des if.
        - Deux méthodes pour afficher les catégories et voir les substituts.
    
#### Afficher les catégories et en choisir une
    Le programme doit aller chercher des catégories sur l'api OpenFoodFacts
    et les afficher avec la commande correspondante et permettre de rentrer
    dedans pour voir les produits disponibles
    
    Au niveau du code on mettra:
        - Une méthode qui récupère les catégories dans un certain intervalle
        ( ex: les 10 premières catégories que l'api renvoie ) puis qui
        utilisera enumerate pour afficher "index: nom de la catégorie"
        et ajouter les data de la catégorie à ce même index dans un 
        dictionnaire ( exemple: options[index] = categorie ).
        Cette méthode permettra également de choisir la catégorie avec un
        input() qui appellera la clé du dictionnaire correspondant au choix
        fait dans l'input ( exemple: print_products(options[input()])
  
#### Afficher les produits et en choisir un
    Le programme doit aller chercher les produits contenus dans une catégorie
    donnée. Les afficher avec la commande correspondante et permettre de
    voir leurs infos et un substitut.
    
    Le code sera très proche de celui des catégories pour récupérer les
    produits, les afficher et y accéder.
    Pour le reste des fonctionnalités:
        - Une méthode qui affiche les infos qu'on veut sur le produit
        - Une méthode qui prend un produit en argument et qui va chercher
        un substitut a partir de la catégorie et du grade nutritionnel
        en utilisant l'url de recherche de l'api OpenFoodFacts et qui permet
        de sauvegarder les infos de ce substitut en bdd

#### Voir les substituts
    Le programme doit aller chercher les substituts que l'utilisateur a
    sauvegardés en bdd et les afficher avec la commande correspondante pour accéder
    à leur details.
    
#### Communiquer avec la bdd
    Le programme aura une classe Database() qui se connectera a la base de
    données a son initialisation et qui contiendra des méthodes génériques
    pour communiquer avec la base de données.
    
    Au niveau du code on aura:
        - Une méthode __init__ qui va initialiser la connection a la bdd
        - Une méthode insert qui génèrera une instruction SQL INSERT a partir
        de headers et données données en arguments dans la table donnée en
        arguments
        - Une méthode select qui génèrera et executera une instruction SQL 
        SELECT pour la table donnée en argument avec les conditions données
        puis renverra le retour.
