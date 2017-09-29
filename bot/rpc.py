import discord
from discord.ext import commands
import random
import json

class RPCCommands(object):
    """RPC cluster commands"""

    def __init__(self, bot, main):
        self.bot = bot
        self.main = main

    @commands.command()
    async def status(self):
        """Pings the RPC on the UberDOG to confirm its online"""
        say = 'The servers are currently down.'
        try:
            response = json.loads(self.main.cluster.ping('PONG'))
            if (response['code'] == 200 and response['message'] == 'Success'):
                say = 'The servers are currently online!'
        except:
            pass
        finally:
            await self.bot.say(say)

