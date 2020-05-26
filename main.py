#!/usr/bin/env python
# -*- coding: utf-8 -*-

import discord
import os
import asyncio as asio
import aiosqlite as sqlite
# local imports, add .py to see their contents
from archive import archive

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
        print(message.content,'command found')
    else: # do regular archival
        post = await archive(message)
        
# This creates the posts.db file which stores every single post, starting from
# execution. The table created from this stores the posts with the following 
# keys:
# TEXT date: the date of the post
# TEXT post: the text content of the post
# TEXT user: the username of the user who made the post
# TEXT embed: the embeds/files of the post, should be semicolon delimited 
#   links to where the embeds are
# TEXT channel: the channel that the post was posted in
# This also creates the table for caching embeds so that they are only 
# downloaded once per day using the following keys:
# TEXT url: url of the attachment
# TEXT filename: filename of the attachment
async def genpostsdb():
    print('posts.db does not exist, creating...', end='')
    async with sqlite.connect('posts.db') as temp:
        await temp.execute('''CREATE TABLE posts
                    (date TEXT, post TEXT, user TEXT,
                    embed TEXT, channel TEXT)''')
        await temp.execute('''CREATE TABLE embed_cache
                    (url TEXT, filename TEXT)''')
        await temp.commit()
    print('done!')

# Main function. Calls setup funcs and then the main event loop in client.run 
def main():
    if not os.path.exists('posts.db'):
        await genpostsdb()
    
    client.run(open('botid').read().strip())

if __name__ == "__main__":
    main()
