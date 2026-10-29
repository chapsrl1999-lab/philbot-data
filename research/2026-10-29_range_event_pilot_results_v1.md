# PhilBot LABO EDGE-FIRST — pilotage statistique V1 (pas un backtest de bot)
Date : 2026-10-29. **Résultat de mesure exploratoire ; non validé, aucune recommandation de trading.**
Aucun bot existant, position, ordre réel, infrastructure live ou paramètre modifié.

## Définition causale de l'événement préliminaire
- EMA du prix calculée sur 48 heures : 48 barres à 1h, ou 12 barres à 4h ; centre EMA arrêté à la barre précédente, connu avant la clôture du signal.
- ATR proxy : moyenne simple des 14 derniers true ranges incluant la barre signal clôturée. Extrême si |prix de clôture - centre EMA précédent| ≥ 1,5 ATR.
- Efficacité directionnelle (ratio déplacement net / somme des variations absolues sur les 48 heures précédentes, incluant barre signal) : range si <= 0,25 ; intermédiaire si (0,25 ; 0,45) ; tendanciel si >= 0,45.
- Échantillonnage au plus un événement sur 24h pour chaque combinaison régime/sens/actif (mais des événements peuvent encore se chevaucher ENTRE combinaisons ; ce ne sont pas des observations statistiquement indépendantes certifiées).
- Sens étudié : retour vers l'EMA (LONG après excès sous la moyenne, SHORT après excès au-dessus) ; entrée hypothétique à l'ouverture de la prochaine barre, liquidation hypothétique à la clôture de la 24e heure, sans levier ; net proxy = rendement directionnel en % - 0,20 point de pourcentage de coûts aller-retour. Pas de stop exécuté ni de remplissage réel.
- Étiquette auxiliaire +1 ATR avant -1 ATR : parcours OHLC jusqu'à 24h, si les deux touchés dans la même bougie, stop considéré premier. **Ce n'est pas le résultat d'un bot**.
- Les signaux ne consultent pas les données après leur date ; les étiquettes d'issue utilisent naturellement les barres futures.
- 2024/25 : perpétuels Bybit BTCUSDT et ETHUSDT sur 4h. 2026 : Spot Binance BTCUSDT 1h et 4h. Sources issues de miroirs GitHub, non certifiées contre les historiques natifs, funding non inclus. Les marchés/sources ne sont PAS équivalents.

## Résultats bruts après hypothèse -0,20 point de coût, épisodes classés « range »
| Instrument/source | Fenêtre | TF | Événements | Net moyen sur 24 h / événement | Taux de rendements > 0 |
|---|---|---:|---:|---:|---:|
| BTC Bybit perp | 2024 entière | 4h | 15 | +1,122 % | 66,7 % |
| BTC Bybit perp | 2025 au 05-12 | 4h | 31 | +0,652 % | 58,1 % |
| ETH Bybit perp | 2024 entière | 4h | 11 | +0,339 % | 45,5 % |
| ETH Bybit perp | 2025 au 05-12 | 4h | 19 | +0,625 % | 52,6 % |
| BTC Binance spot | juillet-septembre 2026 | 4h | **5** | **−0,122 %** | 60,0 % |
| BTC Binance spot | juillet-septembre 2026 | 1h | **93** | **−0,326 %** | 41,9 % |

4h BTC spot 2026 (juil–sept.) : tous régimes confondus, 42 événements, rendement net moyen −0,306 %; la classification stricte « range+excès » n'en détecte que 5. 1h BTC spot sur même fenêtre : 145 événements tous régimes, moyenne −0,388 %, dont 93 « range » à −0,326 %.
Le taux de succès « >0 après coûts à 24h » n'est pas le taux d'atteinte d'un TP : horizons de sortie hypothétiques et stops ne sont pas modélisés dans ces rendements.

## Couverture / sources relues
- BTC Bybit perp 4h : 12 489 bougies sans trou, du 2020-03-25 au 2025-12-05, SHA GitHub `1628d548488c28bacb7c237383895f46e4571831`.
- ETH Bybit perp 4h : 10 361 bougies sans trou, du 2021-03-15 au 2025-12-05, SHA `538a834150c6c6c01df402ecd0f2ec2c3d57f55d`.
- BTC Binance spot 1h : 2 745 bougies sans trou, 2026-06-15 au 2026-10-07, SHA `48f8ba7124cddf1b79e3f3f9b7636c5435db7741`.
- BTC Binance spot 4h : 1 136 bougies sans trou, 2026-04-01 au 2026-10-07, SHA `fc1f17b1863adfad7daa58f9e7c35db088a32540`.
- Sources : `mestoness/btc-eth-candles-history` et `Silent47boryara/searching-for-edge/07-bos/attribution-p1/raw`.
- **Aucune donnée de prix au-delà du 7 octobre 2026 dans les deux CSV 2026 consultés.**

## Interprétation limitée
- Les classes 4h donnent quelques moyennes positives pour BTC/ETH 2024/25, MAIS petits échantillons, sélection a posteriori, historiques/venues différents et aucun contrôle aléatoire apparié. **Ce n'est pas une preuve d'edge**.
- Sur BTC juil–sept 2026, retour moyen 24h dans la classe « range » **négatif après coût**, surtout en 1h. Il ne suffit pas de voir un range visuel pour conclure à une opportunité rentable.
- Les cinq événements « range » 4h en trois mois indiquent que cette définition peut manquer la plupart des fluctuations observables. Ne PAS retoucher le seuil uniquement pour augmenter le taux de réussite a posteriori ; examiner d'abord la couverture du régime.
- Aucune allocation de capital, aucun PF par trade, aucun drawdown de portefeuille ni test de liquidation calculé. Aucune conclusion sur une stratégie multiasset réelle.

## Prochaine expérience falsifiable
Sur un univers d'actifs comparable *dans une même venue* et tous les régimes 2024/25/26, construire un contrôle aléatoire **apparié actif/date/régime/volatilité**, dissocier LONG/SHORT et comparer direction retour contre continuation. Échantillonner par épisodes non chevauchants ; calculer IC/bootstrap par blocs temporels ; puis seulement chercher un moteur de trading avec entrées/sorties/coûts réalistes.
