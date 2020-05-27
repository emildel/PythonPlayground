# bot.py
import os
import random
import discord
from dotenv import load_dotenv
from discord.ext import commands, tasks

# load_dotenv() loads environment variables from .env file
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

# Client is an object that represents connection to Discord.
client = discord.Client()

# Code that gets run when bot set up
@bot.event
async def on_ready():

    print(
        f'{bot.user.name} has connected to Discord!'
    )

# Send message to new member in their DMs
@client.event
async def on_member_join(member):
    # Create a DM channel to new member
    await member.create_dm()
    # Send message in DM channel just created to new member
    # await ensures that previous line is complete before running next line
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to my Discord server!'
    )

# Pick a random game to play based on user input. 
# Games must be seperated by comma only. Eg, BF1,warzone,minecraft
@bot.command(name='pickgame', help='| Pick a random game. Games must be seperated by comma only.')
async def random_game(ctx, games):

    list_of_games = games.split(',')

    # Randomly pick one game from list
    response = random.choice(list_of_games)
    await ctx.send(f'Randomly picked: {response}')


@client.event
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise

@bot.command(name='kick', help='| Kick person from server.')
async def kick(ctx, member : discord.Member, *, reason=None):
    await member.kick(reason=reason)

@bot.command(name='ban', help='| Ban person from server.')
async def ban(ctx, member : discord.Member, *, reason=None):
    await member.ban(reason=reason)

#  Run Client using bot token
bot.run(TOKEN)