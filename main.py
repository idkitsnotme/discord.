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
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command()
async def someone(ctx, *, message: str = ""):
    server_id = ctx.guild.id

    # Build cache if it doesn't exist
    if server_id not in server_cache:
        server_cache[server_id] = [m.mention for m in ctx.guild.members if not m.bot]

    if server_cache[server_id]:
        rando = random.choice(server_cache[server_id])
        
        # If the user added text (like "farted"), it adds it after the mention
        if message:
            await ctx.send(f"{rando} {message}")
        else:
            # Default response if you just type @someone with no text
            await ctx.send(f"I choose you: {rando}")
    else:
        await ctx.send("I couldn't find anyone in the guest list!")

# Cache update events (Keep these the same as before)
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
