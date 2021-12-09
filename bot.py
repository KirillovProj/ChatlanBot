import discord
import random
from discord.ext import commands
from config import TOKEN
from discord_slash import SlashCommand, SlashContext
import db
import time
import os

intents = discord.Intents.default()
intents.members = True
chatlan_bot = commands.Bot(command_prefix='?', intents=intents)
slash = SlashCommand(chatlan_bot, sync_commands=True)
my_guild = 323195968780763149


@chatlan_bot.event
async def on_ready():
    guild = chatlan_bot.get_guild(my_guild)
    for member in guild.members:
        for role in member.roles:
            if role.name in ['свинки', 'папа свин']:
                try:
                    db.add_to_game(member.id)
                except TypeError:
                    print(f'Couldn\'t add user with id {member.id} to database')


@slash.slash(name='zhmak', guild_ids=[my_guild])
async def send_pig_photo(ctx: SlashContext):
    await ctx.send(db.get_pigs(random.randint(1, 53)))


@slash.slash(name='agent', guild_ids=[my_guild])
async def game(ctx: SlashContext):
    if db.check_not_played_today():
        try:
            players = db.get_players()
            winner = players[random.randint(0, len(players) - 1)]
            await ctx.send(db.get_phrase(random.randint(1, 24), 'prelude'))
            time.sleep(1)
            await ctx.send(f'{db.get_phrase(random.randint(1, 24), "final")} <@{winner}>!')
            db.reg_game(winner)
        except TypeError:
            await ctx.send(os.environ['ON_BROKEN'])
    else:
        await ctx.send(os.environ['ON_ONCE'])


@slash.slash(name='top_agents', guild_ids=[my_guild])
async def top_winners(ctx: SlashContext):
    stats = db.get_stats()
    message = ''
    num = 1
    for i in stats:
        message += f'{num}. <@{i[0]}> — {i[1]}\n'
        num += 1
    await ctx.send(message)


@slash.slash(name='chatlan_help', guild_ids=[my_guild])
async def help_info(ctx: SlashContext):
    await ctx.send(os.environ['ON_HELP'])


chatlan_bot.run(TOKEN)
