import discord
from discord import app_commands
import json
from discord.ui import View
from discord import ui
from Core import GetStatsEmed
from discord.ext import tasks
        
intents = discord.Intents.default()
intents.messages = True
intents.members = True

def getModalData(filepath):
  with open(f'modals/{filepath}.json') as json_file:
    data = json.load(json_file)
  return data

class TestModal(ui.Modal):
  def __init__(self, title: str, description: str):
    super().__init__(title=title)
    self.description = description

  async def on_submit(self, interaction: discord.Integration):
    embed = discord.Embed(title='✅ Succes ✅', description=f'{self.description}')
    await interaction.response.send_message(embed=embed, ephemeral=True)

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
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Coin Magi Stats"))
    print(f"Logged as {self.user}")


client = aclient()
tree = app_commands.CommandTree(client)



discord_token = "MTA3OTg0MDg2MDU3MDY2OTE2Nw.GPqR1A.8uU92vh4VVax0KHihzTRYfAG-wZk6TW49oM_Qg"

@tree.command(name="ping", description="Get Latency")
async def ping(interaction: discord.Interaction):
  latency = round(client.latency * 1000)
  embed = discord.Embed(title='Pong 🏓', description=f'The latency is {latency}')
  await interaction.response.send_message(embed=embed, ephemeral=True)

@tree.command(name="changelog", description="Dev Command")
async def changelog(interaction: discord.Interaction):
  if not interaction.user.id == 691007640007868487:
    embed = discord.Embed(title='❌Error❌', description=f'Error while setup, Missing permissions')
    embed.set_footer(text=f"{interaction.user} is not Developer")
    await interaction.response.send_message(embed=embed, ephemeral=True) 
    return
  
  data = getModalData("changelogSubmit")
  modal = TestModal(data["ModalName"], data["ModalResponse"])
  for field in data['fields']:
    text_input = ui.TextInput(label=field['label'], style= discord.TextStyle[field['style']], placeholder = field['placeholder'], required = field['required'])
    modal.add_item(text_input)

  await interaction.response.send_modal(modal)
  await modal.wait()
  name = modal.children[0].value
  description = modal.children[1].value

  embed = discord.Embed(title=name, description=description, color=0x00ffee)
    
  for guild in client.guilds:
    embed.set_footer(text=f"Sent from {guild.name}")
    await guild.owner.send(embed=embed)  


@tree.command(name="about", description="About the Magi Stats+")
async def about(interaction: discord.Interaction):
  latency = round(client.latency * 1000)
  embed = discord.Embed(title='🗨 About 🗨', description=f'The `Magi Stats+` is bot that connect your server with Coin Magi!')
  embed.add_field(name="👁‍🗨 Future Plans 👁‍🗨", value="1. Let users manage Magi account trought Discordn\n2. Add Coin Magi Faceuet")
  embed.add_field(name="💳 Credits 💳", value="1. [Duino Coin Magi API for fetching stats](https://magi.duinocoin.com/\n2. [tommarek#1245 | Head Developer](https://github.com/tommarekCZE)")
  embed.add_field(name="📃 Source Code 📃", value="[tommarekCZE/CoinMagiStats](https://github.com/tommarekCZE/CoinMagiStats)")
  await interaction.response.send_message(embed=embed, ephemeral=True)

@tree.command(name="setup", description="Setup Statiscics")
async def setup(interaction: discord.Interaction, channel: discord.TextChannel):
  if not interaction.channel.permissions_for(interaction.user).administrator:
    embed = discord.Embed(title='❌Error❌', description=f'Error while setup, Missing permissions')
    embed.set_footer(text=f"`{interaction.user}` does not have administrator permissions")
    await interaction.response.send_message(embed=embed, ephemeral=True) 
    return

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
    embed.set_footer(text=e)
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