import discord
from discord.ext import commands

class CogBase(object):
    """Base class for all cogs"""

    def __init__(self, bot, main):
        self.bot = bot
        self.main = main

    def isAdmin(self, ctx):
        admin = False
        if not hasattr(ctx.message.author, 'roles'):
            return False
        for role in ctx.message.author.roles:
            if role.permissions.administrator:
                admin = True
                break
        return admin

    def hasRole(self, ctx, roleId, allowAdmin=True):
        return (str(roleId) in [str(y.id) for y in ctx.message.author.roles]) or (self.isAdmin(ctx) and allowAdmin)

    def isStaff(self, ctx):
        discordStaffId = self.main.config.getValue('roles.staff', 0)
        return self.hasRole(ctx, discordStaffId)

    def isGameMaster(self, ctx):
        discordGMId = self.main.config.getValue('roles.gameMaster', 0)
        discordLGMId = self.main.config.getValue('roles.leadGameMaster', 0)
        return self.hasRole(ctx, discordGMId) or self.hasRole(discordLGMId)

    def isDeveloper(self, ctx):
        discordDeveloperId = self.main.config.getValue('roles.developer', 0)
        discordLDeveloperId = self.main.config.getValue('roles.leadDeveloper', 0)
        return self.hasRole(ctx, discordDeveloperId) or self.hasRole(discordLDeveloperId)

    def isDiscordDeveloper(self, ctx):
        discordDevId = self.main.config.getValue('roles.discordDeveloper', 0)
        return self.hasRole(ctx, discordDevId)