import requests

# Replace with your Discord webhook URL
DISCORD_WEBHOOK_URL = 'YOUR_DISCORD_WEBHOOK_URL'

def send_discord_alert(item):
    """
    Sends a simple text alert to Discord with the item details.
    """
    content = f"**{item['title']}**\nPrice: ${item['price']:.2f}\n{item['url']}"
    payload = {'content': content}
    resp = requests.post(DISCORD_WEBHOOK_URL, json=payload)
    resp.raise_for_status()