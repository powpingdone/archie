#!/usr/bin/env python
# -*- coding: utf-8 -*-

import discord
from datetime import datetime

client = discord.Client()
day = datetime.now().day

@client.event
async def on_ready():
    print('{0.user} ready!'.format(client))

@client.event
async def on_message(message):
    if day != datetime.now().day:
        print('day change, archive')
    if message.author == client.user:
        return

    if message.content.startswith(''):
        print(message.content)

messages = []
client.run(open('botid').read().strip())
