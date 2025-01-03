import requests

# Ton token de bot Telegram
BOT_TOKEN = "7841497479:AAE1mfwU7ULMngC8OxWtl6VAAygKYf98NWg"

# L'identifiant de ton groupe Telegram
CHAT_ID = "-1001426677742"  # Remplace par l'identifiant exact de ton groupe

# Message à envoyer
message = "🎉 Bonjour, ceci est un test d'envoi depuis GAH-Coin Bot."

# URL pour envoyer le message
url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

# Paramètres du message
params = {
    "chat_id": CHAT_ID,
    "text": message
}

# Envoi de la requête
response = requests.post(url, data=params)

if response.status_code == 200:
    print("Message envoyé avec succès dans le groupe !")
else:
    print(f"Erreur lors de l'envoi : {response.text}")
