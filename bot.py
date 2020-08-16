import discord
import linecache2
import random
import pandas as pd
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
from discord.ext import commands
import key

client = commands.Bot(command_prefix = ".")

@client.event
async def on_ready():
    print("Ready")  

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('hey'):
        await message.channel.send('hello')
    
    if message.content.startswith('???'):
        await message.channel.send('???')

    await client.process_commands(message)

@client.command()
@commands.has_permissions(manage_messages=True)
async def delete(ctx, amount):
    number = int(amount) + 1
    await ctx.channel.purge(limit=number)

@delete.error
async def delete_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You do not have permissions to delete messages")

@client.command()
async def fc(ctx):
    await ctx.send("1342-1744-9712")

@client.command()
async def steam(ctx, a, b):

    my_url = "https://store.steampowered.com/specials#p=0&tab=NewReleases"

    uClient = uReq(my_url)
    page_html = uClient.read()
    uClient.close()
    page_soup = soup(page_html, "html.parser")
    
    total_games = len(page_soup.find_all('a', attrs={'class': 'tab_item'}))
    a = int(a)
    b = int(b) - 1
    if a >= 1 and b <= int(total_games):

        a = a - 1
        c = b - a + 1
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

            games += "**" + name + "**" + " **|** Original Price - " + "*" + original_price + "*" + " **|** Discounted Price - " + "*" + discount_price + "*" + "\n\n"
        embed = discord.Embed(
            title = 'Games on Sale',
            description = games,
            colour = discord.Colour.green()
        )
        await ctx.send(embed=embed)

    else:
        await ctx.send("Please enter valid numbers from 1 to " + str(total_games))

@client.command()
async def steam_search(ctx, raw_game):

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

    #container_price = container.find_all('div', attrs={'class': 'game_purchase_price price'})
    #price = container_price[0].text

    embed = discord.Embed(
        title = name,
        url = my_url,
        description = description,
        colour = discord.Colour.green()
    )

    embed.set_image(url=container_banner)
    embed.set_thumbnail(url=container_image)
    embed.add_field(name='Reviews', value=review)
    embed.add_field(name='Tags', value=tags)
    #embed.add_field(name='Price', value=price, inline=False)

    await ctx.send(embed=embed)

client.run(key.key)