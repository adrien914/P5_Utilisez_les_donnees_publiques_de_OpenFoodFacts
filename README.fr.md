# P5 Utilisez les donnees publiques de OpenFoodFacts

Lisez ce fichier dans d'autres langues:

<a href="https://github.com/adrien914/P5_Utilisez_les_donnees_publiques_de_OpenFoodFacts/blob/master/README.md"><img src="https://github.com/adrien914/P5_Utilisez_les_donnees_publiques_de_OpenFoodFacts/blob/master/img/english.png"></a>
<a href="https://github.com/adrien914/P5_Utilisez_les_donnees_publiques_de_OpenFoodFacts/blob/master/README.fr.md"><img src="https://github.com/adrien914/P5_Utilisez_les_donnees_publiques_de_OpenFoodFacts/blob/master/img/french.png"></a>

## Contenu du repo
- Le script d'initialisation de la bdd dans database
- Le code de l'application dans utils et main.py
- La documentation dans le README.md
- Le fichier requirements.txt pour installer les librairies python

## Installation
N'oubliez pas d'avoir un serveur mysql qui tourne sur 0.0.0.0:3306 et 
d'y executer le script se trouvant dans database.
L'utilisateur de base est "root" et le password est "root", vous pouvez
changer les informations de la bdd dans settings.py 

- Pour installer l'application et la lancer, commencez par cloner le repo:
```bash
git clone https://github.com/adrien914/P5_Utilisez_les_donnees_publiques_de_OpenFoodFacts.git
```
    
- Installez virtualenv si ce n'est pas déja fait:
```bash
pip3 install virtualenv
```

- Créez un environnement virtuel:
```bash
virtualenv venv
```

- Activez cet environnement:
```bash
source venv/bin/activate
```

- Installez les requirements:
```bash
pip3 install -r requirements.txt
```

- Lancez le programme:
```bash
python3 main.py
```

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
        utilisera enumerate pour afficher "index: nom de la catégorie".
        Cette méthode permettra également de choisir la catégorie avec un
        input() qui appellera l'index de "categories" correspondant au choix
        fait dans l'input ( exemple: print_products(categories[input()])
  
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
        - Une méthode __init__ qui va initialiser la connection a la bdd et
        la récupération des données de la base OpenFoodFacts si besoin
        - Une méthode insert qui génèrera une instruction SQL INSERT a partir
        de headers et données données en arguments dans la table donnée en
        arguments
        - Une méthode select qui génèrera et executera une instruction SQL 
        SELECT pour la table donnée en argument avec les conditions données
        puis renverra le retour.
        - Une méthode update qui générera et éxécutera une instruction SQL UPDATE sur la table
        donnée en arguments avec les valeurs et conditions données en argument
        - Une méthode pour remplir la base de données a partir de l'api OpenFoodFacts au cas
        ou la bdd ne soit pas encore remplie.

#### Pouvoir modifier les valeurs importantes facilement
    Le programme inclura un fichier settings.py dans lequel on pourra modifier facilement
    les identifiants de connexion a la base de données et le nombre d'aliments et de produits
    à récupérer
