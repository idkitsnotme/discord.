import discord
import os
import random
from discord.ext import commands

TOKEN = os.getenv("DISCORD_TOKEN") 

intents = discord.Intents.default()
intents.members = True          
intents.message_content = True   

bot = commands.Bot(command_prefix='@', intents=intents)

server_cache = {}

@bot.event
async def __on_ready__():
    print(f'Logged in as {bot.user}')

@bot.command()
async def someone(ctx, *, user_input: str = ""):
    server_id = ctx.guild.id

    # 1. Build the list of humans only
    if server_id not in server_cache or not server_cache[server_id]:
        server_cache[server_id] = [m.mention for m in ctx.guild.members if not m.bot]

    # 2. Pick EXACTLY one person
    if server_cache[server_id]:
        rando = random.choice(server_cache[server_id])
        
        # 3. Clean the user_input to make sure no extra pings snuck in
        # We only send the one 'rando' we picked
        await ctx.send(f"{rando} {user_input}")
    else:
        await ctx.send("I can't find anyone to ping!")

# Keep the list updated
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
