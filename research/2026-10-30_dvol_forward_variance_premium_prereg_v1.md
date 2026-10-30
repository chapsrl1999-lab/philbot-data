# PhilBot — contrôle du prix de la volatilité des options BTC, AVANT calcul
Gel 30 octobre 2026. Recherche uniquement. Aucun bot ni compte ni stop modifié. R20 totalement exclu. Pas de nouvelle stratégie de trading autorisée.

## Question économique unique
Le marché des options facture-t-il une **volatilité implicite 30 jours** systématiquement supérieure à celle qui se réalise dans les 30 jours suivants, **lorsque BTC ne suit pas de tendance forte** ? Une prime de variance positive est une condition préalable possible pour vendre une protection (options) mais n'est PAS le profit net d'une vente d'options. On ne créera ni faux tickets, ni PNL fictif.

## Séries et méthode, figées avant résultats
- DVOL BTC officiel Deribit 1h, 36 mois 2023-10→2026-09, SHA256 de chaque mois selon ancien manifeste PhilBot lot69 vérifié.
- BTCUSDT Binance USD-M 1h OHLC vérifiées par ZIP CHECKSUM; fenêtres jusqu'à septembre 2026. Sous-jacent **différent** de l'indice de règlement Deribit : risque de base déclaré.
- Chaque lundi **00:00 UTC**, IV = clôture DVOL du dimanche 23:00 UTC, connue alors. RV futur = racine de la somme des carrés de retours logarithmiques horaires BTC `log(close/open)` des **720 prochaines heures** (30 jours) multipliée par `365/30`, annualisée en pourcentage. Mesure brute des returns sous-jacents, pas une simulation delta-hedgée.
- Prime **IV30² − RV30² en points de variance annuels**, avec les deux volatilités exprimées en % annuels; et écart IV30−RV30 en points de volatilité. Les retours horaires avec données manquantes excluent entièrement l'observation (aucune interpolation).
- BTC « peu directionnel » défini causalement par |variation du close BTC sur les **14 jours précédents**| <=5% avant le lundi00.
- Périodes 2024,2025,2026 jusqu'aux lundis dont les 30 jours futurs sont entièrement couverts (pas de remplissage futur). Afficher nombre, fraction de primes positives, médiane, moyenne, pires 5, volatilité implicite/réalisée ; contrôle flat vs all. Fenêtres hebdomadaires se chevauchent : ne pas compter ces points comme indépendants, bootstrap par blocs de 5 semaines ou mois civil, montrer n mois.
- Critère initial : prime moyenne ET médiane positive en 2025 **et** 2026 dans le sous-échantillon BTC peu directionnel. Si positif, piste de **source économique** seulement, et prochaine étape obligatoire = historique bids/asks options, construction de positions à risque défini, exécution/frais/liquidation/marge. Si négatif, écarter pour le présent horizon, pas d'optimisation d'expiration.
- Ne PAS annoncer de rendement ni PF sur 1000 USD à partir de IV-RV : aucune option effectivement cotée ni exécutée. Risque de pertes extrêmes en vente de volatilité, plus grand que prime moyenne.
