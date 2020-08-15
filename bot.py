import discord
import linecache2
import random
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

            games += name + " | Original Price - " + original_price + " | Discounted Price - " + discount_price + "\n"
        await ctx.send("```" + games + "```")

    else:
        await ctx.send("Please enter valid numbers from 1 to " + str(total_games))

        
client.run(key.key)