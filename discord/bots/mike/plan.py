from typing import NamedTuple
import requests
from bs4 import BeautifulSoup


class Meal(NamedTuple):
    name: str
    meal: str
    price: float


def get_meals():
    URL = "https://www.imensa.de/karlsruhe/mensa-erzbergerstrasse/index.html"
    page = requests.get(URL)
    res = BeautifulSoup(page.content, "html.parser")

    meals = []
    for meal in res.select('.aw-meal-category'):
        n = meal.select('.aw-meal-category-name')[0].text
        m = meal.select_one('.aw-meal').select_one(
            'p.aw-meal-description').text
        p = meal.select_one('.aw-meal').select_one(
            '.aw-meal-price').text.replace('\xa0', ' ')
        meals.append(Meal(n, m, p))
    return meals
