import requests
import json
import datetime
import matplotlib.pyplot as plt
from binance.client import Client

# Clés API Binance
BINANCE_API_KEY = "lgQ8PnpRMKD94fB8hX3IdCnutSuQF6JX18ZCGXMp1u1OpBr3z1sZzolgKrNlP0IJ"
BINANCE_API_SECRET = "z12ZicLEKqaEiGxHRHKnlJKULladUEgln78vHNd4rseVTh97uj6G7wtmvRW3La5J"

# Token et ID du groupe Telegram
BOT_TOKEN = "7841497479:AAE1mfwU7ULMngC8OxWtl6VAAygKYf98NWg"
CHAT_ID = "-1001426677742"  # Identifiant du groupe

# Fichiers pour stocker les données
FICHIER_ETAT = "dernier_gah_coin_value.json"
FICHIER_HISTORIQUE = "historique_gah_coin.json"

# Initialiser le client Binance
client = Client(BINANCE_API_KEY, BINANCE_API_SECRET)

def lire_historique():
    """Lire l'historique des valeurs depuis le fichier JSON."""
    try:
        with open(FICHIER_HISTORIQUE, "r") as fichier:
            return json.load(fichier)
    except FileNotFoundError:
        return []

def sauvegarder_historique(valeur_usd, valeur_fcfa):
    """Sauvegarder l'évolution dans l'historique."""
    historique = lire_historique()
    horodatage = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    nouvelle_entree = {
        "date": horodatage,
        "valeur_usd": valeur_usd,
        "valeur_fcfa": valeur_fcfa
    }
    historique.append(nouvelle_entree)
    with open(FICHIER_HISTORIQUE, "w") as fichier:
        json.dump(historique, fichier, indent=4)

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

def generer_graphique():
    """Générer un graphique basé sur l'historique."""
    historique = lire_historique()
    dates = [entry["date"] for entry in historique]
    valeurs_usd = [entry["valeur_usd"] for entry in historique]
    valeurs_fcfa = [entry["valeur_fcfa"] for entry in historique]

    plt.figure(figsize=(10, 6))
    plt.plot(dates, valeurs_usd, label="Valeur en USD", marker="o")
    plt.plot(dates, valeurs_fcfa, label="Valeur en FCFA", marker="o")
    plt.xlabel("Date")
    plt.ylabel("Valeur")
    plt.title("Évolution du GAH-COIN")
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("evolution_gah_coin.png")
    print("Graphique généré et sauvegardé sous 'evolution_gah_coin.png'.")

def envoyer_message_telegram(message):
    """Envoyer un message dans le groupe Telegram."""
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

def envoyer_graphique_telegram(nom_fichier):
    """Envoyer un fichier (graphique) dans le groupe Telegram."""
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
        with open(nom_fichier, "rb") as fichier:
            files = {"document": fichier}
            params = {"chat_id": CHAT_ID}
            response = requests.post(url, data=params, files=files)
        if response.status_code == 200:
            print("Graphique envoyé avec succès sur Telegram !")
        else:
            print(f"Erreur lors de l'envoi du graphique : {response.text}")
    except Exception as e:
        print(f"Erreur lors de l'envoi du graphique : {e}")

if __name__ == "__main__":
    # Calculer la nouvelle valeur du GAH-COIN
    nouvelle_valeur_usd, nouvelle_valeur_fcfa = calculer_valeur_gah_coin()

    if nouvelle_valeur_usd > 0:
        # Sauvegarder l'historique
        sauvegarder_historique(nouvelle_valeur_usd, nouvelle_valeur_fcfa)

        # Créer le message
        message = (
            f"💰 Valeur actuelle GAH-COIN\n\n"
            f"1 GAH-COIN = {nouvelle_valeur_usd:.6f} USD\n"
            f"1 GAH-COIN = {nouvelle_valeur_fcfa:.2f} FCFA\n"
            f"📈 Historique sauvegardé avec succès !"
        )

        # Envoyer le message
        envoyer_message_telegram(message)

        # Générer et envoyer le graphique
        generer_graphique()
        envoyer_graphique_telegram("evolution_gah_coin.png")
    else:
        print("Impossible de calculer la valeur GAH-COIN.")
