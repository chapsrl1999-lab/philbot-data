# PhilBot — Pourquoi les bots de range échouent et changement de méthode
29 octobre 2026. **DIAGNOSTIC ET ORIENTATION DE RECHERCHE, pas de résultat de nouvelle stratégie et aucune modification live.**
Périmètre **R20 exclu intégralement** (ni référence, ni objet de comparaison, ni variante). Aucune exécution en bourse, aucun service Railway, aucune modification de code des bots.

## Verdict
Nous avons surtout cherché à prévoir un petit retournement du prix à partir d'oscillateurs/EMA et à optimiser des entrées. La recherche doit désormais identifier **la contrepartie économique qui paie** un avantage dans les marchés peu directionnels. Une statistique brute du cours ou un graphique latéral ne suffit pas à démontrer que ce retournement rapporte net après coûts.

## Différence fondamentale tendance / range
- Un moteur de tendance peut survivre avec peu de gagnants si certaines positions capturent un mouvement exceptionnellement long. La littérature documente une persistance conditionnelle dans plusieurs marchés à terme; cela ne garantit pas les bots crypto particuliers.
- Un moteur de retour à la moyenne a souvent beaucoup de gains plus petits et quelques pertes importantes lorsque le cours cesse de revenir. Le régime horizontal *constaté après coup* ne peut pas être employé pour qualifier le régime à l'entrée.
- Pour un marché sans prévisibilité au prix d'exécution, la moyenne brute des prix ne constitue pas une rente : coûts et slippage sont structurellement négatifs. Il faut soit une vraie prévisibilité du rendement **conditionnel**, soit gagner autrement (spread, financement, différence relative entre instruments).

## Preuves internes déjà enregistrées
- Archives OFFICIELLES et vérifiées de 12 marchés USDT-M Binance, 408/408 checksums SHA-256, historiques 4h du 1 décembre 2023 au 30 septembre 2026 : `research/2026-10-29_range_edge_first_results_v2.md`.
- Retour sur excursion 4h en régime "range" : rendement moyen net par occasion +0.4409 % 2024 (219), -0.3560 % 2025 (307), -0.1688 % été 2026 (57), coûts hypothétiques de 0.20 point et sorties horaires proxies, sans vraie simulation de book.
- Confirmation de première bougie de retour : +0.4437 % 2024 (112), -0.1092 % 2025 (162), -0.1363 % été 2026 (38). Pas d'avantage statistique convaincant vs témoins, 2026 déjà influencée par recherche antérieure.
- Les anciens rapports fondés seulement sur OHLC ne prouvent pas la file d'attente, l'ordre exact des touches intrabougie ni les fills maker; aucun résultat de spread net réel n'en découle.

## Ce que les sources externes indiquent
1. Dobrynskaya (Journal of Alternative Investments, 2023), 2 000 cryptos 2014–2020 : momentum de court horizon (jusqu'à ~2 à 4 semaines), inversion à horizons supérieurs à ~un mois. **Ce n'est PAS une preuve sur 2026 ou sur le perp 15m; cela rend notre présupposé de reversal après 4h douteux et nécessite un test d'échelle avant de créer un moteur.** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3913263
2. Tiniç et al., Journal of Financial Research (2023), coûts de sélection adverse dans le spread des principales cryptos. Un fill d'ordre limite est parfois exécuté parce que le prix va contre nous. **Les calculs maker sur OHLC 4h ne valident pas une stratégie market making.** https://onlinelibrary.wiley.com/doi/10.1111/jfir.12317
3. Hyperliquid publie des instantanés L2 historiques et des flux de transactions, mais archive avec coût de transfert et possibles lacunes. **Données L2 + règles de file d'attente sont indispensables à un test de capture de spread.** https://hyperliquid.gitbook.io/hyperliquid-docs/historical-data
4. Hyperliquid affiche en base perp (tier 0) taker 0.045% et maker 0.015% *avant rabais propres au compte*, sur la page officielle. Le statut « maker » ne suffit pas à prouver un gain : spread réellement encaissé, sélection adverse, frais, ordres non exécutés, inventaire et latence à mesurer. https://hyperliquid.gitbook.io/hyperliquid-docs/trading/fees
5. Étude de 2026 sur 26 marchés de funding, 749 actifs / huit jours : écarts de financement affichés souvent non exploitables net de coûts et reversals; seulement 40% des meilleures occasions (selon leurs hypothèses) positives net. Fenêtre courte et hypothèses spécifiques, donc pas de généralisation. https://www.mdpi.com/2227-7390/14/2/346
6. Les études sur paires/cointegration donnent des résultats nuancés, parfois positifs hors échantillon, mais sensibles au coût et à la qualité du prix : https://www.tandfonline.com/doi/full/10.1080/14697688.2026.2653663 . Pas de validation pour notre portefeuille.

## Remplacement du « 103e bot » par un audit de source de rendement
On ne démarre **aucun nouveau moteur** tant que les trois questions suivantes n'ont pas une réponse mesurée :
- **D'où viennent les dollars ?** L'autre côté de l'opération paie-t-il un spread, une prime de financement, une différence de prix relative, ou un risque mesurable de liquidité ?
- **Ce dollar est-il réellement encaissable ?** Mesure de fills maker/taker, ordres non exécutés, frais effectifs, funding, volatilité adverse pendant l'attente, latence, capital immobilisé et liquidation. Pour les hedges, prise en compte explicite de deux jambes.
- **Est-ce exploitable 2024, 2025 et durant l'été 2026 ?** Pas uniquement une année ni un univers actuel; test causal, comparateur, coûts stressés, régimes et semaines, hypothèses et données figées avant les chiffres.

## Trois sources économiques distinctes (liste de vérification, aucune validée)
**A. Capture de liquidité (market making passif).** Le client pressé paie implicitement l'écart acheteur-vendeur; le danger est qu'il soit informé et que l'inventaire chute. Doit être étudiée en données L2 réelles et possible exécution, pas avec touches intrabougie 4h. Coût d'exploitation potentiellement élevé et latence exigeante : ne pas construire sans bénéfice probable mesuré.

**B. Financement / basis (carry).** Un acteur paye des funding lorsque le perp est déséquilibré. Le gain brut peut être amputé des écarts de base, frais de deux jambes, liquidations, immobilisation des fonds et contrepartie. Valeur complémentaire possible, rendement élevé non acquis. Exige historique funding et exécution réalisable.

**C. Valeur relative (positions simultanées LONG/SHORT ou panier).** Parier sur un écart inter-actifs ou résiduel au facteur BTC/ETH, mais **ne pas présumer reversion** : comparer retour et continuation, horaires et coûts sur les mêmes données. Mesurer corrélation instable, betas estimés causalement, deux jambes, funding et pertes simultanées. Pistes soutenues mais pas prouvées par la littérature.

## Décision d'architecture
**Premier travail utile** : inventorier les données réellement accessibles (ordres L2, prix perp 15m, funding, fee tiers et coûts) et quantifier l'espérance *nette réalisable* de chaque mécanisme, avec possibilité de rejeter vite une famille sans ajouter de filtre. N'en sélectionner qu'une après confrontation, au lieu de promettre qu'une nouvelle stratégie bâtie sur l'EMA « devrait fonctionner ».

- Si aucun mécanisme positif net n'est trouvé, noter le résultat négatif et ne pas construire.
- Si un mécanisme positif net, multi-régime et non dû à sélection tardive existe, construire une unique preuve de concept isolée, compte neuf, parité trade-by-trade, puis validation chronologique et prospective avant toute discussion live.
- Le rendement ambitieux du projet n'est **pas** plafonné au rendement d'un livre. Il dépendra de l'avantage démontré, du risque accepté et de l'exécution.
- L'architecture de recherche n'autorise **aucune** modification d'un bot existant, risque ou compte.

**État : cette note est un diagnostic sourcé et une orientation de laboratoire, pas la découverte d'une stratégie gagnante, ni un replay, ni un bot installé.**
