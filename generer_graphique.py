import matplotlib.pyplot as plt
import json

def generer_graphique():
    """Générer un graphique basé sur l'historique avec un design amélioré."""
    try:
        # Lire l'historique depuis le fichier
        with open("historique_gah_coin.json", "r") as fichier:
            historique = json.load(fichier)

        if not historique:
            print("Aucune donnée disponible dans l'historique.")
            return

        # Extraire les données
        dates = [entry["date"] for entry in historique]
        valeurs_usd = [entry["valeur_usd"] for entry in historique]
        valeurs_fcfa = [entry["valeur_fcfa"] for entry in historique]

        if len(dates) < 2:
            print("Pas assez de points pour tracer un graphique.")
            return

        # Trouver les valeurs maximales et minimales
        max_usd = max(valeurs_usd)
        min_usd = min(valeurs_usd)
        max_fcfa = max(valeurs_fcfa)
        min_fcfa = min(valeurs_fcfa)
        max_usd_date = dates[valeurs_usd.index(max_usd)]
        min_usd_date = dates[valeurs_usd.index(min_usd)]
        max_fcfa_date = dates[valeurs_fcfa.index(max_fcfa)]
        min_fcfa_date = dates[valeurs_fcfa.index(min_fcfa)]

        # Configurer le graphique
        plt.figure(figsize=(12, 7))
        plt.plot(dates, valeurs_usd, label="Valeur en USD", color="blue", marker="o", linestyle="--")
        plt.plot(dates, valeurs_fcfa, label="Valeur en FCFA", color="green", marker="o", linestyle="-.")

        # Ajouter des annotations
        plt.annotate(f"Max: {max_usd:.6f} USD", xy=(max_usd_date, max_usd), xytext=(max_usd_date, max_usd + 0.0001),
                     arrowprops=dict(facecolor='blue', arrowstyle="->"), fontsize=10, color="blue")
        plt.annotate(f"Min: {min_usd:.6f} USD", xy=(min_usd_date, min_usd), xytext=(min_usd_date, min_usd - 0.0001),
                     arrowprops=dict(facecolor='blue', arrowstyle="->"), fontsize=10, color="blue")
        plt.annotate(f"Max: {max_fcfa:.2f} FCFA", xy=(max_fcfa_date, max_fcfa), xytext=(max_fcfa_date, max_fcfa + 50),
                     arrowprops=dict(facecolor='green', arrowstyle="->"), fontsize=10, color="green")
        plt.annotate(f"Min: {min_fcfa:.2f} FCFA", xy=(min_fcfa_date, min_fcfa), xytext=(min_fcfa_date, min_fcfa - 50),
                     arrowprops=dict(facecolor='green', arrowstyle="->"), fontsize=10, color="green")

        # Ajouter des labels et une légende
        plt.xlabel("Date", fontsize=12)
        plt.ylabel("Valeur", fontsize=12)
        plt.title("Évolution du GAH-COIN", fontsize=16, fontweight="bold")
        plt.legend()
        plt.grid(True, linestyle="--", alpha=0.7)

        # Ajuster les ticks de l'axe X
        plt.xticks(rotation=45, fontsize=10)
        if len(dates) > 10:  # Si trop de dates, afficher 10 ticks maximum
            plt.xticks(dates[::len(dates)//10])

        # Sauvegarder le graphique
        plt.tight_layout()
        plt.savefig("evolution_gah_coin.png")
        print("Graphique amélioré généré et sauvegardé sous 'evolution_gah_coin.png'.")
    except Exception as e:
        print(f"Erreur lors de la génération du graphique : {e}")

if __name__ == "__main__":
    generer_graphique()
