import discord
from discord.ext import commands
from bot.cogs import CogBase
import asyncio
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

    @commands.command(pass_context=True, no_pm=True, hidden=True)
    async def serverMessage(self, ctx, *messages):
        """Tells the game servers to display a message across the Caribbean"""
        if not self.isAdmin(ctx):
            return
        message = ''
        for m in messages:
            if isinstance(m, str):
                message +='%s ' % m
        say = 'Succesfully sent message: %s' % message
        try:
            response = json.loads(self.main.cluster.systemMessage(message))
            if response['code'] != 200 or response['message'] != 'Success':
                say = 'Failed to send message'
        except:
            pass
        finally:
            await self.bot.say(say)

    @commands.command(pass_context=True, no_pm=True, hidden=True)
    async def holidays(self, ctx):
        """Asks the game servers for the current holiday list"""
        if not self.isDeveloper(ctx):
            return
        say = 'Failed to retrieve holidays'
        try:
            response = json.loads(self.main.cluster.getHolidays())
            if response['code'] == 200 or response['message'] == 'Success':
                say = 'Holidays: %s' % response['holidays']
        except:
            pass
        finally:
            await self.bot.say(say)   

class Moderation(CogBase):
    """Moderator commands"""

    def __init__(self, bot, main):
        super().__init__(bot, main)     

    def __isDevOrStaff(self, ctx):
        return self.isGameMaster(ctx) or self.isDeveloper(ctx)

    @commands.command(pass_context=True, no_pm=True, hidden=True)
    async def kick(self, ctx, member: discord.member):
        """Kicks the user from the Discord server"""
        if not self.__isDevOrStaff(ctx):
            return
        await self.bot.kick(member)
        messages = self.main.config.getValue('moderation.kick_messages', [])
        if len(messages) > 0:
            message = random.choice(messages)
            await self.bot.say(message)

    @commands.command(pass_context=True, no_pm=True, hidden=True)
    async def ban(self, ctx, member : discord.member, messages):
        """Bans the specified member and removes their messages for the last X days"""
        if not self.__isDevOrStaff(ctx):
            return
        await self.bot.ban(member, messages)
        messages = self.main.config.getValue('moderation.ban_messages', [])
        if len(messages) > 0:
            message = random.choice(messages)
            await self.bot.say(message)

    @commands.command(pass_context=True, no_pm=True, hidden=True)
    async def unban(self, ctx, member : discord.member):
        """Unbans the specified member"""
        if not self.__isDevOrStaff(ctx):
            return
        await self.bot.unban(ctx.message.server, member)
        messages = self.main.config.getValue('moderation.unban_messages', [])
        if len(messages) > 0:
            message = random.choice(messages)
            await self.bot.say(message)

    @commands.command(pass_context=True, no_pm=True, hidden=True)
    async def purge(self, ctx, amount):
        """Purges the specified amount of messages from the channel"""
        if not self.__isDevOrStaff(ctx):
            return

        if amount.isdigit():
            amount = int(amount)
        else:
            await self.bot.say('%s is not a valid number!' % amount)
            return 

        deleted = []
        msg = None
        try:
            deleted = await self.bot.purge_from(ctx.message.channel, limit=amount)
            msg = await self.bot.say('Deleted %s messages' % len(deleted))
        except:
            await self.bot.delete_message(ctx.message)
            msg = await self.bot.say('You can only purge messages that are under 14 days old!')

        if msg:
            await asyncio.sleep(5)
            await self.bot.delete_message(msg)

    @commands.command(pass_context=True, no_pm=True, hidden=True)
    async def clear(self, ctx, amount, member : discord.member = None):
        """Clears the specified amount of messages from the channel. 
        This command is not restricted by the age of the message"""
        if not self.__isDevOrStaff(ctx):
            return

        if amount.isdigit():
            amount = int(amount)
        else:
            await self.bot.say('%s is not a valid number!' % amount)
            return 

        deleted = 0
        async for message in client.logs_from(channel, limit=500):
            if i > len(messages):
                break
            message = messages[i]

            if not message:
                continue

            if member and message.author != member:
                continue

            yield from self.bot.delete_message(msg)
            deleted += 1

        msg = await self.bot.say('Deleted %s messages' % deleted)

        if msg:
            await asyncio.sleep(5)
            await self.bot.delete_message(msg)

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

        await self.bot.whisper('The %s server roles are:\n %s' % (ctx.message.server.name, message))

    @commands.command(pass_context=True, hidden=True)
    async def myRoles(self, ctx):
        """Returns the command users roles"""
        if not self.isDiscordDeveloper(ctx):
            return
        message = ''
        for role in ctx.message.author.roles:
            message += '%s: %s\n' % (role.name, role.id)

        await self.bot.whisper('Your %s roles are:\n%s' % (ctx.message.server.name, message))

    @commands.command(pass_context=True, hidden=True)
    async def myId(self, ctx):
        """Returns the requesters Discord id"""
        if not self.isDiscordDeveloper(ctx):
            return
        await self.bot.whisper('Your Discord Id is: %s' % ctx.message.author.id)