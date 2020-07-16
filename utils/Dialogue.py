from utils.terminal import clear
import requests


class Dialogue:
    steps = ("choice", "categories", "products")
    current_step = 0

    def __init__(self):
        self.main_menu()

    def main_menu(self):
        options = [
            {"text": "Chercher un produit", "method": self.show_categories},
            {"text": "Voir mes aliments substitués", "method": self.show_substitutes},
        ]
        clear()
        print("Choisissez une option:")
        for index, option in enumerate(options):  # foreach
            print(str(index) + ". " + option["text"])
        while True:
            try:
                choice = int(input())
                clear()
                if 0 <= choice < len(options):
                    return options[choice]["method"]()
                print("Choix inconnu")
            except ValueError:
                clear()
                print("Veuillez entrer un nombre entier svp")

    def show_categories(self):
        request = requests.get("https://fr.openfoodfacts.org/categories.json")
        if request.status_code != 200:
            raise Exception("Il y a eu un problème avec la connexion a l'api OpenFoodFacts "
                            "veuillez reessayer plus tard")
        categories = request.json()["tags"][:10]
        for index, category in enumerate(categories):
            print(str(index) + ". " + category["name"])
        while True:
            try:
                choice = int(input())
                clear()
                if 0 <= choice < len(categories):
                    return self.show_products(categories[choice]["url"])
                print("Choix inconnu")
            except ValueError:
                clear()
                print("Veuillez entrer un nombre entier svp")

    def show_substitutes(self):
        print("substitutes")

    def show_products(self, category):
        request = requests.get(category + ".json")
        products = request.json()["products"]
        options = []
        for index, product in enumerate(products):
            print(str(index) + ". " + product["product_name"])
            options.append(product)
        while True:
            try:
                choice = int(input())
                clear()
                if 0 <= choice < len(options):
                    return self.show_product_info(options[choice])
                else:
                    print("Choix inconnu")
            except ValueError:
                clear()
                print("Veuillez entrer un nombre entier svp")

    def show_product_info(self, product):
        print(product["product_name"])
        if "stores" in product:
            print(product["stores"])
