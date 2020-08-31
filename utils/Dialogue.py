from utils.terminal import clear
from utils.Database import Database
import requests
from utils.OpenApi import OpenApi

class Dialogue:

    def __init__(self):
        self.database = Database()
        self.main_menu()
        self.open_api = OpenApi()

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
        categories = self.database.select("category")
        for index, category in enumerate(categories):
            print(str(index) + ". " + category[1])
        print("-1. Revenir au menu principal")
        while True:
            try:
                choice = int(input())
                clear()
                if choice == -1:
                    self.main_menu()
                if 0 <= choice < len(categories):
                    return self.show_products(categories[choice])
                print("Choix inconnu")
            except ValueError:
                clear()
                print("Veuillez entrer un nombre entier svp")

    def show_substitutes(self):
        aliments = self.database.select("aliment", "substitute_id is not null")
        print("Choisissez un aliment:")
        for index, aliment in enumerate(aliments):
            print(str(index) + ". " + aliment[1])
        print("-1. Revenir au menu principal")
        while True:
            try:
                choice = int(input())
                clear()
                if choice == -1:
                    self.main_menu()
                if 0 <= choice < len(aliments):
                    self.show_substitute_infos(aliments[choice])
                else:
                    print("Choix inconnu")
            except ValueError:
                clear()
                print("Veuillez entrer un nombre entier svp")

    def show_substitute_infos(self, aliment):
        substitute = self.database.select("substitute", "id=" + str(aliment[-1]))[0]
        print("Substitut à {}:".format(aliment[1]))
        print("nom:", substitute[1])
        print("categorie:", substitute[2])
        print("grade nutritionnel:", substitute[3])
        print("Magasins:", substitute[4])
        print("\nAppuyez sur entrée pour revenir au menu principal")
        input()
        self.main_menu()

    def show_products(self, category):
        products = self.database.select("aliment", "category=" + str(category[0]))
        for index, product in enumerate(products):
            print(str(index) + ". " + product[1])
        print("-1. Revenir au menu principal")
        while True:
            try:
                choice = int(input())
                clear()
                if choice == -1:
                    self.main_menu()
                if 0 <= choice < len(products):
                    return self.show_product_info(products[choice], category)
                else:
                    print("Choix inconnu")
            except ValueError:
                clear()
                print("Veuillez entrer un nombre entier svp")

    @staticmethod
    def generate_search_params(category, nutrition_grade):
        params = "?action=process&" \
                 "tagtype_0=categories&" \
                 "tag_contains_0=contains&" \
                 "tag_0={}&" \
                 "tagtype_1=nutrition_grades&" \
                 "tag_contains_1=contains&" \
                 "tag_1={}&" \
                 "json=1".format(category[0], nutrition_grade)
        return params

    def show_product_info(self, product, category):
        print("Infos produit:")
        print("Nom:", product[1])
        print("Grade nutritionnel:", product[3])
        if "stores" in product:
            print(product[4] + "\n")
        substitut = self.search_substitute(product, category)
        if substitut:
            print("Voulez-vous enregistrer le substitut en base de données ?")
            print("o. Oui")
            print("n. Non")
            choice = input()
            if choice.lower() == "o":
                self.save_substitute(substitut, product)
            print("\nAppuyez sur entrée pour revenir au menu principal")
            input()
            self.main_menu()

    def save_substitute(self, substitut, product):
        already_exists = self.database.select("substitute", "product_name = '{}'"
                                              .format(substitut["product_name"].replace("'", "\\'")))
        if already_exists:
            substitute_id = already_exists[0][0]
        else: # if the substitute doesn't exist create it
            headers = ["product_name", "category", "nutrition_grades", "stores"]
            substitut["category"] = product[2]
            data = []
            for header in headers:
                try:
                    data.append("'" + substitut[header].replace("'", "\\'") + "'")
                except KeyError:
                    data.append("NULL")
                except AttributeError:
                    data.append(str(substitut["category"]))
            substitute_id = self.database.insert("substitute", headers, data)
        self.database.update("aliment", ["substitute_id=" + str(substitute_id)], ["id=" + str(product[0])])

    def search_substitute(self, product: dict, category: list) -> dict:
        substitut = None
        search_url = "https://fr.openfoodfacts.org/cgi/search.pl"
        print("search sub")
        for i in range(0, 5):
            # get ascii value of A and add the current index to it so we can get the next letters
            nutrition_grade = chr(ord("A") + i)
            if ord(nutrition_grade) >= ord(product[3]):  # if the nutrigrade is the same as the product's, break
                print("Nous n'avons pas pu trouver de substitut plus sain à ce produit")
                break
            params = Dialogue.generate_search_params(category[1], nutrition_grade)
            print(category)
            r = requests.get(search_url + params).json()
            if r["count"]:
                substitut = r["products"][0]
                print("\nSubstitut:")
                print("Nom:", substitut["product_name"])
                print("Grade nutritionnel:", substitut["nutrition_grades"])
                print("Ou l'acheter:", substitut["stores"] + "\n")
                break
        if substitut:
            substitut["category"] = category[1]
            return substitut
        return {}
