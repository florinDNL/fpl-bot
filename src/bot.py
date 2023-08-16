import os
import discord
import fpl_gw
import time

from discord.ext import commands, tasks
from discord.utils import get
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(intents=intents, command_prefix='++')


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    checkDeadline.start()

async def sendReminder(hoursLeft, gw):
    role = None
    fantasy_channel = None
    for guild in bot.guilds:
        role = get(guild.roles, name='Fantasy Football Addicts Anonymous')
        for channel in guild.channels:
            if channel.name == 'fantazoo':
                fantasy_channel = channel

    await fantasy_channel.send(f'<@&{role.id}> {hoursLeft} hours until {gw} deadline.')


@tasks.loop(minutes=500)
async def checkDeadline():
    ngw = None
    gameweeks = await fpl_gw.getGameWeeks()

    for gw in gameweeks:
        if gw.is_next:
            ngw = gw
    
    currentTime = int(time.time())
    deadlineEpoch = int(ngw.deadline_time_epoch)
    hoursLeft = (deadlineEpoch - currentTime) // 3600

    if hoursLeft <= 24:
        await sendReminder(hoursLeft=hoursLeft, gw=ngw.name)


@commands.has_role('Furries')                
@bot.command(name='remindertest')
async def reminderTest():
    await sendReminder(hoursLeft='X', gw='Y')

bot.run(TOKEN)