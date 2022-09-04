import discord
from discord.ext import commands
from datetime import datetime, time, timedelta
import asyncio
import plan
import os

client = commands.Bot(command_prefix="///")


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


@client.command()
async def meals(ctx):
    await called_once_a_day(ctx)


WHEN = time(7 - 2, 0, 0)
channel_id = 999971580773924936


@client.command()
async def currenttime(ctx):
    await ctx.send(datetime.now())
    await ctx.send("active at: " + str(WHEN))


async def background_task():
    now = datetime.now()
    if now.time() > WHEN:
        tomorrow = datetime.combine(now.date() + timedelta(days=1), time(0))
        seconds = (tomorrow - now).total_seconds()
        await asyncio.sleep(seconds)
    while True:
        now = datetime.now()
        target_time = datetime.combine(now.date(), WHEN)
        seconds_until_target = (target_time - now).total_seconds()
        await asyncio.sleep(seconds_until_target)
        await called_once_a_day(client.get_channel(channel_id))
        tomorrow = datetime.combine(now.date() + timedelta(days=1), time(0))
        seconds = (tomorrow - now).total_seconds()
        await asyncio.sleep(seconds)


async def called_once_a_day(channel):
    await client.wait_until_ready()
    meals = plan.get_meals()
    await channel.send("Heute bei Mike:\n")
    for meal in meals:
        await channel.send(meal.name + ":\n" + meal.meal + "\n" + meal.price +
                           "\n\n")


if __name__ == "__main__":
    # client.loop.create_task(background_task())
    client.run(os.getenv('MIKE_TOKEN'))
    pass
