import discord
from discord.ext import commands
from discord.utils import get
import os
import datetime as dt
import pytz
from timetable import timetable

client = commands.Bot(command_prefix="?")

days = {
    0: 'Monday',
    1: 'Tuesday',
    2: 'Wednesday',
    3: 'Thursday',
    4: 'Friday',
    5: 'Saturday',
    6: 'Sunday',
}

@client.event
async def on_ready():
    print(f'Logged in as {client.user.name}')
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='?class'))

@client.event
async def on_message(ctx):
    if ctx.author == client.user:
        return
    if ctx.content.startswith('?class'):
        args_len = len(ctx.content.split())
        now = dt.datetime.now(pytz.timezone('Asia/Kolkata'))
        if args_len == 1:
            if now.weekday() < 5:
                first = True
                for i in timetable[now.weekday()]:
                    className = ''
                    if first:
                        first = False
                        className = 'CS-A'
                        await ctx.channel.send(get(ctx.guild.roles, name="CS-A").mention)
                    else:
                        className = 'CS-B'
                        await ctx.channel.send(get(ctx.guild.roles, name="CS-B").mention)
                    embed = discord.Embed(title=f"Timetable {className}", description=f"{className} Timetable for {days[now.weekday()]}", color=discord.Color.green())
                    for j in i:
                        temp = j.split(' ') # CVPDE Class at 9:00 AM, MEET LINK: N/A
                        embed.add_field(name="Subject", value=f"{temp[0]} {temp[1]}", inline=True)
                        embed.add_field(name="Time", value=temp[3], inline=True)
                        embed.add_field(name="Meet Link", value=temp[-1], inline=True)
                    embed.set_thumbnail(url= client.user.avatar_url)
                    embed.set_footer(icon_url = ctx.author.avatar_url, text=f'Requested by {ctx.author}')
                    await ctx.channel.send(embed=embed)
            else:
                embed = discord.Embed(title="No Class", description=f"According to timetable {days[now.weekday()]} is a holiday")
                embed.set_thumbnail(url= client.user.avatar_url)
                embed.set_footer(icon_url = ctx.author.avatar_url, text=f'Requested by {ctx.author}')
                await ctx.channel.send(embed=embed)
        elif args_len == 2:
            if 'help' == ctx.content.split(' ')[1].lower():
                embed = discord.Embed(title = "Commands" ,description = "Commands for the CS2K23 Timetable Reminder Bot", color=discord.Color.red())
                embed.add_field(name = "?class", value="This command returns the class timetable for both CS-A and CS-B Batch for that particular day", inline=False)
                embed.add_field(name = "?class csa", value="This command returns the class timetable for CS-A Batch for that particular day", inline=False)
                embed.add_field(name = "?class csb", value="This command returns the class timetable for CS-B Batch for that particular day", inline=False)
                embed.set_thumbnail(url= client.user.avatar_url)
                embed.set_footer(icon_url = ctx.author.avatar_url, text=f'Requested by {ctx.author}')
                return await ctx.channel.send(embed=embed)
            if now.weekday() < 5:
                if 'csa' == ctx.content.split(' ')[1].lower():
                    className = 'CS-A'
                    await ctx.channel.send(get(ctx.guild.roles, name="CS-A").mention)
                    i = timetable[now.weekday()][0]
                elif 'csb' == ctx.content.split(' ')[1].lower():
                    className = 'CS-B'
                    await ctx.channel.send(get(ctx.guild.roles, name="CS-B").mention)
                    i = timetable[now.weekday()][1]
                else:
                    embed = discord.Embed(title = "Commands" ,description = "Commands for the CS2K23 Timetable Reminder Bot", color=discord.Color.red())
                    embed.add_field(name = "?class", value="This command returns the class timetable for both CS-A and CS-B Batch for that particular day", inline=False)
                    embed.add_field(name = "?class csa", value="This command returns the class timetable for CS-A Batch for that particular day", inline=False)
                    embed.add_field(name = "?class csb", value="This command returns the class timetable for CS-B Batch for that particular day", inline=False)
                    embed.set_thumbnail(url= client.user.avatar_url)
                    embed.set_footer(icon_url = ctx.author.avatar_url, text=f'Requested by {ctx.author}')
                    return await ctx.channel.send(embed=embed)
                embed = discord.Embed(title=f"Timetable {className}", description=f"{className} Timetable for {days[now.weekday()]}", color=discord.Color.green())
                for j in i:
                    temp = j.split(' ') # CVPDE Class at 9:00 AM, MEET LINK: N/A
                    embed.add_field(name="Subject", value=f"{temp[0]} {temp[1]}", inline=True)
                    embed.add_field(name="Time", value=temp[3], inline=True)
                    embed.add_field(name="Meet Link", value=temp[-1], inline=True)
                embed.set_thumbnail(url= client.user.avatar_url)
                embed.set_footer(icon_url = ctx.author.avatar_url, text=f'Requested by {ctx.author}')
            else:
                embed = discord.Embed(title="No Class", description=f"According to timetable {days[now.weekday()]} is a holiday")
                embed.set_thumbnail(url= client.user.avatar_url)
                embed.set_footer(icon_url = ctx.author.avatar_url, text=f'Requested by {ctx.author}')
            await ctx.channel.send(embed=embed)

client.run(os.getenv('TOKEN'))

