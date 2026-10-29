# PhilBot EDGE-FIRST — préenregistrement de l'expérience B : confirmation 4h
Date 2026-10-29, avant exécution de cette expérience.
Aucun bot existant, même en témoin, et aucune connexion à une API d'ordre.

## Question UNIQUE
Après un excès du prix déjà détecté à l'instant t, attendre une bougie 4h complète qui évolue **vers** la moyenne améliore-t-il l'espérance économique par rapport aux excès non confirmés et à des moments non extrêmes avec la même première impulsion ?

## Population inchangée
- Les 12 actifs, 408 archives USDT-M Binance, 2024, 2025 et juillet–septembre 2026, mêmes checksums et couverture que l'étude A.
- Signal original : écart >=1.5 ATR14 à l'EMA12 sur 4h, efficacité de direction <=0.25 sur 12 bougies, événements espacés d'au moins 24h par actif, calcul causal. Aucun réglage optimisé.
- Un seul supplément : la bougie immédiatement SUIVANTE après le signal clôture dans la direction du retour vers l'équilibre : LONG si close[t+1] > close[t], SHORT si close[t+1] < close[t]. Cette clôture doit être connue avant l'entrée.
- **Pour tous les événements confirmés comme non confirmés, simuler l'entrée seulement à l'ouverture t+2** et sortir à la clôture t+7 (24h après clôture de confirmation). Ainsi une confirmation ne prend jamais artificiellement le prix de t+1.
- Coût hypothétique aller-retour constant 0.20 point de pourcentage; sens LONG/SHORT séparé. Funding, slippage natif, exécution, stop/marge non modélisés => PAS un bot.
- Contrôle apparié : même actif, mois UTC, sens, efficacité de range, ATR/prix à +/-40%, écart non extrême (0.25 à <1.5 ATR), confirmation identique à t+1, non chevauchant l'événement à +/-24h; comparer rendement net moyen.
- Intervalle de confiance par rééchantillonnage de semaines UTC communes à tous les actifs. Vérifier 2024, 2025, été 2026 séparément; aucun paramètre nouveau selon les résultats.
- Critère de poursuite : avantage net confirmé contre contrôle et coût stressé dans plusieurs années, pas concentré dans un seul actif; sinon rejeter cette famille de confirmation comme démonstration insuffisante.
- Ne pas confondre avantage de trade avec un portefeuille exécutable; aucun déploiement, aucune modification de risque.
