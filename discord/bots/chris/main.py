import discord
from discord.ext import commands
from datetime import datetime, time, timedelta
import asyncio
import plan
import os
from random import randint
from diet import get_diet
from dotenv import load_dotenv

load_dotenv()

client = commands.Bot(command_prefix="////")


@client.event
async def on_ready():
    print(f"Logged in as {client.user}")


@client.command()
async def ping(ctx):
    await ctx.send(f'**Pong!** Latency: {round(client.latency * 1000)}ms')


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
        await ctx.send("Du bist in keinem Voice Channel :(")


@client.command(pass_context=True)
async def leave(ctx):
    if ctx.voice_client:
        await ctx.guild.voice_client.disconnect()
    else:
        await ctx.send("Bin doch garnicht da :(")


channel_id = 1001037382935658597


async def background_task():
    while True:
        seconds_until_target = randint(60, 60 * 60 * 24)
        print("Sleeping for " + str(seconds_until_target / 60 / 60) + " hours")
        await asyncio.sleep(seconds_until_target)
        await hallo_chris(client.get_channel(channel_id))


@client.event
async def on_message(message):
    if message.author != client.user:
        if "hallo chris" in str(
                message.content).lower() or "hallochris" in str(
                    message.content).lower():
            await hallo_chris(message.channel)
        if "diet" in str(message.content).lower():
            await my_diet(message)


async def my_diet(message):
    mes = await message.channel.send("fetching diet...")
    diet = "Heute gegessen:\n" + get_diet()
    await mes.edit(content=diet)


async def hallo_chris(channel):
    await client.wait_until_ready()
    await channel.send("Hallo Chris!")


if __name__ == "__main__":
    # client.loop.create_task(background_task())
    client.run(os.getenv('CHRIS_TOKEN'))
    pass
