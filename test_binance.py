from binance.client import Client

# Clés API Binance
API_KEY = "lgQ8PnpRMKD94fB8hX3IdCnutSuQF6JX18ZCGXMp1u1OpBr3z1sZzolgKrNlP0IJ"
API_SECRET = "z12ZicLEKqaEiGxHRHKnlJKULladUEgln78vHNd4rseVTh97uj6G7wtmvRW3La5J"

# Initialiser le client Binance
client = Client(API_KEY, API_SECRET)

try:
    # Récupérer les soldes avec recvWindow explicite
    account = client.get_account(recvWindow=10000)
    balances = account['balances']

    print("Liste des actifs avec des soldes non nuls :")
    total_usd = 0.0

    for balance in balances:
        asset = balance['asset']
        free = float(balance['free'])
        if free > 0:  # Afficher uniquement les cryptos avec un solde supérieur à 0
            print(f"{asset}: {free}")

            # Convertir en USD si ce n'est pas déjà de l'USDT
            if asset != "USDT":
                try:
                    price = float(client.get_symbol_ticker(symbol=f"{asset}USDT")['price'])
                    total_usd += free * price
                except:
                    print(f"Impossible de récupérer le prix de {asset}.")
            else:
                total_usd += free

    print(f"\nValeur totale du portefeuille en USD : {total_usd:.2f}")

    # Calculer la valeur d’un GAH-COIN
    if total_usd > 0:
        gah_coin_value = total_usd / 1000000  # Divisé par 1 000 000
        print(f"Valeur actuelle d'un GAH-COIN : {gah_coin_value:.6f} USD")
    else:
        print("Portefeuille vide, impossible de calculer la valeur d'un GAH-COIN.")

except Exception as e:
    print(f"Erreur lors de la connexion à Binance : {e}")
