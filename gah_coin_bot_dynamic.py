import requests
import json
from binance.client import Client

# Clés API Binance
BINANCE_API_KEY = "lgQ8PnpRMKD94fB8hX3IdCnutSuQF6JX18ZCGXMp1u1OpBr3z1sZzolgKrNlP0IJ"
BINANCE_API_SECRET = "z12ZicLEKqaEiGxHRHKnlJKULladUEgln78vHNd4rseVTh97uj6G7wtmvRW3La5J"

# Token et ID du groupe Telegram
BOT_TOKEN = "7841497479:AAE1mfwU7ULMngC8OxWtl6VAAygKYf98NWg"
CHAT_ID = "-1001426677742"  # Identifiant du groupe

# Fichier pour stocker la dernière valeur du GAH-COIN
FICHIER_ETAT = "dernier_gah_coin_value.json"

# Initialiser le client Binance
client = Client(BINANCE_API_KEY, BINANCE_API_SECRET)

def lire_derniere_valeur():
    """Lire la dernière valeur sauvegardée depuis le fichier."""
    try:
        with open(FICHIER_ETAT, "r") as fichier:
            data = json.load(fichier)
            return data.get("dernier_gah_coin_value", None)
    except FileNotFoundError:
        return None

def sauvegarder_derniere_valeur(valeur):
    """Sauvegarder la dernière valeur dans le fichier."""
    with open(FICHIER_ETAT, "w") as fichier:
        json.dump({"dernier_gah_coin_value": valeur}, fichier)

def obtenir_taux_conversion():
    """Obtenir le taux de conversion USD -> FCFA (XAF) depuis une API."""
    try:
        url = "https://api.exchangerate-api.com/v4/latest/USD"
        response = requests.get(url)
        data = response.json()
        taux_fcfa = data["rates"].get("XAF", 0)
        if taux_fcfa > 0:
            return taux_fcfa
        else:
            print("Erreur : Taux FCFA non trouvé dans les données.")
            return 600  # Retourner un taux par défaut en cas de problème
    except Exception as e:
        print(f"Erreur lors de la récupération du taux de conversion : {e}")
        return 600  # Retourner un taux par défaut en cas d'erreur

def calculer_valeur_gah_coin():
    try:
        # Récupérer les soldes
        account = client.get_account(recvWindow=10000)
        balances = account['balances']
        total_usd = 0.0

        for balance in balances:
            asset = balance['asset']
            free = float(balance['free'])
            if free > 0:  # Considérer uniquement les actifs avec des soldes non nuls
                if asset != "USDT":
                    try:
                        price = float(client.get_symbol_ticker(symbol=f"{asset}USDT")['price'])
                        total_usd += free * price
                    except:
                        pass
                else:
                    total_usd += free

        # Calculer la valeur d’un GAH-COIN
        if total_usd > 0:
            gah_coin_value_usd = total_usd / 1000000  # Divisé par 1 000 000
            taux_fcfa = obtenir_taux_conversion()
            gah_coin_value_fcfa = gah_coin_value_usd * taux_fcfa
            return gah_coin_value_usd, gah_coin_value_fcfa
        else:
            return 0, 0
    except Exception as e:
        print(f"Erreur lors du calcul de la valeur GAH-COIN : {e}")
        return 0, 0

def envoyer_message_telegram(message):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        params = {
            "chat_id": CHAT_ID,
            "text": message
        }
        response = requests.post(url, data=params)
        if response.status_code == 200:
            print("Message envoyé avec succès sur Telegram !")
        else:
            print(f"Erreur lors de l'envoi du message Telegram : {response.text}")
    except Exception as e:
        print(f"Erreur lors de l'envoi du message Telegram : {e}")

if __name__ == "__main__":
    # Lire la dernière valeur sauvegardée
    dernier_gah_coin_value = lire_derniere_valeur()

    # Calculer la nouvelle valeur du GAH-COIN
    nouvelle_valeur_usd, nouvelle_valeur_fcfa = calculer_valeur_gah_coin()

    if nouvelle_valeur_usd > 0:
        # Vérifier si la valeur a changé
        if dernier_gah_coin_value is None or dernier_gah_coin_value != nouvelle_valeur_usd:
            # Sauvegarder la nouvelle valeur
            sauvegarder_derniere_valeur(nouvelle_valeur_usd)

            # Créer le message
            message = (
                f"💰 Valeur actuelle GAH-COIN\n\n"
                f"1 GAH-COIN = {nouvelle_valeur_usd:.6f} USD\n"
                f"1 GAH-COIN = {nouvelle_valeur_fcfa:.2f} FCFA\n"
                f"🌍 Taux de conversion dynamique mis à jour. Restez connectés pour plus de mises à jour !"
            )

            # Envoyer le message
            envoyer_message_telegram(message)
        else:
            print("Pas de changement dans la valeur du GAH-COIN. Aucun message envoyé.")
    else:
        print("Impossible de calculer la valeur GAH-COIN.")
