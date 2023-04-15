import json

import PloudosAPI
import disnake
from disnake.ext import commands
from passwords_compiled import config

session = PloudosAPI.login(config.get('login'), config.get('password'))
print(session.servers().get('shared')[0].serverName)
server = session.servers().get('shared')[0]

bot = commands.Bot(command_prefix=config['prefix'], help_command=None, intents=disnake.Intents.all())

debugmode = True

stop_role='Выключатель сервера'


def start():
    if not debugmode:
        return server.start()
    else:
        print('server.start()')

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
    await ctx.reply(f"Имя сервера: {server.serverName}")


@bot.command()
@commands.has_role("Выключатель сервера")
async def force_stop(ctx: commands.Context, *arg):
    print()
    print(ctx.message.guild.roles)
    if disnake.utils.find(lambda r: r.name == stop_role, ctx.message.guild.roles) is None:
        await ctx.reply(f'Создайте роль **"{stop_role}"**, чтобы сервер можно было остановить.')
    return
    if debugmode:
        await ctx.reply('Сервер был остановлен.')
        return
    s = json.loads(server.force_stop())

    if s.get('error', False) is False:
        await ctx.reply('Сервер был остановлен.')
    else:
        await ctx.reply(
            f'Что-то не так с остановкой сервера **{server.serverName}**...\nпопробуйте прочитать сообщение об ошибке:\n`{s.get("errorText")}`')


bot.run(config['token'])
