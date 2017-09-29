import discord
from discord.ext import commands
from bot.cogs import CogBase
import random
import json

class General(CogBase):
    """General commands"""

    def __init__(self, bot, main):
        super().__init__(bot, main)

    @commands.command(description="Rolls a dice in the NdN format.")
    async def roll(self, dice, no_pm=True):
        """Rolls a dice in the NdN format."""
        try:
            rolls, limit = map(int, dice.split('d'))
        except Exception:
            await self.bot.say('Format has to be in NdN!')

        result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
        await self.bot.say(result)

    @commands.command(description='For when you wanna settle the score some other way', no_pm=True)
    async def choose(self, *choices):
        """Chooses between multiple choices."""
        await self.bot.say(random.choice(choices))

    @commands.command(pass_context=True, no_pm=True)
    async def cursed(self, ctx, member : discord.Member):
        """Checks if the user is cursed!"""
        msgs = ['{0.name} has an evil curse!', '{0.name} does not have an evil curse.']
        await self.bot.say(random.choice(msgs).format(member))

class Servers(CogBase):
    """RPC cluster commands"""

    def __init__(self, bot, main):
        super().__init__(bot, main)

    @commands.command(pass_context=True, no_pm=True)
    async def status(self, ctx):
        """Pings the game servers to see if they are online"""
        if not self.isStaff(ctx):
            await self.bot.say('Sorry, Only staff members can use this command')
            return
        say = 'The servers are currently down.'
        try:
            response = json.loads(self.main.cluster.ping('PONG'))
            if (response['code'] == 200 and response['message'] == 'Success'):
                say = 'The servers are currently online!'
        except:
            pass
        finally:
            await self.bot.say(say)

class Developer(CogBase):
    """Developer commands"""

    def __init__(self, bot, main):
        super().__init__(bot, main)

    @commands.command(pass_context=True, hidden=True)
    async def roles(self, ctx):
        """Returns the Discord server roles"""
        if not self.isDiscordDeveloper(ctx):
            return
        message = ''
        for role in ctx.message.server.roles:
            message += '%s: %s\n' % (role.name, role.id)

        await self.bot.say(message)

    @commands.command(pass_context=True, hidden=True)
    async def myRoles(self, ctx):
        """Returns the command users roles"""
        if not self.isDiscordDeveloper(ctx):
            return
        message = ''
        for role in ctx.message.author.roles:
            message += '%s: %s\n' % (role.name, role.id)

        await self.bot.say(message)               

    @commands.command(pass_context=True, hidden=True)
    async def myId(self, ctx):
        """Returns the requesters Discord id"""
        if not self.isDiscordDeveloper(ctx):
            return
        await self.bot.say(ctx.message.author.id)