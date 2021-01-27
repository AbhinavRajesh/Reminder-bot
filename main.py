import discord
import os
import datetime as dt
import pytz
from timetable import timetable

client = discord.Client()

@client.event
async def on_ready():
    print(f'Logged in as {client.user.name}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('$class'):
        args_len = len(message.content.split())
        now = dt.datetime.now(pytz.timezone('Asia/Kolkata'))
        if args_len == 1:
            if now.weekday() < 5:
                first = True
                for i in timetable[now.weekday()]:
                    text = ''
                    if first:
                        first = False
                        text = '**CS A** \n'
                    else:
                        text = '**CS B** \n'
                    for j in i:
                        text += j + '\n'
                    await message.channel.send(text)
            else:
                await message.channel.send("**No Class today according to Timetable**")
        elif args_len == 2:
            if 'help' == message.content.split(' ')[1].lower():
                return await message.channel.send("""
`$class` : Returns timetable for that particular day for both the batches [ CS-A and CS-B],
`$class ARGS`: Returns the timetable for the batch specified as ARGS
Currently Accepted `ARGS`:
    - `CSA` [ Case insensitive ]
    - `CSB` [ Case insensitive ]
    - `HELP` [ Case insensitive ]
""")
            if 'csa' == message.content.split(' ')[1].lower():
                text = '**CS A** \n'
                i = timetable[now.weekday()][0]
            elif 'csb' == message.content.split(' ')[1].lower():
                text = '**CS B** \n'
                i = timetable[now.weekday()][1]
            for j in i:
                text += j + '\n'
            await message.channel.send(text)

client.run(os.getenv('TOKEN'))