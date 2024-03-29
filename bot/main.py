import discord
from discord.ext import commands
from bot.music import Music
from bot import commands as botCommands
from bot.config import ConfigFile
from bot.stream import TwitchMonitor
import xmlrpc.client
import logging
import asyncio
import random
import time
import os

bot = commands.Bot(command_prefix='~', description='')

class PirateBot(object):
    logger = logging.getLogger('PirateBot')

    def __init__(self, configPath):
        self.config = None
        self.cluster = None

        if not os.path.exists(configPath):
            self.logger.warning('Failed to start Pirate Bot; Config: %s does not exist' % configPath)
            return

        try:
            with open(configPath) as configFile:
                self.config = ConfigFile.loadFromJson(configFile)
        except ValueError:
            self.logger.error('Failed to read config file: %s; Invalid JSON' % configPath)
            return

        self.__setupLogging()

        if self.config.getValue('cluster.rpc_enabled', False):
            rpcUrl = self.config.getValue('cluster.rpc_url', '')
            self.logger.info('Connecting to %s...' % rpcUrl)
            self.cluster = xmlrpc.client.ServerProxy(rpcUrl)

        self.__setupBot()

    def __setupLogging(self):
        # check if the log folder exists. If not create it
        log_path = self.config.getValue('logging.log_path', default='logs/')
        if not os.path.exists(log_path):
            os.makedirs(log_path)

        # Generate a log file path is a timestamp suffix
        ltime = time.localtime()
        suffix = '%02d%02d%02d_%02d%02d%02d' % (ltime[0] - 2000, ltime[1], ltime[2], ltime[3], ltime[4], ltime[5])
        log_file = 'log-%s.log' % suffix
        log_path = '%s%s%s' % (log_path, os.sep, log_file)

        log_levels = {
            'info': logging.INFO,
            'debug': logging.DEBUG,
            'warning': logging.WARNING,
            'error': logging.ERROR
        }

        log_level = self.config.getValue('logging.level', default=logging.INFO)
        if log_level not in log_levels:
            print('Invalid log level: %s; Defaulting to %s' % (log_level, logging.INFO))
        log_level = log_levels[log_level]

        formatting = "[%(asctime)s][%(name)s][%(levelname)s] %(message)s"

        formatter = None
        stream = None
        try:
            import colorlog
            stream = colorlog.StreamHandler()
            formatter = colorlog.ColoredFormatter('%(log_color)s' + formatting, log_colors={
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'red,bg_white'
            })
        except:
            formatter = logging.Formatter(formatting)
            stream = logging.StreamHandler()
            raise

        if self.config.getValue('logging.file_logging', default=False):
            logging.basicConfig(level=log_level, filename=log_path, format=formatter)

            stream.setFormatter(formatter)
            logging.getLogger().addHandler(stream)
        else:
            stream.setFormatter(formatter)
            logging.getLogger().setLevel(log_level)
            logging.getLogger().addHandler(stream)

    def __setupBot(self):
        self.twitchMonitor = TwitchMonitor(bot, self)
        bot.pm_help = True

        bot.add_cog(botCommands.General(bot, self))
        bot.add_cog(botCommands.Moderation(bot, self))
        bot.add_cog(botCommands.Developer(bot, self))

        if self.config.getValue('commands.music', False):
            self.logger.debug('Enabling Music commands...')
            bot.add_cog(Music(bot, self))

        if self.config.getValue('commands.rpc', False):
            self.logger.debug('Enabling RPC commands...')
            bot.add_cog(botCommands.Servers(bot, self))

    async def __managePlayingStatus(self):
        await bot.wait_until_ready()
        messages = self.config.getValue('bot.play_messages', None)

        if not messages:
            return

        if len(messages) == 0:
            return

        if isinstance(messages, str):
            await bot.change_presence(game=discord.Game(name=messages))
            return

        while not bot.is_closed:
            message = random.choice(messages)
            await bot.change_presence(game=discord.Game(name=message))
            await asyncio.sleep(60 * random.randint(3, 8))

    def start(self):
        bot.loop.create_task(self.__managePlayingStatus())
        bot.run(self.config.getValue('bot.token', ''))

    @bot.event
    async def on_ready():
        logger = logging.getLogger('PirateBot')
        logger.info('Logged in as Username: %s with userId: %s' % (bot.user.name, bot.user.id))

if __name__ == '__main__':
    PirateBot = PirateBot('./config.json')
    PirateBot.start()