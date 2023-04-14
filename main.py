import json
import subprocess

import PloudosAPI
import disnake
from disnake.ext import commands

session = PloudosAPI.login("NezertorcheaT", "Batman06psps")
server = session.get_server(0)

config = {
    'token': 'MTA5NjE1ODg2NDM4NDIxMzEwNA.GtUtuZ.mqq44K_idActK5XtSTEbKPGJ0Lk4ZFUJuwzHSs',
    'prefix': '!',
    'id': 1096158864384213104,
}

bot = commands.Bot(command_prefix=config['prefix'], help_command=None, intents=disnake.Intents.all())


@bot.command()
async def start_server(ctx: commands.Context, *arg):
    try:
        server.start()
    except Exception as e:
        print(repr(e))
        await ctx.reply(repr(e))
    finally:
        await ctx.reply("Done!")


@bot.command()
async def force_stop(ctx: commands.Context, *arg):
    s = json.loads(server.force_stop())

    if s.get('error', True) is False:
        await ctx.reply('is done')
    else:
        await ctx.reply(
            f'something wrong with sopping **{server.serverName}** server...\ntry to read error message:\n`{s.get("errorText")}`')


bot.run(config['token'])
