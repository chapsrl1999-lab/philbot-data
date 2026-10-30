# PhilBot — attribution Swing 1h/RECENT40, **34 marchés** (29 octobre 2026)
**STATUT : recherches historiques hors ligne exécutées et archivées, candidate limitée, aucune preuve de rentabilité future. AUCUN déploiement, ordre ni changement de paramètres/risque. R20 totalement exclu.**

## Verdict
Une interaction précise semble mériter une validation future : **entrée STC après repli *dans le sens d'une tendance AlgoAlpha 1h*, suivie d'une sortie au flip AA/720h**. Lorsque le comparateur est une entrée quelconque du même actif/mois/sens AA, la prime moyenne est légèrement positive en 2025/2026, mais ses intervalles de confiance comprennent zéro ; **elle se réduit à presque rien sur 12 actifs supplémentaires non utilisés dans l'étude initiale**. La méthode n'est pas validée comme stratégie ni nouveau bot rentable.

### État des expériences, à ne pas confondre
- **Proposé :** une sortie précoce à 72h si le trade n'est pas gagnant ET ne bat pas BTC en direction — **TESTÉ HORS LIGNE et REJETÉ**.
- **Testé :** entrée Swing vs autres cryptos AA-alignées aux mêmes instants — **pas d'alpha de sélection d'actif robuste**.
- **Testé :** AA direction seule chaque lundi à horizon7j — **pas de rendement net stable pendant BTC plat**.
- **Testé :** interaction STC entrée + AA sortie longue vs entrées témoins en même tendance du même actif — **piste descriptive positive mais non robuste**, à mettre à l'épreuve.
- **Testé sur 12 autres actifs gelés avant accès aux données :** signe positif mais **gain nul à faible selon l'année**, insuffisant pour qualifier la piste.
- **NON EFFECTUÉ :** replay à vrai nouveau compte avec risque, financement, exécution, liquidation et PF en dollars; vérification trade-by-trade TradingView; prospective intacte. **Installé en live : rien**.

## 1. Pourquoi couper à 72h était une mauvaise idée
Le précédent comparateur 72h était imparfait car il n'honorait pas toujours le flip AA antérieur. Nous l'avons réparé : pour toutes les politiques, un flip AA avant72h entraîne la même sortie. Ensuite :
- A sort au flip AA ou 72h, au premier échu ;
- B sort au flip AA ou720h ;
- C sort à72h si PnL directionnel <=0 OU progression relative vs BTC <=0, sinon suit B.
654 entrées Swing communes pleinement maturées (22 actifs ; 272 en2024,213 en2025,169 jan–sept2026).
Moyenne du PNL **par entrée à notionnel identique**, net coût proxy 0,16point aller-retour :
| période | A courte | B longue AA | C filtre72h | C−B |
|---|---:|---:|---:|---:|
| 2024 | +2,58 % | +2,84 % | +3,13 % | +0,29pt |
| 2025 | −1,07 % | +1,56 % | −0,58 % | **−2,14pt** |
| 2026 jan–sept | +0,97 % | +4,44 % | +1,83 % | **−2,61pt** |
2026 C−B intervalle bootstrap par semaines **[−4,79; −0,47] points**. Le filtre rejette de nombreux trades temporairement perdants qui deviendront gagnants au flip AA. Parmi les 96 situations coupées en 2026 à72h, la prolongation B aurait rapporté en moyenne **+4,59 points** de plus que la sortie A. **NE PAS ajuster un seuil après cette réfutation**.

## 2. Le choix d'actif n'est pas la source évidente du profit
Témoin : même moment, même sens AA, autres cryptos AA-alignées, durée calendaire de sortie identique au trade source, frais identiques, 22 actifs.
Alpha moyen de l'événement Swing vs pairs AA :
- 2024 −0,49pt (IC95 [−2,17; +1,09])
- 2025 +0,71pt (IC95 [−0,98; +2,48])
- 2026 jan–sept **−0,01pt** (IC95 [−0,99; +1,27])
- 2026 BTC classé plat **−1,04pt** (IC95 [−3,03; +0,92])
Cela ne démontre pas que le timing STC soit inutile : **le témoin partage le même calendrier de signal STC** et isole la sélection de l'actif. Les 22 marchés sont survivants et la sélection est observationnelle.

## 3. AlgoAlpha seul chaque lundi ne suffit pas
Entrée chaque lundi 00UTC dans le sens AA connu à la clôture précédente, tenue 7j sur les mêmes 22 actifs, coût0,16point :
- BTC plat2024 : rendement moyen par événement AA −1,51%, témoin short −1,68%.
- BTC plat2025 : AA +0,28%, témoin short +2,82%.
- BTC plat jan–sept2026 : **AA −0,40%**, témoin short +0,52%.
Donc direction AA seule à horizon hebdomadaire fixe **REJETÉE** comme moteur indépendant pour marchés plats, selon critère figé.

## 4. Interaction STC+AA — contrôle d'entrée sur le même actif
Témoins = toutes les heures possibles du **même actif et mois**, même direction AA à la clôture, même état BTC-plat mesuré causalement, écart d'au moins 72h au signal. Entrée prochain open et sortie au propre AA flip ou720h. Comparateurs observationnels et très corrélés. Bootstrap par semaines UTC 2000.
**22 actifs initiaux, 647 événements comparables** (7 sans témoin) :
| période | n | surplus moyen de l'entrée STC | IC95 semaines |
|---|---:|---:|---|
| 2024 | 269 | −0,06pt | [−5,17; +4,29] |
| 2025 | 211 | **+1,41pt** | [−0,78; +3,84] |
| 2026 jan–sept | 167 | **+1,34pt** | [−1,03; +4,06] |
| 2026 BTC plat | 86 | **+2,22pt** | [−1,36; +5,08] |
| 2026 juil–sept, BTC plat | 30 | **+4,58pt** | [+1,77; +6,38] |
Le dernier sous-groupe ne compte que ~8 semaines synchronisées, a déjà fait l'objet de nombreuses recherches et **ne constitue pas une preuve découverte non biaisée**.

## 5. Validation transversale sans changer les règles
12 actifs préenregistrés avant téléchargement : **AAVE, ADA, APE, BCH, BNB, ETH, FIL, LINK, LTC, SAND, VET, ZEC**. Aucun dans les 22 initiaux. **780/780 archives** officielles mensuelles / quotidiennes téléchargées, SHA256 confirmé, 12×28 416 bougies1h sans lacune. Même protocole et seuils.
| période | n comparables | surplus moyen STC+AA | IC95 |
|---|---:|---:|---|
| 2024 | 148 | +3,14pt | [−1,33; +7,80] |
| 2025 | 124 | **+0,28pt** | [−1,86; +2,28] |
| 2026 jan–sept | 96 | **+0,08pt** | [−2,68; +2,84] |
| 2026 BTC plat | 50 | **+1,54pt** | [−1,32; +5,20] |
Les critères de signe (>0) et effectifs du pré-enregistrement sont **techniquement satisfaits**, mais le surplus est minuscule et très incertain en 2025/2026. **Passer un gate de criblage n'est PAS une validation d'avantage rentable.**

## 6. Ensemble de 34 actifs — description consolidée, non nouvelle règle d'admission
Pooled après les deux expériences, **1 015 événements appariés** :
| période | n | prime STC+AA vs témoin | IC95 bootstrap semaines |
|---|---:|---:|---|
| 2024 | 417 | +1,07pt | [−2,93; +4,93] |
| 2025 | 335 | +0,99pt | [−0,79; +3,00] |
| 2026 jan–sept | 263 | +0,88pt | [−1,30; +3,13] |
| 2026 BTC plat | 136 | +1,97pt | [−1,38; +4,88] |
| 2026 juil–sept BTC plat | 51 | +4,26pt | [+0,68; +7,81] |
2026 jan–sept : **LONG n168 +2,34pt**, IC[−0,89;+5,26], **SHORT n95 −1,70pt**, IC[−3,33;+0,41]. Une majorité de SHORT gagnants en live n'est pas la preuve que le signal de sélection SHORT surpasse un suivi quelconque des tendances.
Une partie du résultat 2026 est concentrée : en supprimant les trois événements les plus favorables à cette prime, l'avantage global moyen tombe de +0,88 à **+0,34pt**. Aucun de ces résultats n'est un rendement de compte ni un test de trading réel.

## 7. Risque non mesuré : bloquant pour toute promotion
Le Swing live utilise **zéro SL natif fixe**, ne pas interpréter le budget de bande de 1,75% comme perte garantie. Dans les positions virtuelles de notre premier groupe, l'excursion adverse intratrade 5e percentile des longs suivis jusqu'au flip AA est environ **−28,6% du prix** sans levier, pire proche de **−49%** ; avec levier réel, marge et corrélation, danger beaucoup plus grand.
Le moteur a des conditions de profit flottant/fermeture et des frais/funding inconnus, donc **aucun PF dollars, CAGR, DD portefeuille, rendement hebdomadaire composé ni probabilité de liquidation validés ici**. Ces grandeurs ne doivent pas être inventées à partir des moyennes de retours par entrée.

## 8. Action recommandée et état
- **Retenir une seule hypothèse** pour la recherche suivante : un *repli STC* dans une tendance locale AA pourrait apporter un léger surplus de qualité d'entrée quand la position peut rester ouverte assez longtemps. Le mécanisme n'est pas confirmé statistiquement sur toutes les années.
- **Rejeter** fermeture naïve à72h, confiance excessive dans la sélection des actifs, modèle AA hebdomadaire seul, et toute grille d'optimisation post hoc pour sauver les chiffres.
- **Avant toute création de moteur indépendant** : reconstruire un vrai compte neuf à capital initial (avec marges, stops/absence de stop, funding, liquidation et PNL flottant), vérifier les décisions contre TradingView, puis évaluer sur une période post-gel réellement non utilisée. Sans cela, ne pas déployer.
- **État vérifié** : aucune modification de Swing, Sélectif/Recent40, R20, aucune hausse de risque et aucun ordre envoyé. Les anciens résultats du rapport initial restent enregistrés; ce document les complète/corrige sans les effacer.

### Preuves
- Hypothèses préenregistrées dans le dépôt **privé** `chapsrl1999-lab/philbot-signer`, branche `research/swing-selectif-attribution-20261029` : `HOLD_OR_EXIT_72H_PREREG_20261029.md`, `CROSS_SECTIONAL_CONTROL_PREREG_20261029.md`, `AA_REGIME_WEEKLY_FACTOR_PREREG_20261029.md`, `STC_ENTRY_AA_EXIT_INTERACTION_PREREG_20261029.md`, `INTERACTION_12ASSETS_HOLDOUT_PREREG_20261029.md`.
- Source installée Swing SHA `83a20ec47f18b30d31ee5bdc3a58434c03585771`. Source Recent40 SHA `34501482f85e993e7473a51d6b52bfa03a3e4efb`. **Aucun de ces services n'a été modifié pour la recherche.**
- Archives **publiques** Binance vérifiées (sans code privé) dans runs GitHub `philbot-data` `40987169370`, `40987405056`, `40987699515` (complément octobre partial demandé), `40992859488` (12 nouveaux actifs, 780/780 SUCCESS).
- Script/source et registres JSON des cinq expériences remis séparément en archive HTML/ZIP de la conversation; SHA256 des registres dans le rapport HTML. Ne pas prétendre que les outputs des scripts sont installés en production.
