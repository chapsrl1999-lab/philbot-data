# PhilBot — recherche de rendement en range : résultats EDGE-FIRST V2
Date : 29 octobre 2026 (Québec). **Recherche exécutée hors ligne. Aucune stratégie ou infrastructure de trading modifiée.**

## Décision
**Rejeté comme source de rendement démontrée :** entrer directement sur un excès de prix en range (expérience A), ou attendre simplement une première bougie 4h de retour (expérience B). La confirmation évite une partie des pires opérations, mais ne crée pas de rendement net robuste ni d'avantage crédible contre des événements témoins.
Cette décision ne condamne pas les autres familles de stratégies de range. Elle rejette **uniquement ces deux mécanismes précis** sur cet univers et ce protocole.

## Preuves reproduisibles, statut
- Code A : [range_edge_once.py](https://github.com/chapsrl1999-lab/philbot-data/blob/research/range-edge-once-20261029/research/edge-first/range_edge_once.py).
- Résultats A : [results_20261029.json](https://github.com/chapsrl1999-lab/philbot-data/blob/research/range-edge-once-20261029/research/edge-first/results_20261029.json), blob GitHub `f5eb92d744436089f4e0e08c260ea373529bc652`.
- Run GitHub Actions A : [40951423748](https://github.com/chapsrl1999-lab/philbot-data/actions/runs/40951423748), status **SUCCESS**.
- Préenregistrement B *avant exécution* : [confirmation_pre_register.md](https://github.com/chapsrl1999-lab/philbot-data/blob/research/range-edge-once-20261029/research/edge-first/confirmation_pre_register.md), commit initial `eedd15b3965f89f8440a056d1bae09cb4ac87c6d`.
- Code B : [range_edge_confirmation_once.py](https://github.com/chapsrl1999-lab/philbot-data/blob/research/range-edge-once-20261029/research/edge-first/range_edge_confirmation_once.py).
- Résultats B : [confirmation_results_20261029.json](https://github.com/chapsrl1999-lab/philbot-data/blob/research/range-edge-once-20261029/research/edge-first/confirmation_results_20261029.json), blob GitHub `b06c132d898b5a9d727b49052a36779ef6b62126`.
- Sources : archives mensuelles OFFICIELLES `data.binance.vision/data/futures/um/monthly/klines`, BTC/ETH/SOL/BNB/XRP/ADA/DOGE/AVAX/LINK/LTC/DOT/BCH en futures USD-M 4h.
- **408 archives téléchargées sur 408 demandées**, SHA-256 du ZIP vérifié contre chaque fichier officiel CHECKSUM ; 6210 bougies *par actif*, continuité complète du 1 déc 2023 00:00 UTC au 30 sept 2026 20:00 UTC ; manifest complet des SHA-256 dans les résultats JSON.
- Aucun transfert de secrets ou requête API privée : seulement des prix publics. La branche dédiée `research/range-edge-once-20261029` n'est reliée à aucun service live.
- Compte de 1000 USD, registre d'ordres, slippage plateforme, stops/funding/marge/liquidation NON simulés — **ce n'est pas un backtest de bot ni un revenu réalisable**.

## Hypothèse A : acheter/vendre directement les excès en range
Règles figées : EMA12 des clôtures 4h, bande d'excès ±1,5 ATR14, régime causal `efficacité directionnelle 48h <= 0,25`, espacement minimum 24h par actif, entrée virtuelle à l'ouverture de la prochaine 4h et valorisation 24h après signal. Gains nets directionnels diminués de **0,20 point de pourcentage hypothétique** par aller-retour. Les contrôles ont même actif, mois, sens, régime et volatilité comparable (±40%), mais un écart moins extrême.

| Fenêtre UTC | Événements | Rendement net moyen / occasion | Avantage moyen vs contrôles | IC95% par semaines de l'avantage |
|---|---:|---:|---:|---:|
| 2024 complet | 219 | **+0,4409 %** | +0,5487 point | [-0,3125 ; +1,4036] |
| 2025 complet | 307 | **−0,3560 %** | −0,3802 point | [-1,3341 ; +0,5039] |
| Juil-sept 2026 | 57 | **−0,1688 %** | +0,1970 point | [-0,5533 ; +0,7570] |

Toutes les IC de l'avantage comprennent zéro. L'avantage n'est pas démontré.
La moyenne 2024 est **concentrée sur AVAX** : 22 événements à +3,7114 % de moyenne apportent ~+0,373 point à la moyenne globale +0,441. **En retirant fictivement AVAX, la moyenne des 197 autres occasions tombe à +0,0757 %**, sans constituer un nouveau backtest ni une permission de sélectionner a posteriori. En 2025, AVAX présente au contraire 26 événements, −1,9569 % en moyenne.

## Hypothèse B préenregistrée : attendre une bougie de retour 4h
Mêmes événements et prix, une seule condition ajoutée. Si la bougie 4h suivante clôture dans le sens du retour, le signal est « confirmé » ; **toutes les comparaisons B** entrent à l'ouverture de la barre t+2, et ressortent à la clôture de t+7. Les témoins appariés doivent EUX AUSSI confirmer leur première bougie, sans excursion extrême. Aucun remplissage artificiellement rétrospectif.

| Fenêtre | Total événements A | Confirmés B | Rendement net moyen confirmé B | Non confirmés (même entrée retardée) | Avantage B vs témoins confirmés | IC95% de l'avantage B |
|---|---:|---:|---:|---:|---:|---:|
| 2024 | 219 | 112 | **+0,4437 %** | +0,1945 % | +0,9733 point | [-0,2677 ; +2,3133] |
| 2025 | 307 | 162 | **−0,1092 %** | −1,4095 % | −0,2262 point | [-1,1741 ; +0,6567] |
| Juil-sept 2026 | 57 | 38 | **−0,1363 %** | −0,4140 % | −0,1483 point | [-0,7063 ; +0,4043] |

La confirmation réduit les mauvaises entrées de 2025 et 2026, mais **ne transforme pas le mécanisme en avantage rentable**. Elle ne surpasse pas les témoins de façon stable. Rendement 2025 B avec coût hypothétique doublé à 0,40 % A/R : −0,3092 %/occasion ; 2026 : −0,3363 %/occasion.

## Ce que cela démontre, et ce que cela ne démontre pas
- C'est une comparaison de résultats *conditionnels sur des événements*, pas une simulation de portefeuille et donc aucun PF par trade, rendement annuel composé, DD ni bilan de liquidation honnêtement disponible.
- Le panier de 12 grandes cryptos est un univers choisi avec connaissance de 2026 (biais de survivants). Les actifs disparus ne figurent pas; cela limite l'extrapolation.
- Les états historiques « range » ne sont définis qu'avec les prix disponibles à l'instant du signal; les issues futures servent uniquement à mesurer le résultat, pas à déclencher l'entrée.
- Les contrôles restent observationnels ; leurs caractéristiques non appariées et des marchés corrélés peuvent subsister. Le bootstrap regroupe par semaine, mais ses IC ne compensent pas le choix de sujets après des recherches passées.
- 2026 est connue des chercheurs et n'est pas un vrai hors-échantillon vierge.
- Résultats séparés par année nécessaires : sélectionner 2024, AVAX ou l'une des variantes après lecture serait une nouvelle forme d'overfitting.

## Prochaine hypothèse UNIQUE, encore NON TESTÉE
Avant de retester des RSI/STC ou des stops, examiner une **différence relative entre cryptomonnaies** : après neutralisation du mouvement commun BTC/ETH, un actif exceptionnellement faible revient-il vers son groupe plus souvent qu'il ne continue de sous-performer ?
Cela testerait une autre source de rendement (retour des écarts relatifs avec paire LONG/SHORT), potentiellement moins dépendante du sens général du marché. Aucune rentabilité présumée. Commencer par enregistrer et tester le comportement relatif *sans levier, stops ou bot*, avec contrôle apparié et coûts de deux jambes, sur 2024/2025/été 2026.
Ne déployer ni modifier aucun système existant sur cette base.

**État exact** : A TESTÉ, B TESTÉ, données 408/408 VALIDÉES, aucune stratégie découverte et validée, protocole du prochain test seulement PROPOSÉ, aucun live touché.
