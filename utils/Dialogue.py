from utils.terminal import clear
from utils.Database import Database
import requests


class Dialogue:
    steps = ("choice", "categories", "products")
    current_step = 0

    def __init__(self):
        self.database = Database()
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
        aliments = self.database.select("aliment")
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
        request = requests.get(category["url"] + ".json")
        products = request.json()["products"]
        options = []
        for index, product in enumerate(products):
            print(str(index) + ". " + product["product_name"])
            options.append(product)
        print("-1. Revenir au menu principal")
        while True:
            try:
                choice = int(input())
                clear()
                if choice == -1:
                    self.main_menu()
                if 0 <= choice < len(options):
                    return self.show_product_info(options[choice], category)
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
                 "json=1".format(category["id"], nutrition_grade)
        return params

    def show_product_info(self, product, category):
        print("Infos produit:")
        print("Nom:", product["product_name"])
        print("Grade nutritionnel:", product["nutrition_grades"])
        if "stores" in product:
            print(product["stores"] + "\n")
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
            data = []
            for header in headers:
                data.append("'" + substitut[header].replace("'", "\\'") + "'")
            substitute_id = self.database.insert("substitute", headers, data)
        already_exists = self.database.select("aliment", "product_name = '{}'"
                                              .format(product["product_name"].replace("'", "\\'")))
        if already_exists:
            print("Cet aliment a déjà été substitué.")
        else:
            product["category"] = substitut["category"]
            headers = ["product_name", "category", "nutrition_grades", "stores"]
            data = []
            for header in headers:
                data.append("'" + product[header].replace("'", "\\'") + "'")
            headers.append("substitute_id")
            self.database.insert("aliment", headers, data, substitute_id)

    def search_substitute(self, product: dict, category: dict) -> dict:
        substitut = None
        search_url = "https://fr.openfoodfacts.org/cgi/search.pl"
        for i in range(0, 5):
            # get ascii value of A and add the current index to it so we can get the next letters
            nutrition_grade = chr(ord("A") + i)
            if ord(nutrition_grade) >= ord(product["nutrition_grades"]):  # if the ng is the same as the product break
                print("Nous n'avons pas pu trouver de substitut plus sain à ce produit")
                break
            params = Dialogue.generate_search_params(category, nutrition_grade)
            r = requests.get(search_url + params).json()
            if r["count"]:
                substitut = r["products"][0]
                print("Substitut:")
                print("Nom:", substitut["product_name"])
                print("Grade nutritionnel:", substitut["nutrition_grades"])
                print("Ou l'acheter:", substitut["stores"] + "\n")
                break
        if substitut:
            substitut["category"] = category["name"]
            return substitut
        return {}
