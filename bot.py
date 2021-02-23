import discord, configparser, os, time, random, asyncio
from commands.music import play_music, leave_music, pause_music, resume_music, skip_music, show_queue
from commands.social import instapic

song_queue = []

intents = discord.Intents.default()
intents.members = True
config = configparser.ConfigParser()
config.read("config.ini", encoding = "utf8")
client = discord.Client(guild_subscriptions = True, intents = intents)

@client.event
async def on_ready():
    global guild
    guild = await client.fetch_guild(int(config['bot']['guild_id']))
    if len(client.voice_clients):
        for x in client.voice_clients:
            await x.disconnect()
    os.system("cls")
    print(client.user.name+"#"+client.user.discriminator+"\n"+"Elindult")
    client.loop.create_task(check_date())
@client.event
async def on_message(message):
    if message.author == client.user or message.content.startswith(config['bot']['prefix']): return
    args = message.content[len(config['bot']['prefix']):].split()
    if args[0] == "play": await play_music.run(discord, client, guild, config, message, args, song_queue, os)
    if args[0] in ["leave", "stop", "stfu"]: await leave_music.run(discord, client, guild, config, message, args, song_queue)
    if args[0] == "pause": await pause_music.run(discord, client, guild, config, message, args)
    if args[0] == "resume": await resume_music.run(discord, client, guild, config, message, args)
    if args[0] == "skip": await skip_music.run(discord, client, guild, config, message, args, song_queue, os)
    if args[0] == "queue": await show_queue.run(discord, client, guild, config, message, args, song_queue, os)
    if args[0] == "instapic": await instapic.run(discord, client, guild, config, message, args)
@client.event
async def on_member_join(member):
    embed = discord.Embed(title = member.display_name + "#" + member.discriminator + " " +config['welcome_message']['embed_message'], color = int(config['welcome_message']['embed_color'], 16))
    embed.set_thumbnail(url = member.avatar_url)
    channel = await client.fetch_channel(int(config['welcome_message']['channel_id']))
    await channel.send(embed = embed)

@client.event
async def on_raw_reaction_add(payload):
    if(int(payload.channel_id) == int(config['rules']['channel_id']) and payload.emoji.name == config['rules']['reaction']):
        role = guild.get_role(int(config['rules']['role_id']))
        await payload.member.add_roles(role)
    if(int(payload.channel_id) == int(config['911_programming_english']['channel_id'])):
        if payload.emoji.name == config['911_programming_english']['911_reaction']:
            role = guild.get_role(int(config['911_programming_english']['911_role_id']))
            await payload.member.add_roles(role)
        elif payload.emoji.name == config['911_programming_english']['911_reaction']:
            role = guild.get_role(int(config['911_programming_english']['programming_role_id']))
            await payload.member.add_roles(role)
        elif payload.emoji.name == config['911_programming_english']['911_reaction']:
            role = guild.get_role(int(config['911_programming_english']['english_role_id']))
            await payload.member.add_roles(role)

#Morning And Night

async def send_msg(lang, time):
    time_cfg = config["morning_and_night"]
    hun_channel = await client.fetch_channel(int(time_cfg['hun_channel_id']))
    eng_channel = await client.fetch_channel(int(time_cfg['eng_channel_id']))
    msg = {
        "hun" : {
            "morning" : time_cfg["hun_mornings"],
            "night" : time_cfg["hun_nights"]
        },
        "eng" : {
            "morning" : time_cfg["eng_mornings"],
            "night" : time_cfg["eng_nights"]
        }
    }
    if time == "morning": color = time_cfg["morning_color"]
    else: color = time_cfg["night_color"]

    if lang == "hun": channel = hun_channel
    else: channel = eng_channel

    embed = discord.Embed(title = random.choice(msg[lang][time].split('@')), color = int(color, 16))
    await channel.send(embed = embed)
async def check_date():
    time_cfg = config["morning_and_night"] 
    while True:
        if time.strftime("%H:%M:%S") == time_cfg["morning_time"]:
            await send_msg("hun", "morning")
            await send_msg("eng", "morning")
        if time.strftime("%H:%M:%S") == time_cfg["night_time"]:
            await send_msg("hun", "night")
            await send_msg("eng", "night")
        await asyncio.sleep(1)
client.run(config['bot']['token'])