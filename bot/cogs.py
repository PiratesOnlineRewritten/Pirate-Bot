import discord
from discord.ext import commands

class CogBase(object):
    """Base class for all cogs"""

    def __init__(self, bot, main):
        self.bot = bot
        self.main = main

    def isAdmin(self, ctx):
        admin = False
        for role in ctx.message.author.roles:
            if role.permissions.administrator:
                admin = True
        return admin

    def isDiscordDeveloper(self, ctx):
        discordDevId = self.main.config.getValue('roles.discordDeveloper', 0)
        discordDevRole = discord.utils.get(ctx.message.server.roles, id=discordDevId)
        
        # Check if the user is a server admin
        admin = self.isAdmin(ctx)
        return (discordDevRole in ctx.message.author.roles) or admin