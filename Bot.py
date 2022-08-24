import discord
from discord import Intents
from discord.ext import commands
import datetime

client = commands.Bot(command_prefix=".",intents=Intents.all())

f = open("Rules.txt","r")
rules = f.readlines()

f = open("token.txt","r",encoding="utf-8")
Token = f.read()

guild_ids = [806925492736753735]

client.lavalink_nodes=[
    {
        'host':'lava.link',
        'port':80,
        'password':'MrParadox'
    }
]

@client.event
async def on_ready():
    print("The bot is ready")
    client.load_extension('dismusic')

@client.event
async def on_command_error(ctx,error):
    if isinstance(error,commands.MissingPermissions):
        await ctx.send("You can't do that ;-;")
        await ctx.message.delete()
    elif isinstance(error,commands.MissingRequiredArgument):
        await ctx.send("Please enter the *required argument*")
        await ctx.message.delete()
    #elif isinstance(error,commands.CommandInvokeError):
        #await ctx.send("Please enter the *required argument*")
        #await ctx.message.delete()
    elif isinstance(error,commands.CommandNotFound):
        await ctx.send("please enter *valid* command ;-;")
        await ctx.message.delete()
    else:
        raise error

async def is_blacklisted(ctx):
    if guild_ids[0] == 806925492736753735:
        return True
    else:
        return False
@commands.check(is_blacklisted)

@client.event
async def on_member_join(member:discord.Member):
    try:
        channel = client.get_channel(866713597845176330)

        member_role = member.guild.get_role(role_id=866684029888757800)

        try:
            #welcome embed
            embed = discord.Embed(colour=discord.Colour.random(), description=f"Welcome to Paradox U&K Gaming's Discord server!\n You are {len(list(member.guild.members))}th member!")
            embed.set_image(url=member.avatar_url)
            embed.set_author(name=f"{member.name}", icon_url=f"{member.avatar_url}")
            embed.set_footer(text=f"{member.guild}", icon_url=f"{member.guild.icon_url}")
            embed.timestamp=datetime.datetime.utcnow()
            await channel.send(embed=embed)

            #add member role
            await member.add_roles(member_role)

        except Exception as e:
            raise e
    except Exception as e:
        raise e

@client.command()
async def hello(ctx):
    await ctx.send("Hi")

@client.command(aliases=['Rule','Rules','rules','rul'])
async def rule(ctx,*,number):
    await ctx.reply(rules[int(number)-1])

@client.command(aliases = ['clear'])
@commands.has_permissions(manage_messages = True)
async def purge(ctx,amount: int=2):
    await ctx.channel.purge(limit=amount)

@client.command()
@commands.has_permissions(kick_members = True)
async def kick(ctx,member:discord.Member,*,reason="No Reason Provided"):
    try:
        await member.send("You have been kicked from Paradox U&K Gaming, Becuase:"+reason)
    except:
        print("member have their DMs closed")

    await ctx.send(member.name +" has been kicked from Paradox U&K Gaming, Becuase:"+reason)
    await member.kick(reason=reason)

@client.command()
@commands.has_permissions(ban_members = True)
async def ban(ctx,member:discord.Member,*,reason="No Reason Provided"):
    try:
        await member.send("You have been banned from Paradox U&K Gaming, Becuase:"+reason)
    except:
        print("member have their DMs closed")

    await ctx.send(member.name +" has been banned from Paradox U&K Gaming, Becuase:"+reason)
    await member.ban(reason=reason)

@client.command()
@commands.has_permissions(ban_members = True)
async def unban(ctx,*,member):
    banned_users = await ctx.guild.bans()
    member_name,member_discriminator = member.split('#')

    for banned_entry in banned_users:
        user = banned_entry.user

        if (user.name,user.discriminator)==(member_name,member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(member_name + " has been unbanned")
            return
    
    await ctx.send(member+" was not found")

@client.command()
@commands.has_permissions(kick_members = True)
async def mute(ctx,member:discord.Member):
    muted_role = ctx.guild.get_role(886995164592218163)

    await member.add_roles(muted_role)  
    await ctx.send(member.mention +" has been muted")

@client.command()
@commands.has_permissions(kick_members = True)
async def unmute(ctx,member:discord.Member):
    muted_role = ctx.guild.get_role(886995164592218163)

    await member.remove_roles(muted_role)  
    await ctx.send(member.mention +" has been unmuted") 

@client.command(aliases = ['user','info'])
async def whois(ctx,member:discord.Member):
    
    roles=[role for role in member.roles]
    embed = discord.Embed(title=member.name,description=member.mention,color=discord.Colour.random())

    embed.set_thumbnail(url=member.avatar_url)
    embed.set_footer(icon_url=ctx.author.avatar_url,text=f"request by {ctx.author.name}")

    embed.add_field(name="ID:",value=member.id)
    embed.add_field(name=f"Roles({len(roles)}):",value=" ".join([role.mention for role in roles]))
    embed.add_field(name=f"Top Roles: ",value=member.top_role.mention)
    embed.add_field(name="Created at: ",value=member.created_at.strftime("%a , %#d %b %Y, %I:%M %p GMT"))
    embed.add_field(name="Joined at: ",value=member.joined_at.strftime("%a , %#d %b %Y, %I:%M %p GMT"))
    
    await ctx.send(embed=embed)

@client.command()
async def rule_embed(ctx):
    embed = discord.Embed(title="Rules",description="These rules have been made in order to keep the server safe for everyone. Every member must follow these rules at all times. If you break the rules, you will receive a warning. If you reach 5 warnings in under a month, you'll get banned from the server.",color=discord.Colour.random())
    embed.add_field(name="1. This is an English only server.",value="This is an English only server.",inline=False)
    embed.add_field(name="2. Respect Everyone and don't cause drama",value="Please don't harass/bully anyone or be toxic and avoid having any fights/ creating drama in this server. Even though non-excessive cursing is allowed in this server, you are not allowed to target a member.",inline=False)
    embed.add_field(name="3. Follow Discord TOS",value="Make sure to follow Discord Terms of service and guidelines at all times. Any violation will result in an instant ban. (e.g. Being under 13)\n :link: https://discord.com/terms :link: https://discord.com/guidelines")
    embed.add_field(name="4. No form of Racism",value="Any form of Racism will not be tolerated. The use Racial slurs (e.g. N word) are prohibited and will result in a permanent ban. Do not misuse spoilers to make words look like racial slurs. ",inline=False)
    embed.add_field(name="5. No Illegal Actions",value="Do not talk about or do anything illegal in the server. This includes posting code that can be used to commit a crime. Do not post malicious links or files that could be used to steal accounts or information anywhere.")
    embed.add_field(name="6. No NSFW",value="Do not send any NSFW images/emotes or discuss NSFW topics anywhere in this server. This also includes any suggestive emojis. Any kind of NSFW will not be tolerated. ",inline= False)
    embed.add_field(name="7. Avoid Controversial Topics",value="Avoid having any religious or political conversations here.",inline=False)
    embed.add_field(name="8. Do not spam",value="Don't spam within channels, this can mean: \n➥Chat Flood: Typing separate lines very quickly ; \n➥Wall Text: Typing out large blocks of text ;  \n➥Chaining:  Lyrics that make up a song etc ; \n➥Repetitive Messages:Posting the same images/emojis multiple times  ; \n➥Epileptic Emotes: Posting/reacting with flashy GIFs or Emotes")
    embed.add_field(name="9. Do not Self-Advertise",value="Please don't promote your stuff anywhere in the server and in DMs, you can only advertise in self-advertising ",inline=False)
    embed.add_field(name="10. Stay on Topic",value="Keep your topics in the correct channels and if you don't know what channel is for you can look at the channel topics/pins to see exactly what you must keep on-topic there. Bot commands should not be used in channels meant for conversing. If the commands are related to the topic they can be used as long as they aren't being spammed. ",inline=False)
    embed.add_field(name="11. Do not argue with Staff",value="Do not argue with staff in chats instead, message a higher ranked staff member. Do not ping or annoy staff members without a valid reason. Staff have the right to punish members for reasons that haven't been listed in the rules as long as the reason is valid.")
    embed.add_field(name="12. No Begging",value="Do not beg for code, nitro, roles, items or anything similar from anyone in the server.",inline=False)
    embed.add_field(name="13. No Impersonation",value="Do not impersonate people/bots by using identical profile pictures or names.")
   
    await ctx.send(content=f"{ctx.message.guild.default_role}",embed=embed)
    await ctx.message.delete()



client.run(Token) 