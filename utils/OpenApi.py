import requests
from settings import number_of_categories, aliments_per_category


class OpenApi:

    @staticmethod
    def get_categories() -> list:
        """
        Get a certain number of categories from the openfooodfacts api
        :return: the list of the categories retrieved from the api
        """
        request = requests.get("https://fr.openfoodfacts.org/categories.json")
        if request.status_code != 200:
            raise Exception("Il y a eu un problème avec la connexion a l'api OpenFoodFacts "
                            "veuillez reessayer plus tard")
        categories = request.json()["tags"][:number_of_categories]
        return categories

    @staticmethod
    def get_aliments( category):
        """
        Get a certain number of aliments from a category from the openfoodfacts api
        :param category: the category to retrieve the aliments from
        :return: the aliments retrieved from the api
        """
        request = requests.get(category[2] + ".json")
        products = request.json()["products"]
        return products
