import discord
from discord.ext import commands
from bot.cogs import CogBase
import random
import json

class RPCCommands(CogBase):
    """RPC cluster commands"""

    def __init__(self, bot, main):
        super().__init__(bot, main)

    @commands.command(pass_context=True)
    async def status(self, ctx):
        """Pings the RPC on the UberDOG to confirm its online"""
        if not self.isStaff(ctx):
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

