from bs4 import BeautifulSoup
import numpy as np
from selenium import webdriver
import time
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

# load the webdriver
options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('disable-gpu')

driver = webdriver.Chrome(options=options)
               
links = [
   
    'https://www.simplyrecipes.com/dessert-recipes-5091513',
    'https://www.simplyrecipes.com/snacks-and-appetizer-recipes-5090762',
    'https://www.simplyrecipes.com/quick-snacks-and-appetizer-recipes-5090759',
    'https://www.simplyrecipes.com/drink-recipes-5091323',
    'https://www.simplyrecipes.com/holiday-and-seasonal-recipes-5091321',
    'https://www.simplyrecipes.com/recipes-by-ingredients-5091192',
    'https://www.simplyrecipes.com/recipes-by-method-5091235',
    'https://www.simplyrecipes.com/recipes-by-diet-5091259',
    'https://www.simplyrecipes.com/recipes-by-time-and-ease-5090817',
    'https://www.simplyrecipes.com/world-cuisine-recipes-5090811',
    'https://www.simplyrecipes.com/quick-recipes-5090813',
    'https://www.simplyrecipes.com/easy-recipes-5090816',
    'https://www.simplyrecipes.com/freezer-meal-recipes-5090815',
    'https://www.simplyrecipes.com/meal-prep-recipes-5090814',
    'https://www.simplyrecipes.com/comfort-food-recipes-5091432',
    'https://www.simplyrecipes.com/family-dinner-recipes-5091349',
    'https://www.simplyrecipes.com/side-dish-recipes-5091328',
    'https://www.simplyrecipes.com/sauce-recipes-5091342',
    'https://www.simplyrecipes.com/dinner-recipes-by-type-5091419',
    'https://www.simplyrecipes.com/dinner-recipes-by-ingredients-5091423',
    'https://www.simplyrecipes.com/dinner-recipes-by-diet-5091431',
    'https://www.simplyrecipes.com/dinner-recipes-by-time-and-ease-5091425',
    'https://www.simplyrecipes.com/healthy-breakfast-recipes-5091517',
    'https://www.simplyrecipes.com/easy-breakfast-recipes-5091519',
    'https://www.simplyrecipes.com/quick-breakfast-recipes-5091518',
    'https://www.simplyrecipes.com/gluten-free-breakfast-recipes-5091521',
    'https://www.simplyrecipes.com/vegan-breakfast-recipes-5091516',
    'https://www.simplyrecipes.com/brunch-recipes-5091522',
    'https://www.simplyrecipes.com/sandwich-recipes-5091260',
    'https://www.simplyrecipes.com/quick-lunch-5091261',
    'https://www.simplyrecipes.com/salad-recipes-5091411',
    'https://www.simplyrecipes.com/soup-recipes-5091377',
    'https://www.simplyrecipes.com/healthy-lunch-recipes-5091273',
    'https://www.simplyrecipes.com/easy-lunch-recipes-5091262',
    'https://www.simplyrecipes.com/comfort-food-recipes-5091432',
    'https://www.simplyrecipes.com/dessert-recipes-by-type-5091493',
    'https://www.simplyrecipes.com/quick-dessert-recipes-5091434',
    'https://www.simplyrecipes.com/easy-dessert-recipes-5091435',
    'https://www.simplyrecipes.com/dessert-recipes-by-diets-5091507',
    'https://www.simplyrecipes.com/dessert-recipes-by-ingredients-5091503',
    'https://www.simplyrecipes.com/dessert-sauce-recipes-5091512',
    'https://www.simplyrecipes.com/dip-recipes-5090764',
    'https://www.simplyrecipes.com/salsa-recipes-5090758',
    'https://www.simplyrecipes.com/easy-snacks-and-appetizer-recipes-5090761',
    'https://www.simplyrecipes.com/healthy-snacks-and-appetizer-recipes-5090760',
    'https://www.simplyrecipes.com/quick-snacks-and-appetizer-recipes-5090759',
    'https://www.simplyrecipes.com/recipe-collections-5119362',
    'https://www.simplyrecipes.com/meal-plans-5090752',
    'https://www.simplyrecipes.com/cooking-tips-and-techniques-5090748',
    'https://www.simplyrecipes.com/simply-curious-7508195',
    'https://www.simplyrecipes.com/ingredient-guides-5090749',
    'https://www.simplyrecipes.com/cleaning-and-organizing-8648889',
    'https://www.simplyrecipes.com/news-and-trends-5206826',
    'https://www.simplyrecipes.com/celebrity-8779178',
    'https://www.simplyrecipes.com/voices-5206832',
    'https://www.simplyrecipes.com/groceries-5206833',
    'https://www.simplyrecipes.com/features-7558492',
    'https://www.simplyrecipes.com/holiday-and-seasonal-recipes-5091321',
    
]
data = []

# url = "https://www.simplyrecipes.com/most-recent-5121175"

# scrape the website
def scrape_simlpy_recipes(url):

    driver.get(url)
    time.sleep(5)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    recipes = soup.find_all('a', class_="comp mntl-card-list-items mntl-document-card mntl-card card card--no-image")
    for recipe in recipes:
        link = recipe['href']
        if link == None:
            link = 'Nan'
        else:
            link = link
        recipe_title = recipe.find('span', class_="card__title")
        if recipe_title == None:
            recipe_title = 'Nan'
        else:
            recipe_title = recipe_title.text

        category = recipe.find('div', class_='card__content')['data-tag']
        if category == None:
            category = 'Nan'
        else:
            category = category

        print('----------------------------')
        print(recipe_title)
        print(link)
        print(category)
        # simulate a click on the recipe 
        driver.get(link)
        time.sleep(5)
        recipe_soup = BeautifulSoup(driver.page_source, 'html.parser')
        # ingredients = recipe_soup.find_all('li', class_='ingredient')
        author = recipe_soup.find('a', class_="mntl-attribution__item-name")
        if author == None:
            author = 'Nan'
        else:
            author = author.text

        print(author)
        publish_date = recipe_soup.find('div', class_="mntl-attribution__item-date")
        if publish_date == None:
            publish_date = 'Nan'
        else:
            publish_date = publish_date.text

        print(publish_date)
        content = recipe_soup.find('div', class_="comp article-content-container mntl-block")
        if content == None:
            content = 'Nan'
        else:
            content = content.text


        print(content)
        print('----------------------------')

        data.append({
            'title': recipe_title,
            'link': link,
            'category': category,
            'author': author,
            'publish_date': publish_date,
            'content': content
        })

        df = pd.DataFrame(data)
        df.to_csv('simply_recipes_v10.csv', index=False)
        print('----------------------------')

    
    return df



if __name__ == "__main__":
    for url in links:
        scrape_simlpy_recipes(url)
    driver.quit()
