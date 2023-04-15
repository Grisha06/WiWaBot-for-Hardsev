import json

import PloudosAPI
import discord
import os
from discord.ext import commands

session = PloudosAPI.login(os.getenv('LOGIN'), os.getenv('PASSWORD'))
print(session.servers().get('shared')[0].serverName)
server = session.servers().get('shared')[0]

bot = commands.Bot(command_prefix=os.getenv('PREFIX'), help_command=None, intents=discord.Intents.all())

debugmode = True

stop_role = 'Выключатель сервера'


def start():
    if not debugmode:
        return server.start()
    else:
        print('server.start()')


@bot.command()
@commands.has_permissions(administrator=True)
async def change_stop_role(ctx: commands.Context, new_role: discord.Role):
    global stop_role
    stop_role = new_role.name
    await ctx.send('Теперь <@&{role}> выключает сервер.'.format(role=new_role.id))

@bot.command()
async def start_server(ctx: commands.Context, *arg):
    await ctx.reply('Дождитесь завершения.')
    try:
        start()
    except Exception as e:
        print(repr(e))
        await ctx.reply(repr(e))
    finally:
        await ctx.reply(
            "Пожалуйста, подождите несколько минут, прежде чем присоединиться к серверу... Сервер прошел через очередь и начал запускаться.")


@bot.command()
async def get_name(ctx: commands.Context, *arg):
    await ctx.send(f"Имя сервера: {server.serverName}")


@bot.command()
@commands.has_role(stop_role)
async def force_stop(ctx: commands.Context, *arg):
    if debugmode:
        print()
        print(ctx.message.guild.roles)
        if discord.utils.find(lambda r: r.name == stop_role, ctx.message.guild.roles) is None:
            await ctx.send(f'Создайте роль **"{stop_role}"**, чтобы сервер можно было остановить.')
            await ctx.send('Сервер был остановлен.')
        return
    s = json.loads(server.force_stop())

    if s.get('error', False) is False:
        await ctx.send('Сервер был остановлен.')
    else:
        await ctx.send(
            f'Что-то не так с остановкой сервера **{server.serverName}**...\nПопробуйте прочитать сообщение об ошибке:\n`{s.get("errorText")}`')


@bot.event
async def on_command_error(ctx, error):
    print(type(error))
    if isinstance(error, discord.ext.commands.errors.MissingRole):
        if discord.utils.find(lambda r: r.name == stop_role, ctx.message.guild.roles) is None:
            await ctx.send(f'Создайте роль **"{error.missing_role}"**, чтобы сервер можно было остановить.')
        else:
            await ctx.send(f'Заимейте роль **"{error.missing_role}"**, чтобы выключать сервер.')
    elif isinstance(error,discord.ext.commands.errors.MissingRequiredArgument):
        await ctx.send(f'Эта команда должна принимать роль.')
    else:
        await ctx.send(f'Произошла непредвиденная ошибка...\nПопробуйте прочитать сообщение:\n`{error}`')


bot.run(os.getenv('TOKEN'))
