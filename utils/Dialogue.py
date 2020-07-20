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
                    return self.show_products(categories[choice])
                print("Choix inconnu")
            except ValueError:
                clear()
                print("Veuillez entrer un nombre entier svp")

    def show_substitutes(self):
        print("substitutes")

    def show_products(self, category):
        request = requests.get(category["url"] + ".json")
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
        print(product["product_name"])
        print(category)
        search_url = "https://fr.openfoodfacts.org/cgi/search.pl"
        for i in range(0, 5):
            # get ascii value of A and add the current index to it so we can get the next letters
            nutrition_grade = chr(ord("A") + i)
            params = Dialogue.generate_search_params(category, nutrition_grade)
            r = requests.get(search_url + params).json()
            if r["count"]:
                substitut = r["products"][0]
                print("Substitut:")
                print("Nom:", substitut["product_name"])
                print("Grade nutritionnel", substitut["nutrition_grades"])
                print("Ou l'acheter:", substitut["stores"])
                break
        if "stores" in product:
            print(product["stores"])
