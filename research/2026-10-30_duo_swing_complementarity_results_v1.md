# DUO et Swing — complémentarité historique, 30 octobre 2026

Verdict: **DUO retenu pour validation comme candidat complémentaire, non validé en live**. Recherche hors ligne uniquement. Aucune modification de bots, comptes, risque, stratégies ou ordres ; R20 complètement exclu.

## Sources exactes
DUO: preuves originales du 25 octobre PhilBot_Recherche_Independante_Preuve_et_Code.zip, courbe 5 min curve_duo_positions18_risk0.0075_continuous.npz et trades_duo_positions18_risk0.0075_continuous.csv. Registre de 2 157 trades, profit net théorique total +4 908,098973 USD, frais modèles 631,534456 USD, PF dollars 1,28516; dernier cash 5 908,098973 USD vérifié par somme PNL des trades.
Swing: scénario 2024–octobre 2026 continu du replay 34 actifs du 30 octobre, PAS le bot BloFin live avec 65 actifs. Tous les résultats historiques sont des simulations déjà connues, pas un nouveau test prospectif.

Courbes marquées au **même timestamp** : 23 h America/Toronto quotidien, 04:00 UTC hiver, 03:00 UTC été, correction DST AVANT calcul. Horizon de comparaison 1 janvier 2024 au 24 octobre 2026, 1 028 marques MTM quotidiennes et 147 semaines.

## Portefeuilles simulés continus, 1 000 USD au départ

| Moteur | Capital final 24 oct 2026 | PNL % | DD MTM quotidien | Pire semaine |
|---|---:|---:|---:|---:|
| Swing seul 34 actifs | 9 183,93 USD | +818,39% | −69,45% | −27,99% |
| DUO seul | 5 976,76 USD | +497,68% | −29,83% | −20,81% |
| DUO+Swing poids fixe 50/50 | 7 580,34 USD | +658,03% | −34,06% | −21,01% |

**Important :** le 50/50 est un INDICE mathématique des deux comptes (500 USD théoriques pour chacun), pas un replay réellement exécutable à ces tailles et pas un compte partagé. Avec le flottant en 5m, DUO a connu −31,04% DD ; Swing a connu −70,99% intrajournalier dans son propre replay. Le tableau est sur marquage quotidien, n'égale pas ces risques intra-période.

## Effet de compensation, semaines synchronisées
- 2024 : DUO gagnant 16 fois parmi 29 semaines Swing perdantes : 55%.
- 2025 : 16 parmi 25 : 64%.
- 2026 : 15 parmi 23 : 65%.
- Total 47 parmi 77 : **61%**. Il existe encore 30 semaines où les deux perdent. Corrélation hebdomadaire générale +0,054 ; 2026 +0,408, ce n'est pas une couverture fiable.

## BTC latéral, définition causale avant semaine
Variation absolue du rendement BTC sur les 14 jours passés ≤5%, mesurée avant le début de semaine, source historique BTC Binance 1h. Sur 76 semaines ainsi classées, DUO positif dans 48 (63,2%). Swing négatif pendant 42 semaines latérales ; DUO positif 27/42 (64,3%).

Moyenne hebdomadaire ARITHMÉTIQUE, pas composée : 2024 (25 semaines) Swing −2,05%, DUO +3,02%; 2025 (26 semaines) Swing +1,62%, DUO +1,59%; 2026 (25 semaines) Swing +3,76%, DUO +2,89%. Le régime BTC n'a pas été négocié en live.

## Risque / résultats négatifs qu'il ne faut jamais effacer
DUO avait perdu dans d'autres régimes : 2021 −62,91%, PF$0,619; 2022 +3,80%, PF$1,014; 2023 −28,72%, PF$0,903. En conditions de coûts dégradés (0,10% frais par côté +0,05% slippage par côté + charge synthétique 0,03% notionnel/jour), résultat annuel DUO : 2024 +11,51% PF$1,034; 2025 +18,04% PF$1,063; 2026 +124,58% PF$1,326. Par conséquent marge très fragile en 2024 et 2025. Funding réel, liquidations, capacité des sous-comptes et exécution native non validés.

## Décision
Retenir **DUO**, ancien moteur incluant mean-reversion conditionnelle, pour étude de complémentarité, PAS pour live. Aucun nouveau bot. Pour obtenir une qualification, comparer avec des comptes neufs réellement exécutables de 500+500 USD en modélisant minimums d'ordre, taille, financement, marge, liquidation, et confronter au régime défavorable 2021/23. Ensuite demander un test prospectif figé après le 30 octobre 2026. Si l'avantage s'effondre, rejet sans grille de paramètres post hoc.

Les sources, scripts, courbes quotidiennes et hebdomadaires, audits JSON, rapports historiques du 25 octobre et SHA256 des sources sont dans philbot_duo_swing_complementarite_preuves_20261030.zip. Le rapport visuel autonome est philbot_duo_swing_complementarite_20261030.html. Les deux ne sont pas installés en production.

État : étude temporelle et régime BTC calculés, originaux récupérés, cash DUO recoupé; combinaison réelle et rentabilité future inconnues; zéro modification live.