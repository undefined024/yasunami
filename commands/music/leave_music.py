async def run(discord, client, guild, config, message, args, song_queue):
    if not len(client.voice_clients):
        embed = discord.Embed(title = config['stop_music']['cant_leave'], description = config['stop_music']['cant_leave_description'], color = int(config['stop_music']['cant_leave_color'], 16))
        await message.channel.send(embed = embed)
        return
    channel = client.voice_clients[0]
    await channel.disconnect()
    song_queue.clear()
