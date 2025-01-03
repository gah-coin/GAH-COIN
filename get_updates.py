import requests

# Ton token de bot Telegram
BOT_TOKEN = "7841497479:AAE1mfwU7ULMngC8OxWtl6VAAygKYf98NWg"

# URL pour récupérer les mises à jour
url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"

# Récupérer les messages récents
response = requests.get(url)

if response.status_code == 200:
    updates = response.json()
    print("Mises à jour reçues :")
    print(updates)
else:
    print(f"Erreur lors de la récupération des mises à jour : {response.text}")
