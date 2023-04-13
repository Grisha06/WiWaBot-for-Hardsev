import random

import discord
from discord.ext import commands

config = {
    'token': 'MTA5NjE1ODg2NDM4NDIxMzEwNA.GtUtuZ.mqq44K_idActK5XtSTEbKPGJ0Lk4ZFUJuwzHSs',
    'prefix': '$',
    'id': 1096158864384213104,
}

bot = commands.Bot(command_prefix=config['prefix'],intents=discord.Intents.default())


@bot.command()
async def rand(ctx, *arg):
    await ctx.reply(random.randint(0, 100))


bot.run(config['token'])
