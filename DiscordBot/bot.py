# bot.py
import os
import random
import discord
from dotenv import load_dotenv
from discord.ext import commands, tasks
import datetime
import csv

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
async def random_game(ctx, *, games):

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



# Kick member from server
@bot.command(name='kick', help='| Kick person from server.')
async def kick(ctx, member : discord.Member, *, reason=None):

    await member.kick(reason=reason)
    await ctx.send(f'Kicked: {member.mention}, for reason: {reason}')

    # members_in_server = []

    # async for memberFetch in ctx.guild.fetch_members():
    #     members_in_server.append(memberFetch.name+memberFetch.discriminator)

    # print(members_in_server)

    # for _ in members_in_server:
    #     if(member in members_in_server):
    #         await member.kick(reason=reason)
    #         await ctx.send(f'Kicked: {member.mention}, for reason: {reason}')
    #     else:
    #         ctx.send(f'{member.mention} not found in server.')


# Ban member from server
@bot.command(name='ban', help='| Ban person from server.')
async def ban(ctx, member : discord.Member, *, reason=None):
    dt = datetime.datetime.now()
    # Append banned users to a .csv file with reason and datetime
    with open('ban.csv', 'a') as f:
        filewriter = csv.writer(f, delimiter=',', quotechar='"')
        filewriter.writerow([member.name+'#'+member.discriminator, reason, dt.strftime("%d-%m-%Y %H:%M:%S")])
        
    await member.ban(reason=reason)
    await ctx.send(f'Banned: {member.mention} for reason: {reason}')

@bot.command(name='unban', help='| Unban person from server.')
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned {user.mention}')
            return


#  Run Client using bot token
bot.run(TOKEN)