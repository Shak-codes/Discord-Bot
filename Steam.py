from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

my_url = "https://store.steampowered.com/specials#p=0&tab=NewReleases"

uClient = uReq(my_url)
page_html = uClient.read()
uClient.close()
page_soup = soup(page_html, "html.parser")
total_games = len(page_soup.find_all('a', attrs={'class': 'tab_item'}))

a = int(input("Indicate from which game you wish to start the list on"))
b = int(input("Indicate from which game you wish to end the list on")) 

if a >= 1 and b <= int(total_games):
  a = a - 1
  c = b - a

  games = ""
  for x in range(c):
    container_name = page_soup.find_all('a', attrs={'class': 'tab_item'})
    container = container_name[a]

    a = a + 1
    name_container = container.find_all('div', attrs={'class': 'tab_item_name'})
    name = name_container[0].text

    original_price_container = container.find_all('div', attrs={'class': 'discount_original_price'})
    original_price = original_price_container[0].text

    discount_price_container = container.find_all("div", attrs={'class': 'discount_final_price'})
    discount_price = discount_price_container[0].text


    games += name + " | **Original Price** " + original_price + " | **Discounted Price** " + discount_price + "\n"

print(games)

