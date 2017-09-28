import discord
from discord.ext import commands
import random

class BasicCommands(object):
    """General commands"""

    def __init__(self, bot, main):
        self.bot = bot
        self.main = main

    @commands.command()
    async def roll(self, dice):
        """Rols a dice in the NdN format."""
        try:
            rolls, limit = map(int, dice.split('d'))
        except Exception:
            await self.bot.say('Format has to be in NdN!')

        result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
        await self.bot.say(result)        
