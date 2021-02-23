import youtube_dl, asyncio, youtube_search

ydl_opts = {
    'format': 'bestaudio/best',
    'quiet': True,
    'no_warnings': True,
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}

async def run(discord, client, guild, config, message, args, song_queue, os):
    if message.author.voice == None:
        embed = discord.Embed(title = config['play_music']['no_voice_channel'], description = config['play_music']['no_voice_channel_description'], color = int(config['play_music']['no_voice_channel_color'] ,16))
        await message.channel.send(embed = embed)
        return
    channel = message.author.voice.channel
    if not len(client.voice_clients):
        await channel.connect()
    if "https://youtube.com/watch?v=" in args[1]:
        url = args[1]
    else:
        args.pop(0)
        sub_url = youtube_search.YoutubeSearch(" ".join(x for x in args), max_results = 1).to_dict()[0]['url_suffix']
        url = "https://youtube.com" + sub_url
    song_queue.append(url)
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        if client.voice_clients[0].is_playing():
            info_dict = ydl.extract_info(url, download = False)
            embed = discord.Embed(title = config['play_music']['added_queue']+ " " + info_dict.get('title', None), description = url, color = int(config['play_music']['added_queue_color'], 16))
            embed.set_thumbnail(url = info_dict.get('thumbnail',None))
            await message.channel.send(embed = embed)
            return
    await play_song(song_queue, config, os, discord, client, guild, channel, message)

async def play_song(song_queue, config, os, discord, client, guild, channel, message):
    if len(song_queue) and len(client.voice_clients):
        song = os.path.isfile(config['bot']['current_song_path'] + config['bot']['current_song_name'])
        if song:
            os.remove(config['bot']['current_song_path'] + config['bot']['current_song_name'])
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(song_queue[0], download = False)
            embed = discord.Embed(title = config['play_music']['playing'] + " " + info.get('title', None), description = song_queue[0], color = int(config['play_music']['playing_color'], 16))
            embed.set_thumbnail(url = info.get('thumbnail',None))
            await message.channel.send(embed = embed)
            ydl.download([song_queue[0]])
        for file in os.listdir("./"):
            if file.endswith(".mp3"):
                os.rename(file, config['bot']['current_song_path'] + config['bot']['current_song_name'])
                break
        voice = discord.utils.get(client.voice_clients, guild = guild)
        song_queue.pop(0)
        voice.play(discord.FFmpegPCMAudio(config['bot']['current_song_path'] + config['bot']['current_song_name']), after = lambda x: asyncio.run_coroutine_threadsafe(play_song(song_queue, config, os, discord, client, guild, channel, message), client.loop))
    else:
        voice = discord.utils.get(client.voice_clients, guild = guild)
        song_queue.clear()
