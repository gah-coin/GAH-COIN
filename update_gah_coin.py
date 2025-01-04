from binance.client import Client

# Tes clés Binance
api_key = "lgQ8PnpRMKD94fB8hX3IdCnutSuQF6JX18ZCGXMp1u1OpBr3z1sZzolgKrNlP0IJ"
api_secret = "z12ZicLEKqaEiGxHRHKnlJKULladUEgln78vHNd4rseVTh97uj6G7wtmvRW3La5J"

# Initialiser le client Binance
client = Client(api_key, api_secret)

# Calcul de la valeur du portefeuille
def calculer_valeur_portefeuille():
    try:
        # Obtenir les soldes et calculer la valeur
        account_info = client.get_account()
        balances = account_info['balances']
        
        valeur_totale = 0
        for asset in balances:
            asset_symbol = asset['asset']
            free_balance = float(asset['free'])
            locked_balance = float(asset['locked'])
            total_balance = free_balance + locked_balance
            
            if total_balance > 0:
                # Obtenir le prix en USDT
                try:
                    ticker = client.get_symbol_ticker(symbol=f"{asset_symbol}USDT")
                    price = float(ticker['price'])
                    valeur_totale += total_balance * price
                except:
                    continue
        
        valeur_gah_coin = valeur_totale / 1000000  # Divisé par 1,000,000
        print(f"Valeur totale du portefeuille : ${valeur_totale:.2f}")
        print(f"Valeur de 1 GAH-COIN : ${valeur_gah_coin:.8f}")
    except Exception as e:
        print(f"Erreur : {e}")

calculer_valeur_portefeuille()
