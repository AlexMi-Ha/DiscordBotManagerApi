import os
import asyncio
import discord
from discord.ext import commands

# ---------------------------

command_symbol = '$'

# --------------------------

intents = discord.Intents.all()
client = commands.Bot(command_prefix=command_symbol,
                      intents=intents)


@client.event
async def on_ready():
    print(f"Logged in as {client.user}")


@client.command()
async def hello(ctx):
    await ctx.send('Hello World!')


@client.command(pass_context=True)
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.message.author.voice.channel
        await channel.connect()

        # disconnect after 5min
        # await asyncio.sleep(5*60)
        # if ctx.voice_client:
        #  await ctx.guild.voice_client.disconnect()
    else:
        await ctx.send("Du bist in keinem Voice Channel du sau hamme :(")


@client.command(pass_context=True)
async def leave(ctx):
    if ctx.voice_client:
        await ctx.guild.voice_client.disconnect()
    else:
        await ctx.send("Bin doch garnicht da :(")

if __name__ == "__main__":
    client.run(os.getenv('SEBI_TOKEN'))
