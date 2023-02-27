import aiohttp
import discord

async def GetStatsEmed():
    async with aiohttp.ClientSession() as session:
      url = 'https://magi.duinocoin.com/statistics'
      async with session.get(url=url) as response:
        if not response.status == 200:
          embed = discord.Embed(title="ERROR", description=f"Error while fetching data from `{url}`", color=0xff0000)
          embed.set_footer(text=f"Response status: {response.status}")
          print(f"embed {response.status}")
          return embed
               
        data = await response.json()

        print(data['result']['blocks'])
        print(data['result']['blocktx'])
        print(data['result']['connections'])
        print(data['result']['difficulty']['pos'])
        print(data['result']['difficulty']['pow'])
        print(data['result']['hashrate'])
        print(data['result']['hours_to_stake'])
        print(data['result']['price']['btcpop'])
        print(data['result']['price']['ducoexchange'])
        print(data['result']['price']['fluffy'])
        print(data['result']['price']['max'])
        print(data['result']['price']['moondex'])
        print(data['result']['reward'])
        print(data['result']['stake_interest'])
        print(data['result']['total_balance'])
        print(data['result']['users'])
        print(data['success'])

        embed = discord.Embed(title="Coin Magi Stats")

        embed.add_field(name="Total Hashrate ⛏", value=f"{data['result']['hashrate']} H/s")
        embed.add_field(name="Total Blocks 🧱", value=f"{data['result']['blocks']}")
        embed.add_field(name="Total Users 👪", value=f"{data['result']['users']}")
        embed.add_field(name="Total Balance :chart_with_upwards_trend:", value=f"{data['result']['total_balance']} XMG")
        embed.add_field(name="Difficulty - POS 🤝", value=f"{data['result']['difficulty']['pos']}")
        embed.add_field(name="Difficulty - POW 💪", value=f"{data['result']['difficulty']['pow']}")
        embed.add_field(name="Stake Interest 🧰", value=f"{data['result']['stake_interest']}")
        embed.add_field(name="Hours to stake 🕐", value=f"{data['result']['hours_to_stake']}")
        embed.add_field(name="Price - FluffySwap ☁️", value=f"{float(data['result']['price']['fluffy'])} $")
        embed.add_field(name="Price - DUCO Exchange ᕲ", value=f"{(float(data['result']['price']['ducoexchange']))} $")
        embed.add_field(name="Price - BTCpop ₿", value=f"{float(data['result']['price']['btcpop'])} $")
        embed.add_field(name="Price - Moondex 🌙", value=f"{float(data['result']['price']['moondex'])} $")

        embed.set_footer(text=f"This message get updated every 60 Seconds")

        return embed