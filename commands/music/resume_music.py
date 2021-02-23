async def run(discord, client, guild, config, message, args):
    channel = client.voice_clients[0]
    if channel.is_paused():
        await channel.resume()
    elif channel.is_playing():
        embed = discord.Embed(title = config['resume_music']['already_resumed'], description = config['resume_music']['already_resumed_description'], color = int(config['resume_music']['already_resumed_color'], 16))
        await message.channel.send(embed = embed)
    else:
        embed = discord.Embed(title = config['resume_music']['cant_resume'], description = config['resume_music']['cant_resume_description'], color = int(config['resume_music']['cant_resume_color'], 16))
        await message.channel.send(embed = embed)