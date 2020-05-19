#!/usr/bin/env python
# -*- coding: utf-8 -*-

import discord
import os
import asyncio as asio
import aiosqlite as sqlite

client = discord.Client()

# This is called when the bot is connected and ready to comm with discord.
@client.event
async def on_ready():
    print('Got {0.user} for username. Ready.'.format(client))

# This is main() for those who are impatient. it
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith('-++'): # its a command
        print(message.content,'command')
    else: # do regular archival
        print(message.content)
        
# This creates the posts.db file which stores every single post, starting from
# execution. The table created from this stores the posts with the following 
# keys:
# TEXT date: the date of the post
# TEXT post: the text content of the post
# TEXT user: the username of the user who made the post
# TEXT embed: the embeds/files of the post, should be semicolon delimited 
#   links to where the embeds are
# TEXT channel: the channel that the post was posted in
async def genpostsdb():
    print('posts.db does not exist, creating...', end='')
    async with sqlite.connect('posts.db') as temp:
        asio.run(temp.execute('''CREATE TABLE posts
                     (date text, post text, user text,
                      embed text, channel text)'''))
        asio.run(temp.commit())
    print('done!')

# This creates the hashes.db files which prevents duplicate files from being
# uploaded or stored. There are four types of files being hashed: audio,
# video, images, and generic files. Each filetype hash is done differently
# and is referenced in their respective funcs.
# TODO: show the funcs in their respective files
async def genhashesdb():
    print('hashes.db does not exist, creating...', end='')
    async with sqlite.connect('hashes.db') as temp:
        await asio.gather(
        temp.execute('''CREATE TABLE images
                     (text url, text hash)'''),
        temp.execute('''CREATE TABLE audio
                     (text url, text hash)'''),
        temp.execute('''CREATE TABLE video
                     (text url, text hash)'''),
        temp.execute('''CREATE TABLE other
                     (text url, text hash)''')
        )
        asio.run(temp.commit())
    print('done!')

# Main function. Calls setup funcs and then the main event loop in client.run 
def main():
    if not os.path.exists('posts.db'):
        asio.run(genpostsdb())
    
    if not os.path.exists('hashes.db'):
        asio.run(genhashesdb())
    
    client.run(open('botid').read().strip())

if __name__ == "__main__":
    main()
