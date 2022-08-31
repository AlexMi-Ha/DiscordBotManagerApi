import requests
from bs4 import BeautifulSoup


def get_diet():
    URL = "https://mydiet.chr1shaefn3r.dev/today"
    page = requests.get(URL)
    res = BeautifulSoup(page.content, "html.parser")

    diet = res.select_one(
        'p.MuiTypography-root.MuiTypography-body1.MuiTypography-alignLeft')
    if diet == None:
        return "Nothing today"
    return diet.text


if __name__ == "__main__":
    print(get_diet())
