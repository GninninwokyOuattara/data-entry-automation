import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from urllib.parse import urlencode
import json

def format_link(url="/san-francisco-ca/rentals/", page = 0):
    if page == 0:
        link = f"https://www.zillow.com{url}"
        params = {
    "https://www.zillow.com/san-francisco-ca/rentals/?searchQueryState": {
        "usersSearchTerm": "San Francisco, CA",
        "mapBounds": {
            "west": -122.73819960546875,
            "east": -122.12845839453125,
            "south": 37.703343724016136,
            "north": 37.847169233586946
        },
        "mapZoom": 11,
        "regionSelection": [{ "regionId": 20330, "regionType": 6 }],
        "isMapVisible": "true",
        "filterState": {
            "price": { "max": 897707 },
            "beds": { "min": 1 },
            "pmf": { "value": "false" },
            "fore": { "value": "false" },
            "mf": { "value": "false" },
            "mp": { "max": 3000 },
            "ah": { "value": "true" },
            "auc": { "value": "false" },
            "nc": { "value": "false" },
            "fr": { "value": "true" },
            "land": { "value": "false" },
            "manu": { "value": "false" },
            "fsbo": { "value": "false" },
            "cmsn": { "value": "false" },
            "pf": { "value": "false" },
            "fsba": { "value": "false" }
        },
        "isListVisible": "true"
    }
}
        params_encoded = urlencode(params)


        return f"{link}?{params_encoded}"

    else:
        link = f"https://www.zillow.com{url}"
        params = {
    "searchQueryState": {
        "usersSearchTerm": "San Francisco, CA",
        "mapBounds": {
            "west": -122.73819960546875,
            "east": -122.12845839453125,
            "south": 37.703343724016136,
            "north": 37.847169233586946
        },
        "mapZoom": 11,
        "regionSelection": [{ "regionId": 20330, "regionType": 6 }],
        "isMapVisible": "true",
        "filterState": {
            "price": { "max": 897707 },
            "beds": { "min": 1 },
            "pmf": { "value": "false" },
            "fore": { "value": "false" },
            "mf": { "value": "false" },
            "mp": { "max": 3000 },
            "ah": { "value": "true" },
            "auc": { "value": "false" },
            "nc": { "value": "false" },
            "fr": { "value": "true" },
            "land": { "value": "false" },
            "manu": { "value": "false" },
            "fsbo": { "value": "false" },
            "cmsn": { "value": "false" },
            "pf": { "value": "false" },
            "fsba": { "value": "false" }
        },
        "isListVisible": "true",
        "pagination": { "currentPage": page }
    }
}

        params_encoded = urlencode(params)
        return f"{link}?{params_encoded}"

def requests_then_paginate(current_page, page_url):
    zillow_search_url = format_link(url=page_url,page = current_page)
    res = requests.get(url=zillow_search_url, headers=headers)
    soup = BeautifulSoup(res.text , "html.parser")
    data = soup.select("article.list-card.list-card-additional-attribution.list-card_not-saved")
    for article in data:
        price = article.select_one("div.list-card-info > div.list-card-heading > div").text
        price = price.split("/")[0]
        info = article.select_one("div.list-card-info > a")
        address = info.text
        url = info.get("href")

        article_obj = {
            "price" : price,
            "address" : address,
            "url" : url
        }
        # print(article_obj)
        search_results.append(article_obj)
    next_url = soup.select_one("#grid-search-results > div.search-pagination > nav > ul > li:nth-child(10) > a").get("href")
    print(next_url)
    next_page = int(next_url.split("/")[-2].split("_")[0])

    if next_page != current_page:
        return requests_then_paginate(next_page, next_url)
    



# zillow_search_url = "https://www.zillow.com/san-francisco-ca/rentals/?searchQueryState=%7B%22usersSearchTerm%22%3A%22San%20Francisco%2C%20CA%22%2C%22mapBounds%22%3A%7B%22west%22%3A-122.73819960546875%2C%22east%22%3A-122.12845839453125%2C%22south%22%3A37.703343724016136%2C%22north%22%3A37.847169233586946%7D%2C%22mapZoom%22%3A11%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A20330%2C%22regionType%22%3A6%7D%5D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22price%22%3A%7B%22max%22%3A897707%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%2C%22pmf%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22mf%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22ah%22%3A%7B%22value%22%3Atrue%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22land%22%3A%7B%22value%22%3Afalse%7D%2C%22manu%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22pf%22%3A%7B%22value%22%3Afalse%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%7D"


headers = {"User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36"}


search_results = []

# res = requests.get(url=zillow_search_url, headers=headers)
# re = res.request.url
# print(re)

requests_then_paginate(current_page= 0, page_url="/san-francisco-ca/rentals/")

with open("./data.json", "w") as f:
    json_data = json.dumps(search_results)
    f.write(json_data)