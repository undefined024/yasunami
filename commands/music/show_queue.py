import youtube_dl
async def run(discord, client, guild, config, message, args, song_queue, os):
    i = 1
    embed = discord.Embed(title = config['show_queue']['title'], description = config['show_queue']['description'], color = int(config['show_queue']['color'], 16))
    if len(song_queue):
        with youtube_dl.YoutubeDL() as ydl:
            for x in song_queue:
                info = ydl.extract_info(x, download = False)
                embed.add_field(name = "#"+ str(i) + " " + info.get('title', None), value = x)
                embed.set_thumbnail(url = client.user.avatar_url)
                i += 1
        await message.channel.send(embed = embed)
    else:
        embed.set_thumbnail(url = client.user.avatar_url)
        embed.add_field(name = config['show_queue']['no_queue'], value = "#")
        await message.channel.send(embed = embed)