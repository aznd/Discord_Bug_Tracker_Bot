import discord
from discord.ext import commands
import os
import logging
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.WARNING)

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix="!", intents=intents)


@commands.has_role("Dev")
@client.command()
async def load(ctx, extension):
    await client.load_extension(f"cogs.{extension}")
    await ctx.send("Loaded cog.")


@commands.has_role("Dev")
@client.command()
async def unload(ctx, extension):
    await client.unload_extension(f"cogs.{extension}")
    await ctx.send("Unloaded cog.")


@commands.has_role("Dev")
@client.command()
async def reload(ctx, extension):
    try:
        await client.unload_extension(f"cogs.{extension}")
        await client.load_extension(f"cogs.{extension}")
        await ctx.send("Reloaded cog.")
    except Exception as e:
        print(e)


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Command not found.")
    elif isinstance(error, commands.MissingRole):
        await ctx.send("You do not have the required role to use this command.")


@client.event
async def on_ready():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await client.load_extension(f"cogs.{filename[:-3]}")
    logging.warning("Bot online.")


client.run(TOKEN)
