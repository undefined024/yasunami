async def run(discord, client, guild, config, message, args):
    channel = client.voice_clients[0]
    if channel.is_playing():
        await channel.pause()
    elif channel.is_paused():
        embed = discord.Embed(title = config['pause_music']['already_paused'], description = config['pause_music']['already_paused_description'], color = int(config['pause_music']['already_paused_color'], 16))
        await message.channel.send(embed = embed)
    else:
        embed = discord.Embed(title = config['pause_music']['cant_pause'], description = config['pause_music']['cant_pause_description'], color = int(config['pause_music']['cant_pause_color'], 16))
        await message.channel.send(embed = embed)