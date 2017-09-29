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
                break
        return admin

    def hasRole(self, ctx, roleId, allowAdmin=True):
        discordRole = discord.utils.get(ctx.message.server.roles, id=roleId)
        return (discordRole in ctx.message.author.roles) or (self.isAdmin(ctx) and allowAdmin)

    def isDiscordDeveloper(self, ctx):
        discordDevId = self.main.config.getValue('roles.discordDeveloper', 0)
        return self.hasRole(ctx, discordDevId)

    def isStaff(self, ctx):
        discordStaffId = self.main.config.getValue('roles.staff', 0)
        return self.hasRole(ctx, discordStaffId)