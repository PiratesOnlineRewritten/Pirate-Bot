import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='~', description='')

class PirateBot(object):

    def __init__(self):
        bot.remove_command("help")

    def start(self):
        print('====================================')
        print('Starting Pirate Bot...')
        print('====================================')
        bot.run('MzU0NDQ0NjA5NDM2MjU0MjA5.DK26Mg.rc4Of9R-pA_26ckWPa14991a5dI')

    @bot.event
    async def on_ready():
        print('Username: %s' % bot.user.name)
        print('UserId: %s' % bot.user.id)
        print('------------------------------------')
        print('Ready!')

    @bot.event
    async def joined(member : discord.member):
        """Says when a member joined."""        
        await bot.say('Welcome to the Discord server {0.name}!'.format(member))

if __name__ == '__main__':
    PirateBot = PirateBot()
    PirateBot.start()