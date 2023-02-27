import discord
from discord import app_commands
import json
import datetime
import os
import asyncio
import aiohttp
from discord.ui import View
from discord import ui
from Core import GetStatsEmed
from discord.ext import tasks
from dotenv import load_dotenv
import sqlite3

load_dotenv()
        
intents = discord.Intents.default()
intents.messages = True

def get_channel_id(guild_id):
  try:
    with open('guilds.json', 'r') as file:
      data = json.load(file)
      str_id = str(guild_id)
      channel_id = data[str_id]
  except KeyError:
    print(f'Guild ID {guild_id} not found in the JSON file')
    channel_id = None 
    return channel_id

class aclient(discord.Client):

  def __init__(self):
    super().__init__(intents=intents)
    self.synced = False

  async def on_ready(self):
    await self.wait_until_ready()
    if not self.synced:
      await tree.sync()
      self.synced = True
      update_info.start()
    print(f"Logged as {self.user}")


client = aclient()
tree = app_commands.CommandTree(client)



discord_token = os.environ['discord_token']

@tree.command(name="ping", description="Get Latency")
async def ping(interaction: discord.Interaction):
  latency = round(client.latency * 1000)
  embed = discord.Embed(title='Pong 🏓', description=f'The latency is {latency}')
  await interaction.response.send_message(embed=embed, ephemeral=True)

@tree.command(name="about", description="About the `Magi Stats+`")
async def ping(interaction: discord.Interaction):
  latency = round(client.latency * 1000)
  embed = discord.Embed(title='🗨 About 🗨', description=f'The `Magi Stats+` is bot that connect your server with Coin Magi!')
  embed.add_field(name="👁‍🗨 Future Plans 👁‍🗨", value="1. Let users manage Magi account trought Discordn\n2. Add Coin Magi Faceuet")
  embed.add_field(name="💳 Credits 💳", value="1. [Duino Coin Magi API for fetching stats](https://magi.duinocoin.com/\n2. [tommarek#1245 | Head Developer](https://github.com/tommarekCZE)")
  embed.add_field(name="📃 Source Code 📃", value="[tommarekCZE/CoinMagiStats](https://github.com/tommarekCZE/CoinMagiStats)")
  await interaction.response.send_message(embed=embed, ephemeral=True)

@tree.command(name="setup", description="Setup Statiscics")
async def ping(interaction: discord.Interaction, channel: discord.TextChannel):
  message = await channel.send("Dont delete this message, this message will in 60 seconds update to stats")

  try:
    with open('guilds.json', 'r') as file:
      data = json.load(file)
    
    values = [str(channel.id), str(message.id)]
    data[str(channel.guild.id)] = values

    with open('guilds.json', 'w') as file:
      json.dump(data, file)
  except Exception as e:
    embed = discord.Embed(title='❌Error❌ ', description=f'Error while setup. Report the error below to `tommarek#1245`')
    embed.set_footer(message=e)
    await interaction.response.send_message(embed=embed, ephemeral=True) 
    return

  embed = discord.Embed(title='✔ Succes ✔', description=f'The statistics channel is now {channel}')
  await interaction.response.send_message(embed=embed, ephemeral=True)

@tasks.loop(minutes=1)
async def update_info():
  stats = await GetStatsEmed()

  with open('guilds.json', 'r') as file:
    data = json.load(file)
    for server_id, values in data.items():
      try:
        print(server_id, values[0],  values[1])
        channel = client.get_channel(int(values[0]))
        msg = await channel.fetch_message(int(values[1]))
        await msg.edit(content="" ,embed=stats)
      except:
        pass

client.run(discord_token)