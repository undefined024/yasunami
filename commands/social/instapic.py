import json, urllib.request
async def run(discord, client, guild, config, message, args):
    if len(args) == 2:
        try:
            with urllib.request.urlopen("https://www.instagram.com/"+args[1]+"/?__a=1") as url:
                if url.getcode() == 200:
                    data = json.loads(url.read().decode())
                    profile_picture_url = data["graphql"]["user"]["profile_pic_url_hd"]
                    await message.channel.send(profile_picture_url)
                    return
        except urllib.error.HTTPError:
            embed = discord.Embed(title = config['insta_pic']['no_profile'], color = int(config['insta_pic']['no_profile_color'], 16))
            await message.channel.send(embed=embed)
    elif len(args) < 2:
        embed = discord.Embed(title = config['insta_pic']['no_username'], color = int(config['insta_pic']['no_username_color'], 16))
        await message.channel.send(embed=embed)
    else:
        embed = discord.Embed(title = config['insta_pic']['much_args'], color = int(config['insta_pic']['much_args_color'], 16))
        await message.channel.send(embed=embed)


