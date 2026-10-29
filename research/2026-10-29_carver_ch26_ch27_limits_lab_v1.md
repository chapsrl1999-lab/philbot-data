# PhilBot Research — Carver 26/27, ordres limites — 2026-10-29
Statut: **recherche exploratoire uniquement, résultats non qualifiés, aucune installation ni changement live**.
Auteur de la source: Robert Carver, *Advanced Futures Trading Strategies*, chapitres 26 et 27 (EPUB fourni en conversation).

## Résultat / décision
- **Piste 26/27 avec ces paramètres: NON RETENUE pour live.**
- Le recours aux ordres limites améliore souvent les rendements comparativement à la simple exécution au marché, mais ne rend pas les modèles positifs dans la fenêtre BTC de juillet-septembre 2026.
- Ne pas confondre optimisation de l'exécution et source d'alpha. Ne pas rechercher après coup le palier qui a maximisé 2025 comme s'il s'agissait d'une preuve future.

## Données vérifiées pendant cette étude (horodatage UTC)
1. BTCUSDT Binance spot 1h, 2026-06-15 00:00–2026-10-07 08:00: 2745 barres, zéro trou horaire dans le CSV; copie GitHub Silent47boryara/searching-for-edge, objet sha **48f8ba7124cddf1b79e3f3f9b7636c5435db7741**.
2. BTCUSDT Binance spot 4h, 2026-04-01–2026-10-07: 1136 barres, objet sha **fc1f17b1863adfad7daa58f9e7c35db088a32540**.
3. BTCUSDT Binance spot daily, 2025-01-01–2026-10-06: 644 barres continues, pour préchauffage causal; objet sha **c3674de80ad5ac06dd171e507a2c559b518533ba**.
4. BTC et ETH USDT perps Bybit 4h, respectivement 12489 et 10361 barres continues, sources GitHub mestoness/btc-eth-candles-history; objets SHA **1628d548488c28bacb7c237383895f46e4571831** et **538a834150c6c6c01df402ecd0f2ec2c3d57f55d**. Couverture jusqu'au 2025-12-05, pas 2026.
Les CSV sont des dépôts secondaires; source déclarée non vérifiée de façon indépendante contre archives signées/flux natifs des bourses.

## Protocole d'approximation, pas une réplique parfaite de Carver
- Signal 26: EWM daily span 5, (equilibrium-current_price)/(price*annual_sigma/sqrt(365)), scalar 9.3, forecast cap +/-20.
- Signal 27: même mécanisme, scalar 20, annule les signaux opposés au signe EMA16-EMA64 daily; variante 27v multiplie le signal par un estimateur vol relatif basé sur percentile d'une fenêtre de 180j et EMA10, non la fenêtre originale de dix ans.
- Volatilité: variance du rendement log quotidien lissée exponentiellement sur environ 37 jours, annualisée par sqrt(365). Tous les indicateurs utilisent seulement les journées UTC terminées avant la bougie testée.
- Capital initial **neuf** 1000 USD à chaque début de période, sans position héritée, clôture finale du flottant. BTC 2026 seul: 1000 USD; BTC+ETH 2024/2025: 500 USD isolés par actif.
- Exposition nominale cible: 20% de risque annualisé de référence, plafonnée à 70% du capital par actif; aucune simulation de marge/liquidation native. Pas de stop-loss fixe.
- Marché: rebalancement au début de la bougie, frais taker hypothétiques 0.07%, glissement 0.03%.
- Limites: ajustement marché si écart à la cible >100 USD, sinon grille à deux côtés de 100 USD, limites obtenues par inversion du signal prix/cible; pénétration de 0.01% du niveau avant de compter le remplissage; maker 0.02%; supposé 100% exécution après franchissement. Intra-bougie: trajets HL ou LH simulés, *non observés* (biais important). Aucun carnet d'ordres.
- Profit factor PAR TRADE et R par trade non calculés car pas de registre de cycles d'inventaire indépendant; ne pas qualifier le PF des variations par bougie comme PF trade. DD avec flottant calculé aux clôtures, pas aux extrêmes intrabar.

## Résultats comparatifs (net en %, DD close-to-close en %, frais $)
| Données / dates | modèle | Marché net | Limites net HL | Limites DD HL | Frais limites |
| --- | --- | ---: | ---: | ---: | ---: |
| BTC spot 1h, 2026-07-01–09-30 | 26 | -16.83 | -8.77 | -16.32 | 44.23 |
| BTC spot 1h, 2026-07-01–09-30 | 27 | -10.42 | **-7.80** | **-11.97** | **38.32** |
| BTC spot 1h, 2026-07-01–09-30 | 27v | -9.96 | -9.31 | -13.62 | 36.20 |
| BTC spot 4h, 2026-07-01–09-30 | 27 | -9.52 | -9.95 | -12.38 | 25.77 |
| BTC+ETH Bybit 4h, 2024-01-01–12-31 | 27 | -23.47 | -5.91 | -19.60 | 45.88 |
| BTC+ETH Bybit 4h, 2025-01-01–12-05 | 27 | -8.74 | +2.11 | -13.86 | 48.55 |

**Sensibilité chapitre 27 BTC 1h juillet-septembre 2026:** pénétration maker 0.05% = -9.88%; pénétration 0.10% = -10.91%; coûts maker/taker et glissement x2 = -11.49%; paliers 50 USD = -11.81%, 150 USD = -5.76%, 200 USD = -4.33%. Ces variations sont toutes négatives.
**Sensibilité chapitre 27 BTC+ETH Bybit 4h 2025:** base +2.11%, pénétration 0.05% = -0.10%, 0.10% = -3.93%, coûts x2 = -2.62%. Le gain 2025 n'est pas robuste.

## Limites, non réalisés
- Pas de funding, spread réel, queue maker, quote réel, latence, min taille native, arrondis, marge, liquidation, stops, capacité, registre indépendant, contrôle Replay Maître, ni vraie validation prospective.
- La période 2026 utile est tronquée au 7 octobre. Le résultat sur BTC ne démontre ni la rentabilité ni l'échec d'un univers de 60 cryptos.
- La variation du palier et des hypothèses après observation n'est pas un véritable out-of-sample.
- Les chiffres doivent être recalculés et revérifiés depuis les OHLC et un ledger d'inventaire avant toute exploitation; ce fichier conserve les résultats expérimentaux, pas une certification.

## Next
Tester une hypothèse explicitement différente du signal de range, avec zones d'équilibre adaptées au régime, détection de cassure, puis validation chronologique, cross-assets et R20 strictement comparables. Aucun déploiement autorisé sur la base de cette recherche.