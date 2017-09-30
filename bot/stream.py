import discord
from discord.ext import commands
from bot.cogs import CogBase
import asyncio
import requests
import logging
import random
import json

class TwitchMonitor(CogBase):
    logger = logging.getLogger('TwitchMonitor')

    def __init__(self, bot, main):
        super().__init__(bot, main)
        self.alreadyBroadcasted = False
        self.bot.loop.create_task(self.__checkForBroadcast())

    async def __checkForBroadcast(self):

        self.logger.info('Starting Twitch monitor...')

        while True:
            self.logger.debug('Checking stream status...')

            url = 'https://api.twitch.tv/kraken/streams'
            client_id = self.main.config.getValue('twitch.client_id', '')
            channel_name = self.main.config.getValue('twitch.channel_name', '')

            channel_id = self.main.config.getValue('twitch.announcement_channel', '')
            if not channel_id:
                self.notify.warning('Failed to perform Twitch monitor; Announcement channel not defined')
                break

            news_channel = self.bot.get_channel(channel_id)
            if not news_channel:
                await asyncio.sleep(5)
                continue

            params = {
                'client_id': client_id,
                'channel': channel_name,
                'limit': 1
            }

            request = requests.get(url, params=params)
            body = request.json()
            streams = body['streams']

            if len(streams) == 0:
                return

            stream = streams[0]
            if 'stream_type' in stream:
                if stream['stream_type'] == 'live':

                    if self.alreadyBroadcasted:
                        return

                    self.alreadyBroadcasted = True
                    channel_url = 'https://go.twitch.tv/%s' % channel_name
                    self.logger.info('%s is live on Twitch!' % channel_name)
                    await self.bot.send_message(news_channel, '@everyone Ahoy Mateys! %s is live on Twitch! Come join us for a live stream!\n%s' % (channel_name, channel_url))
                else: 
                    self.alreadyBroadcasted = False
            else:
                self.alreadyBroadcasted = False

            await asyncio.sleep(20)