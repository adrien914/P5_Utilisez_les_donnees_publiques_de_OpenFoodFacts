# P5 Utilisez les donnees publiques de OpenFoodFacts

Read this in other languages:


## Content of repository
- The database initialization script in the database directory
- The code of the application
- The documentation in the README
- A requirements.txt to install the required python libraries

## Installation
Don't forget to have a running mysql esrver on 0.0.0.0:3306 ( by default ) and to have executed
the .sql script that's in database in it.

The default user is root:root, this and all the infos on the database can be changed in settings.py

- To install the application clone this repository:
```bash
git clone https://github.com/adrien914/P5_Utilisez_les_donnees_publiques_de_OpenFoodFacts.git
```
    
- Install virtualenv if it's not already:
```bash
pip3 install virtualenv
```

- Create a virtual environment:
```bash
virtualenv venv
```

- Activate this environment:
```bash
source venv/bin/activate
```

- Install the requirements:
```bash
pip3 install -r requirements.txt
```

- Start the program:
```bash
python3 main.py
```

## Features

#### Chose between seeing the aliments or the substitutes
    The program should print the available choices, which command is used to make a choice
     ( example: 0: chercher produit, 1: voir substituts ),
    and allow to enter your choice.
    
    Code side, we'll have: 
        - A print to show the 2 options 
        - An input() to get the player's choice.
        - A dict that simulates a switch statement ( faster than multiple if statements ).
        - Two methods to print the aliments and substitutes.
    
#### Print the categories and chose one
    The program must fetch categories from the OpenFoodFacts API
    and display them with their corresponding command and allow you to go into one
    to see its available products
    
    Au niveau du code on mettra:
        - A method that retrieves categories within a certain interval
        (ex: the first 10 categories that the API returns) which will then use enumerate to display
         "index: category name" for each of them. This method will also allow you to choose the
        category with an input() which will call the index of "categories[]" corresponding to the choice
        done in the input (example: print_products(categories[input()])
  
#### View products and choose one
    The program must fetch the products contained in a given category and
    display them with the corresponding command and allow the user to see their info and a substitute.
    
    The code to retrieve the products will be very similar to that of the categories.
    For the rest of the features:
        - A method that displays the information you want on the product
        - A method which takes a product as an argument and which will search for
        a substitute based on the category and nutritional grade
        using the search url of the OpenFoodFacts API and which allows
        to save the information of this substitute in database

#### View the saved substitutes
    The program must fetch the substitutes that the user has
    saved in database and display them with the corresponding command to access
    their details.
    
#### Communicate with the database
    The program will have a Database() class which will connect to the database
    at its initialization and which will contain generic methods
    to communicate with the database.
    
    At the code level we will have:
        - An __init__ method which will initialize the connection to the database and
        retrieve data from the OpenFoodFacts database if necessary
        - An insert method which will generate a SQL INSERT statement from
        the headers and data given as arguments in the table given as
        arguments
        - A select method which will generate and execute an SQL statement
        SELECT for the table given as argument with the given conditions
        then will resend the return.
        - An update method which will generate and execute an SQL UPDATE statement on the table
        given as arguments with the values ​​and conditions given as arguments
        - A method to populate the database from the OpenFoodFacts API in case
        or the database is not yet full.

#### Allow the easy modification of important values
    The program will include a settings.py file in which we can easily modify
    the database connection identifiers and the number of foods and products
    to get from the API