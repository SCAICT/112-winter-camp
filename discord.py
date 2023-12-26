import requests
import requests

bot_token = 'MTE4ODk4NjA0Mjg1OTE0NzM1NQ.G4PPQu.5ItJp1GyNexrh7PmkF4Z8e2kfJEq1gx95GGjx4'
guild_id = '1172505294920745071'
channel_id = '1188990914488700978'
new_title = '報名人數：'
headers = {
    'Authorization': f'Bot {bot_token}',
    'User-Agent': 'DiscordBot (https://wc.scaict.org, 1.0.0)'
}
url = f'https://discord.com/api/v10/channels/{channel_id}'
response = requests.patch(url, headers=headers, json= {
    'name': new_title,
})
if response.status_code == 200:
    print(f"Changed the title of channel #{channel_id} to {new_title}")
else:
    print(f"Failed to change the title. Status code: {response.status_code}, Response: {response.text}")
