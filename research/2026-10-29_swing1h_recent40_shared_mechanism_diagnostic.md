# PhilBot — SWING 1h et RECENT40 : diagnostic de mécanisme commun
Date : 2026-10-29, analyse en **LECTURE SEULE**, aucun changement live, aucun signal ou ordre émis.
Statut : **SOURCES / VERSIONS VÉRIFIÉES ; HYPOTHÈSES D'ATTRIBUTION NON ENCORE TESTÉES**.
R20 est totalement exclu de cette recherche, comme demandé.

## Verdict
Les deux candidats ayant une performance live affichée croissante ne sont pas des moteurs de range classiques opposés : tous deux utilisent **un rebond / recul STC à l'intérieur d'une direction fixée par AlgoAlpha (AA)**. Ils diffèrent par le timeframe, les réglages, le modèle de sélection et les règles de risque. Une hypothèse particulièrement testable est que leur avantage éventuel provienne de **tendances locales LONG ou SHORT sur certains actifs, même pendant une stagnation du marché global**, pas de la réversion du prix à une moyenne générale. **Rien ici ne prouve encore la rentabilité future de ce mécanisme.**

## Versions effectivement installées lues depuis Railway
- **RAFALE2 Swing-Recycle 1H BloFin** : projet Railway `zesty-learning`, service `philbot-rafale2-swing-shadow` (nom historique : le runtime confirme `mode=LIVE`), branche `fix/rafale2-swing-epic-reconcile-20261020`, SHA installé `83a20ec47f18b30d31ee5bdc3a58434c03585771`, dernier déploiement `582fb46c-996a-49cd-9071-848cce926730`. Source `rafale2_swing_shadow/RAFALE2_SWING_1H_SIGNALER.pine`, blob `b768d73e58578c9e1dc26a98ad87818ab6ca8d2c`, logique de taille `rafale2_swing_core.mjs` blob `5b393b4eacdbaaad548ec521064e8e8ff39079a0`.
- **Recent40/CORR12 Hyperliquid** : projet Railway `philbot-recent40-observer`, service `recent40-observer`, mode LIVE malgré le texte historique du README disant `observation` ; branche `maintenance/recent40-provisional-feed-20261029`, SHA installé `34501482f85e993e7473a51d6b52bfa03a3e4efb`, déploiement `4cc47a17-f2db-4280-a6d6-608f8b3cdfb0`. Contrat `recent40/config/contract.json` blob `7202f23c3615ab889baec85339f04e76be47905a`, moteur `recent40/recent40/live_engine.py`, `recent40/js/features.mjs`, référence `recent40/config/reference_indicators.js`.
- Ces preuves de versions ne certifient pas chacune des décisions ni chacun des fills/TP/SL ultérieurs.

## Mécanismes comparés : faits vérifiés dans le code
| Point | Swing 1h | Recent40/CORR12 |
|---|---|---|
| Unité / paramétrage | 1h, mêmes paramètres sur tous les actifs, 65 actifs annoncés dans Control | 15m/30m, 78 recettes paramétrées par actif et direction (33 en 15m, 45 en 30m), directions 45 LONG et 33 SHORT dans le contrat |
| STC | 200 / 75 / 125 / 0,05, zone 25/75, rebond 9 | STC par recette (ex. 250/100/150/0.1 ou 200/75/125/0.05); zones/rebond par recette |
| AlgoAlpha | ZLEMA350 / multiplicateur ATR 5,5 ; LONG seulement trend==+1, SHORT seulement trend==−1 | AA paramétré par recette ; dans `reference_indicators.js`, les conditions d'entrée sont également `aa.trend == direction` et STC extrême/recul |
| Sélection | Filtre STC+AA unique ; verrou symbole et caps | Sélecteur `RECENCY` apprentissage 12 mois glissants (avec cutoff 2 mois avant le mois courant), calibration 2 mois, score >= percentile 0,60, **non** probabilité de gain; features STC, AA, extension, efficacité, dispersion, historiques virtuels, etc. |
| Sortie | AA_FLIP ou TIME_30D = 720 h; **aucun stop natif fixe**. Bande opposée utilisée seulement comme référence de sizing | Stop AA **natif reduceOnly**, plus sortie au FLIP_AA, éventuellement FLIP_ENTRY. |
| Risque | Budget indicatif à la bande 1,75 %/entrée, plafonds 40 % total / 28 % par sens, marge à l'entrée 60 %, levier <=7. Sans ordre SL natif, 1,75 % n'est pas une perte maximale garantie. | Base 1,25 % par signal, multiplicateur 0,75–1,25, risque ouvert 20 %, risque corrélé 12 %, marge 85 %, levier <=20 ; un stop natif par position doit être confirmé. |

## Captures du 29 oct fournies par Philippe, sans interpréter comme PnL entièrement réalisé
- Swing 20h20 Québec : valeur 763,89 USD, variation depuis live +27,90 % / +166,61 USD, 21 positions, flottant **+160,72 USD**, 0/21 ordres SL natifs (attendu par stratégie); 30j +10,01 %, 14j +17,96 %, 7j +15,55 %.
- Recent40 20h02 Québec : valeur 679,75 USD, variation depuis live +19,98 % / +67,33 USD affichés, 5 positions, flottant **+77,41 USD**, 5/5 stops natifs; 30j +18,79 %, 14j **−6,68 %**, 7j +10,15 %.
- Les montants de PnL **flottant** se rapprochent ou dépassent les gains cumulés depuis live. Ne pas attribuer les +166,61 et +67,33 directement aux trades clôturés sans registre, frais/funding et cashflows.
- Recent40 +67,33 USD et +19,98 % ne se réconcilient pas directement avec valeur actuelle 679,75 USD par une simple soustraction et division. Cela peut refléter bases de calcul/cashflows différents, **pas** une erreur prouvée : reconstitution cashflows nécessaire.

## Source indépendante du sens des positions, datée AVANT les captures
`operations/audits/2026-10-29_bot_by_bot_1715Z.json` (blob `d2481410f230b5b46e5a28725b9d9b6627975dd3`), contrôles à 17:07–17:09 UTC, antérieurs aux captures du soir :
- Swing 21 positions avec owner/mode LIVE, **17 SHORT et 4 LONG** (env. 81 % SHORT en nombre; pas en dollar/risque). La preuve de propriété des 21 positions passe, pas de stop natif par conception. Pas d'attribution PnL asset disponible dans cet audit.
- Recent40 4 positions à 17:09 UTC, **3 SHORT, 1 LONG**, 4/4 protections natives validées individuellement; capture ultérieure 5 positions. Différence de date et de positions normale à vérifier, pas à supprimer.
- **Hypothèse, non démontrée :** exposition SHORT corrélée sur les altcoins en période de mouvements locaux négatifs, malgré un BTC globalement latéral. Les deux profits peuvent être partiellement une même exposition au facteur marché. À vérifier avec montants notionnels historiques, PNL clôturé/flottant et direction.

## Vérification technique ponctuelle
- Railway 28 oct 13:27:19Z pour Swing : log `mode=LIVE fixedStop=NONE`, 56 tests passés, montage volume /data. HTTP lecture source et Control 200; absence de certification individuelle des futurs signaux.
- Recent40 29 oct : déploiement SUCCESS, 1/1 réplique ONLINE et volume /data ; échantillon de requêtes comprend 99 POST /candles 200, 12 statut 499 et 5 statut 400, ainsi que des BrokenPipeError côté serveur. Cela ne prouve pas un flux globalement inactif, mais **l'exploitation n'est pas certifiée sans interruption** par ce seul contrôle. Incidents techniques à traiter dans maintenance, sans modifier ici.
- Les pages JSON live détaillées n'ont pas été récupérées via navigation publique pendant cette passe. Le registre de trades clôturés et cashflows n'a pas été indépendamment relu : ne pas certifier la décomposition du PNL.

## Expérience unique la plus informative, à tester HORS LIGNE (NON FAITE)
**Hypothèse P1 :** pendant un régime BTC/ETH horizontal connu causalement, l'univers de crypto continue à développer des tendances individuelles de quelques heures ou jours ; un filtre directionnel AA + STC de repli peut les exploiter net de coûts.
- Classer régime BTC/ETH uniquement à chaque clôture avant décision (efficacité directionnelle, pente/volatilité et largeur sur 4h) sans étiquettes futures.
- Même univers et calendrier d'existence des contrats, mêmes frais et limites, capital 1000 USD neuf, warm-up causal, contrôle contre tendances courtes simples et positions témoins. Couverture par années 2024/2025/2026, BTC horizontal vs directionnel; LONG/SHORT, PNL réalisé/flottant, sommets→creux MTM, corrélations, durée de sous-pic, bénéfice net par événement et frais/funding.
- Décomposer les différences une par une : recette fixe 1h, adaptation par actif 15/30m, puis score sélection (ablation du score); ensuite sorties AA sans stop vs stop natif ne doivent être comparées qu'avec profils de risque explicitement distincts.
- Test sur départs multiples et holdout chronologique; aucun modèle n'est promu parce qu'il a réussi sur les captures d'octobre. Ne pas utiliser R20 ni modifier un bot existant.

**État : diagnostic source terminé ; hypothèse P1 proposée, PAS TESTÉE; aucune source de rendement future démontrée; aucun déploiement ni modification live, même sur comptes existants.**
