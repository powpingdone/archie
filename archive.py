#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio as asio
import aiosqlite as sqlite
import mimetypes 

# This lock is to make sure sqlite doesn't create extra work by having
# a file that is already cached (or in the process of being cached)
# but hasn't been loaded into the db cache, ie. in the case of spam.
MEDIALOCK = asio.Lock()

# Create a dict with post info for easy sqlite insertion.
async def textparse(message):
    return dict(
        date=str(message.created_at.strftime('%m/%-d/%Y %H:%-M:%-S')),
        post=''.join(message.content),
        user='{0.author.name}#{0.author.discriminator}'.format(message),
        channel=message.channel.name
    )

async def processAttach(attachs):
    async for file, url in attachs:
        async with MEDIALOCK:
            db = sqlite.connect('posts.db')
            files = db.execute
        



# Grabs all possible media from the message, downloads it, converts
# them into better formats, and then adds them to the embed param 
# in the format "'original src url' 'archive link/filename';"
async def mediaparse(message):
    attach = [[attach.filename, attach.url]
            for attach in message.attachments]
    fullpost = ''.join(message.content).split()


# THE main archival function. Takes the content of the message and
# returns a parseable dictionary for sqlite.
async def archive(message):
    post = asio.Task(textparse(message))
    media = asio.Task(mediaparse(message))
    await post
    await media
    post = post.result()
    media = media.result()
    return {**post, **media} # merge both into single dict