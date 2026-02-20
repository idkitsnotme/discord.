import discord
import os
import random
from discord.ext import commands

# Railway will look for this name in the "Variables" tab
TOKEN = os.getenv("DISCORD_TOKEN") 

intents = discord.Intents.default()
intents.members = True          # Needs to be ON in Dev Portal
intents.message_content = True   # Needs to be ON in Dev Portal

# Prefix is '@', so you type '@someone'
bot = commands.Bot(command_prefix='@', intents=intents)

# This is the "Guest List" we talked about
server_cache = {}

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command()
async def someone(ctx):
    server_id = ctx.guild.id

    # If we don't have a list for this server yet, make one
    if server_id not in server_cache:
        # Puts everyone who isn't a bot into the list
        server_cache[server_id] = [m.mention for m in ctx.guild.members if not m.bot]

    if server_cache[server_id]:
        rando = random.choice(server_cache[server_id])
        await ctx.send(f"I choose you: {rando}")
    else:
        await ctx.send("The server seems empty... or I don't have permission to see members!")

# This keeps the guest list updated so you don't ping people who left
@bot.event
async def on_member_join(member):
    if member.guild.id in server_cache and not member.bot:
        server_cache[member.guild.id].append(member.mention)

@bot.event
async def on_member_remove(member):
    if member.guild.id in server_cache:
        try:
            server_cache[member.guild.id].remove(member.mention)
        except ValueError:
            pass 

bot.run(TOKEN)