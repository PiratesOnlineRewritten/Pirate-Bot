import discord
from discord.ext import commands
from bot.cogs import CogBase
import random

class BasicCommands(CogBase):
    """General commands"""

    def __init__(self, bot, main):
        super().__init__(bot, main)

    @commands.command()
    async def roll(self, dice):
        """Rols a dice in the NdN format."""
        try:
            rolls, limit = map(int, dice.split('d'))
        except Exception:
            await self.bot.say('Format has to be in NdN!')

        result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
        await self.bot.say(result)        


class DeveloperCommands(CogBase):
    """Developer commands"""

    def __init__(self, bot, main):
        super().__init__(bot, main)

    @commands.command(pass_context=True)
    async def roles(self, ctx):
        """Returns the Discord server roles"""
        if not self.isDiscordDeveloper(ctx):
            return
        message = ''
        for role in ctx.message.server.roles:
            message += '%s: %s\n' % (role.name, role.id)

        await self.bot.say(message)

    @commands.command(pass_context=True)
    async def myRoles(self, ctx):
        """Returns the command users roles"""
        if not self.isDiscordDeveloper(ctx):
            return
        message = ''
        for role in ctx.message.author.roles:
            message += '%s: %s\n' % (role.name, role.id)

        await self.bot.say(message)               

    @commands.command(pass_context=True)
    async def myId(self, ctx):
        """Returns the requesters Discord id"""
        if not self.isDiscordDeveloper(ctx):
            return
        await self.bot.say(ctx.message.author.id)