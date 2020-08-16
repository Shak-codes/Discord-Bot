from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import pandas as pd

raw_game = input("What game would you like to search for?")
game = raw_game.replace(" ", "+")

my_url = "https://store.steampowered.com/search/?term=" + game
uClient = uReq(my_url)
page_html = uClient.read()
uClient.close()
page_soup = soup(page_html, "html.parser")

container_name = page_soup.find_all('span', attrs={'class': 'title'})
container_name_text = container_name[0].text

if raw_game in container_name_text:
    x = raw_game
else:
    x = container_name[0].text

steam = pd.read_csv("steam.csv")

x = steam.loc[steam["name"] == x]
x = x.iloc[0, 0]

my_url = "https://store.steampowered.com/app/" + str(x)
uClient = uReq(my_url)
page_html = uClient.read()
uClient.close()
page_soup = soup(page_html, "html.parser")

container_game = page_soup.find_all('div', attrs={'class': 'page_content_ctn'})
container = container_game[0]

container_name2 = container.find_all('div', attrs={'class': 'apphub_AppName'})
name = container_name2[0].text

container_dev = container.find_all('div', attrs={'class': 'apphub_AppName'})
container_image = container.find('img').get('src')

container_banner = container.find('img', attrs={'class': 'game_header_image_full'}).get('src')

container_description = container.find_all('div', attrs={'class': 'game_description_snippet'})
description = container_description[0].text

container_review = container.find_all('span', attrs={'class': 'game_review_summary positive'})
review = container_review[0].text

container_tags = container.find_all('a', attrs={'class': 'app_tag'})
tags = container_tags[0].text.strip() + "\n" + container_tags[1].text.strip() + "\n" + container_tags[2].text.strip()

container_price = container.find_all('div', attrs={'class': 'game_purchase_price price'})
price = container_price[0].text






