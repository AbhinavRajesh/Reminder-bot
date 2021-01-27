import discord
import os
import datetime as dt
import pytz

client = discord.Client()

timetable = {
    0: [
            [
                'CVPDE Class at 9:00 AM, MEET LINK: N/A', 
                'ALC Class at 10:45 AM, MEET LINK: https://meet.google.com/msx-ppdx-ytx',
                'DBMS/DS Lab at 01:00 PM, MEET LINK: N/A' 
            ],
            [
                'ALC Class at 9:00 AM, MEET LINK: https://meet.google.com/vok-hnsw-mrx',
                'CVPDE Class at 10:45 AM, MEET LINK: N/A',
                'DBMS/DS Lab Class at 01:00 PM, MEET LINK: N/A',
            ]
        ],
    1: [
            [
                'DBMS Class at 9:00 AM, MEET LINK: N/A', 
                'CAO Class at 10:45 AM, MEET LINK: N/A',
                'MP Class at 01:00 PM, MEET LINK: N/A' 
            ],
            [
                'MP Class at 9:00 AM, MEET LINK: N/A',
                'CAO Class at 10:45 AM, MEET LINK: N/A',
                'DBMS Class at 01:00 PM, MEET LINK: N/A',
            ]
        ],
    2: [
            [
                'DSA Class at 9:00 AM, MEET LINK: N/A', 
                'MP Class at 10:45 AM, MEET LINK: N/A',
                'DBMS/DS Lab at 01:00 PM, MEET LINK: N/A' 
            ],
            [
                'MP Class at 9:00 AM, MEET LINK: N/A',
                'DSA Class at 10:45 AM, MEET LINK: N/A',
                'UHV2 Class at 01:00 PM, MEET LINK: N/A',
            ]
        ],
    3: [
            [
                'CVPDE Class at 9:00 AM, MEET LINK: N/A', 
                'CAO Class at 10:45 AM, MEET LINK: N/A',
                'DSA Class at 01:00 PM, MEET LINK: N/A' 
            ],
            [
                'DSA Class at 9:00 AM, MEET LINK: N/A',
                'CAO Class at 10:45 AM, MEET LINK: N/A',
                'CVPDE Class at 01:00 PM, MEET LINK: N/A',
            ]
        ],
    4: [
            [
                'ALC Class at 9:00 AM, MEET LINK: https://meet.google.com/msx-ppdx-ytx', 
                'DBMS Class at 10:45 AM, MEET LINK: N/A',
                'UHV2 Class at 01:00 PM, MEET LINK: N/A' 
            ],
            [
                'DBMS Class at 9:00 AM, MEET LINK: N/A',
                'ALC Class at 10:45 AM, MEET LINK: https://meet.google.com/vok-hnsw-mrx',
                'DBMS/DS Lab at 01:00 PM, MEET LINK: N/A',
            ]
        ]
}

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