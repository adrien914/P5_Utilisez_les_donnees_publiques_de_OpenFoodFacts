from utils.terminal import clear
from utils.Database import Database
import requests
from utils.OpenApi import OpenApi


class Dialogue:

    def __init__(self):
        self.database = Database()
        self.main_menu()
        self.open_api = OpenApi()

    def main_menu(self) -> None:
        """
        This function prints the main menu for the application and gets the input for the options
        :return: None
        """
        options = [
            {"text": "Chercher un produit", "method": self.show_categories},
            {"text": "Voir mes aliments substitués", "method": self.show_substitutes},
        ]  # Put the options in a list as dicts with a pointer to the method they have to call
        clear()
        while True:
            for index, option in enumerate(options):  # foreach option print it with its index
                print(str(index) + ". " + option["text"])
            print("\x1b[6;32;40mChoisissez une option en écrivant le chiffre correspondant et "
                  "appuyez sur entrée:\x1b[0m")
            try:
                choice = int(input())
                clear()
                if 0 <= choice < len(options):  # if the input is within the range of options available
                    return options[choice]["method"]()  # call the method that's in the option at 'index'
                print("\x1b[6;31;40mChoix inconnu\x1b[0m")
            except ValueError:  # int(input()) throws a ValueError
                clear()
                print("\x1b[6;31;40mVeuillez entrer un nombre entier svp\x1b[0m")

    def show_categories(self) -> None:
        """
        This method prints the categories available in the database and gets an input from the user to chose
        which category to search in
        :return: None
        """
        categories = self.database.select("category")  # Get all the categories in the db
        while True:
            for index, category in enumerate(categories):  # for each category
                print(str(index) + ". " + category[1])  # print the category name and its index
            print("-1. Revenir au menu principal")
            print("\x1b[6;32;40mChoisissez une option en écrivant le chiffre correspondant et "
                  "appuyez sur entrée:\x1b[0m")
            try:
                choice = int(input())
                clear()
                if choice == -1:
                    self.main_menu()
                if 0 <= choice < len(categories):
                    # Show the products corresponding to the chosen category
                    return self.show_products(categories[choice])
                print("\x1b[6;31;40mChoix inconnu\x1b[0m")
            except ValueError:  # int(input()) throws a ValueError
                clear()
                print("\x1b[6;31;40mVeuillez entrer un nombre entier svp\x1b[0m")

    def show_products(self, category: list) -> None:
        """
        This method prints the products that are in the category given in the arguments and gets an input from the
        user to chose a product
        :param category: list
        :return: None
        """
        # Retrieve the products that have the chosen category's id in their category field
        products = self.database.select("aliment", "category=" + str(category[0]))
        while True:
            for index, product in enumerate(products):
                print(str(index) + ". " + product[1])
            print("-1. Revenir au menu principal")
            print("\x1b[6;32;40mChoisissez une option en écrivant le chiffre correspondant et "
                  "appuyez sur entrée:\x1b[0m")
            try:
                choice = int(input())
                clear()
                if choice == -1:
                    self.main_menu()
                if 0 <= choice < len(products):
                    return self.show_product_info(products[choice], category)
                else:
                    print("\x1b[6;31;40mChoix inconnu\x1b[0m")
            except ValueError:  # int(input()) throws a ValueError
                clear()
                print("\x1b[6;31;40mVeuillez entrer un nombre entier svp\x1b[0m")

    @staticmethod
    def generate_search_params(category: list, nutrition_grade: str) -> str:
        """
        This method generates the search parameters needed to get the products from a category and a certain
        nutrition grade
        :param category: the category from which the product is
        :param nutrition_grade: the nutrition grade of the product
        :return: the parameters to add to the search URL
        """
        params = "?action=process&" \
                 "tagtype_0=categories&" \
                 "tag_contains_0=contains&" \
                 "tag_0={}&" \
                 "tagtype_1=nutrition_grades&" \
                 "tag_contains_1=contains&" \
                 "tag_1={}&" \
                 "json=1".format(category[0], nutrition_grade)
        return params

    def show_product_info(self, product: list, category: list) -> None:
        """
        This function shows the infos on a product, searchs for a substitute and asks the user if he wants to save it
        in the database
        :param product: the product the user chose
        :param category: the category of the product ( used to search for the substitute )
        :return: None
        """
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
            print("\x1b[6;32;40mChoisissez une option en écrivant la lettre correspondante et "
                  "appuyez sur entrée:\x1b[0m")
            while True:
                choice = input()
                if str(choice).lower() == "o":
                    self.save_substitute(substitut, product)
                    print("\x1b[6;32;40mSubstitut sauvegardé avec succès!\x1b[0m")
                    break
                elif str(choice).lower() == "n":
                    print("Substitut non sauvegardé.")
                    break
                else:
                    print("\x1b[6;31;40mVeuillez entrer un choix valide svp\x1b[0m")
        print("\nAppuyez sur entrée pour revenir au menu principal")
        input()
        self.main_menu()

    def save_substitute(self, substitut: dict, product: list) -> None:
        """
        This method saves a substitute to the database and links it to an aliment
        :param substitut: The substitute we got from the API
        :param product: the product the user chose ( to link the substitute to it )
        :return: None
        """
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
                except AttributeError:  # if it's an int ( = the id of the category )
                    data.append(str(substitut["category"]))
            substitute_id = self.database.insert("substitute", headers, data)
        # update the aliment with the substitute's id
        self.database.update("aliment", ["substitute_id=" + str(substitute_id)], ["id=" + str(product[0])])

    def search_substitute(self, product: list, category: list) -> dict:
        """
        Uses the search API to retrieve a more healthy substitute to a product
        :param product: the product we want to search a substitute for
        :param category: the category of the product
        :return: the found substitute or an empty dict
        """
        substitut = None
        search_url = "https://fr.openfoodfacts.org/cgi/search.pl"
        for i in range(0, 5):
            # get ascii value of A and add the current index to it so we can get the next letters
            nutrition_grade = chr(ord("A") + i)
            if ord(nutrition_grade) >= ord(product[3]):  # if the nutrigrade is the same as the product's, break
                print("Nous n'avons pas pu trouver de substitut plus sain à ce produit")
                break
            params = Dialogue.generate_search_params(category[1], nutrition_grade)
            r = requests.get(search_url + params).json()  # get the search url with the generated search params
            if r["count"]:
                substitut = r["products"][0]
                print("\nSubstitut:")
                print("Nom:", substitut["product_name"])
                try:
                    print("Grade nutritionnel:", substitut["nutrition_grades"])
                except KeyError:
                    pass
                try:
                    print("Ou l'acheter:", substitut["stores"] + "\n")
                except KeyError:
                    pass
                break
        if substitut:
            substitut["category"] = category[1]
            return substitut
        return {}

    def show_substitutes(self) -> None:
        """
        Show all the aliments that have a substitute saved in the database
        :return: None
        """
        aliments = self.database.select("aliment", "substitute_id is not null")
        while True:
            for index, aliment in enumerate(aliments):
                print(str(index) + ". " + aliment[1])
            print("-1. Revenir au menu principal")
            print("\x1b[6;32;40mChoisissez une option en écrivant le chiffre correspondant et "
                  "appuyez sur entrée:\x1b[0m")
            try:
                choice = int(input())
                clear()
                if choice == -1:
                    self.main_menu()
                if 0 <= choice < len(aliments):
                    self.show_substitute_infos(aliments[choice])
                else:
                    print("\x1b[6;31;40mChoix inconnu\x1b[0m")
            except ValueError:  # int(input()) throws a ValueError
                clear()
                print("\x1b[6;31;40mVeuillez entrer un nombre entier svp\x1b[0m")

    def show_substitute_infos(self, aliment) -> None:
        """
        Show the infos on a saved substitute
        :param aliment: the aliment chosen by the user
        :return: None
        """
        substitute = self.database.select("substitute", "id=" + str(aliment[-1]))[0]
        category = self.database.select("category", "id=" + str(substitute[2]))
        print("Substitut à {}:".format(aliment[1]))
        print("nom:", substitute[1])
        print("categorie:", category[0][1])
        print("grade nutritionnel:", substitute[3])
        print("Magasins:", substitute[4])
        print("\nAppuyez sur entrée pour revenir au menu principal")
        input()
        self.main_menu()
