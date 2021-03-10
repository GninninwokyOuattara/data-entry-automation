import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from urllib.parse import urlencode
import json
import os

CHROME_DRIVER_PATH = os.environ.get("CHROME_DRIVER_PATH")
FORM_LINK = os.environ.get("FORM_LINK")
SHEET_LINK = os.environ.get("SHEET_LINK")


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
    print(f"> Visiting page : {current_page}", end="\r")
    zillow_search_url = format_link(url=page_url,page = current_page)
    res = requests.get(url=zillow_search_url, headers=headers)
    soup = BeautifulSoup(res.text , "html.parser")
    data = soup.select("article.list-card.list-card-additional-attribution.list-card_not-saved")
    for article in data:
        price = article.select_one("div.list-card-info > div.list-card-heading > div").text
        price = price.split("/")[0]
        info = article.select_one("div.list-card-info > a")
        address = info.text
        url : str = info.get("href")
        if not url.startswith("https://"):
            url = f"https://www.zillow.com{url}"

        article_obj = {
            "price" : price,
            "address" : address,
            "url" : url
        }
        # print(article_obj)
        search_results.append(article_obj)
    next_url = soup.select_one("#grid-search-results > div.search-pagination > nav > ul > li:nth-child(10) > a").get("href")
    
    next_page = int(next_url.split("/")[-2].split("_")[0])

    if next_page != current_page:
        return requests_then_paginate(next_page, next_url)
    print("\n")
    



headers = {"User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36"}


search_results = []

print("Scrapping ....")
requests_then_paginate(current_page= 0, page_url="/san-francisco-ca/rentals/")

# with open("./data.json", "w") as f:
#     json_data = json.dumps(search_results)
#     f.write(json_data)
driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH)

print("Forms completion ...")
i = 1
total = len(search_results)
for result in search_results:
    print(f"{i}/{total} > Filling for : {result['address']}", end="\r")
    driver.get(url=FORM_LINK)
    address = driver.find_element_by_css_selector("#mG61Hd > div.freebirdFormviewerViewFormCard.exportFormCard > div > div.freebirdFormviewerViewItemList > div:nth-child(1) > div > div > div.freebirdFormviewerComponentsQuestionTextRoot > div > div.quantumWizTextinputPaperinputMainContent.exportContent > div > div.quantumWizTextinputPaperinputInputArea > input")
    price = driver.find_element_by_css_selector("#mG61Hd > div.freebirdFormviewerViewFormCard.exportFormCard > div > div.freebirdFormviewerViewItemList > div:nth-child(2) > div > div > div.freebirdFormviewerComponentsQuestionTextRoot > div > div.quantumWizTextinputPaperinputMainContent.exportContent > div > div.quantumWizTextinputPaperinputInputArea > input")
    url = driver.find_element_by_css_selector("#mG61Hd > div.freebirdFormviewerViewFormCard.exportFormCard > div > div.freebirdFormviewerViewItemList > div:nth-child(3) > div > div > div.freebirdFormviewerComponentsQuestionTextRoot > div > div.quantumWizTextinputPaperinputMainContent.exportContent > div > div.quantumWizTextinputPaperinputInputArea > input")

    send = driver.find_element_by_css_selector("#mG61Hd > div.freebirdFormviewerViewFormCard.exportFormCard > div > div.freebirdFormviewerViewNavigationNavControls > div.freebirdFormviewerViewNavigationButtonsAndProgress > div > div")

    address.send_keys(result["address"])
    price.send_keys(result["price"])
    url.send_keys(result["url"])
    send.click()
    i+=1

print("\nForm completion completed.")
print("Opening sheet...")
driver.get(SHEET_LINK)
print("Done.")