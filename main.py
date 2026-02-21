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
last_picked = {} # Tracks the last person picked per server

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command()
async def someone(ctx, *, user_input: str = ""):
    server_id = ctx.guild.id

    # 1. Build/Refresh the list
    if server_id not in server_cache or not server_cache[server_id]:
        server_cache[server_id] = [m.mention for m in ctx.guild.members if not m.bot]

    # 2. Filter out the last person picked so we don't repeat
    current_pool = server_cache[server_id].copy()
    if server_id in last_picked and len(current_pool) > 1:
        if last_picked[server_id] in current_pool:
            current_pool.remove(last_picked[server_id])

    # 3. Pick from the new pool
    if current_pool:
        rando = random.choice(current_pool)
        last_picked[server_id] = rando # Remember this person for next time
        
        await ctx.send(f"{rando} {user_input}")
    else:
        await ctx.send("The list is empty!")

# Cache update events (Keep these)
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
