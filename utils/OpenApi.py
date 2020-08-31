import requests
from settings import number_of_categories, aliments_per_category


class OpenApi:

    def get_categories(self):
        request = requests.get("https://fr.openfoodfacts.org/categories.json")
        if request.status_code != 200:
            raise Exception("Il y a eu un problème avec la connexion a l'api OpenFoodFacts "
                            "veuillez reessayer plus tard")
        categories = request.json()["tags"][:number_of_categories]
        return categories

    def get_aliments(self):
        return