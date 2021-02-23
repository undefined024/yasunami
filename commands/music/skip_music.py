from commands.music import play_music
import youtube_dl

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
    if len(song_queue) >= 1 and len(client.voice_clients):
        voice = discord.utils.get(client.voice_clients, guild = guild)
        voice.stop()
        os.remove(config['bot']['current_song_path'] + config['bot']['current_song_name'])
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(song_queue[0], download = False)
            title = info_dict.get('title', None)
        embed = discord.Embed(title = config['skip_music']['info'], description = config['skip_music']['info_description'] + " " + title, color = int(config['skip_music']['info_color'], 16))
        await message.channel.send(embed = embed)
        play_music.play_song(song_queue, config, os, discord, client, guild)
    else:
        embed = discord.Embed(title = config['skip_music']['cant_skip'], description = config['skip_music']['cant_skip_description'], color = int(config['skip_music']['cant_skip_color'], 16))
        await message.channel.send(embed = embed)