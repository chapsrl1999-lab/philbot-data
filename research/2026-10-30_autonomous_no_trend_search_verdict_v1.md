# PhilBot — recherche du troisième moteur sans forte tendance, test du 30 octobre 2026

**VERDICT : AUCUN DES DEUX MOTEURS TESTÉS N'EST QUALIFIÉ.** La prime de volatilité des options BTC présente en outre un changement de signe défavorable pendant le BTC latéral en 2026. Résultats négatifs **conservés**, sans nouvelle optimisation. AUCUNE modification live, aucun ordre, aucun déploiement, **R20 totalement exclu**.

## Source et protocole AVANT chiffres
- BOCPD / filtre bayésien de ruptures de régime (première architecture hebdomadaire PhilBot lot104, synthétique seulement avant ce travail), propre adaptation de Adams/MacKay : protocole déjà vérifié `research/2026-10-30_bocpd_regime_autonome_protocole_v1.md`, commit `1d31a27e7b7e7bd1c85b4807b01ffed6f7fbf066`; source scientifique Tsaknaki et al., Quantitative Finance 2025, DOI 10.1080/14697688.2024.2337300, **sur NASDAQ order flow**, PAS une preuve de crypto.
- Prime de risque transversal BTC DVOL, idée distincte de funding/price-spread : protocole `research/2026-10-30_volatility_beta_relative_risk_protocol_v1.md`, commit `8f9c75a0d1f9cac9b37a3211cbb33369e0e962f6`; littérature SeungOh Han (2026) DOI10.1016/j.ribaf.2026.103374. Le `5.221% weekly` publié est **un alpha factor-adjusted de chercheurs**, ni profit hebdomadaire exécutable ni backtest de PhilBot.
- Écran de volatilité implicite vs réalisée : protocole `research/2026-10-30_dvol_forward_variance_premium_prereg_v1.md`, commit `862e6986043931ea2b73cdd7abde65aa17d7f712`; il mesure un phénomène, PAS les PNL des options.

## 1. BOCPD : un système autonome qui décide LONG/SHORT/FLAT
8 cryptos (BTC ETH SOL XRP ADA DOGE AVAX LINK), chandelles4h regroupées à partir des 1h officielles Binance futures. Pré-chauffage/échelle sur août–déc2023 uniquement ; hazard 1/24 choisi sur **log-score prédictif en 2024 seulement** face aux autres 1/72,1/168 ; pas de choix sur PNL. L'entrée attend une 4h entière après signal et tient la suivante, seuil de probabilité0.60 pour mouvement >40bp, coût0.20% aller-retour et stress0.40. Compte neuf 1000 USDT par année; notionnel 25% de l'equity par signal, max4 positions, aucun financement ou liquidation venue.
| Date du nouveau compte | Capital fin USD | Rdt net simulé | DD MTM (4h) | PF$ | Trades | Capital stress USD |
| 2024-01-01 | **821,55** | **−17,85%** | 27,60% | 0,890 | 783 | **555,13** |
| 2025-01-01 | **613,85** | **−38,62%** | 43,28% | 0,774 | 775 | **416,29** |
| 2026-01-01 → 2026-09-30 | **765,40** | **−23,46%** | 32,12% | 0,713 | 482 | **601,22** |
Sous BTC plat classé causalement sur le rendement BTC des 14 jours précédents ≤5% absolu : en 2025 446 événements, rendement moyen de notionnel **−0,403%** ; en 2026 189 événements **−0,402%**. Formulation figée **REJETÉE**. L'année 2026 juil–sept seule +7,62% (PF1.244 sur182 trades) mais coût stress entraîne 982,75 USD et ne sauve pas l'architecture; ne pas sélectionner cette fenêtre.

## 2. Bêta de volatilité des options, portefeuilles dollar-neutres
Source Deribit : **36 mois/26 304 heures** de DVOL BTC officiel d'oct2023 à sept2026, SHA256 de chacun des 36 fichiers revérifiés à partir du manifeste original du laboratoire lot69. 34 cryptos Binance USD-M 1h avec archives 2023–2026, séries datées vérifiées. Rang du bêta sur variation DVOL vs rendement quotidien passé, fenêtre **180 jours** connus, recalcul le lundi00 UTC. Une heure après, portefeuille de 12 LONG de sensibilité intermédiaire contre22 SHORT de sensibilité extrême (50% notionnel chaque, brut1×, net0). Exécuter uniquement si |variation BTC 14 jours passés|<=5%; coût0,16% aller-retour; stress0,30%; funding absent. Sous-comptes neufs1000 USD, zéro position héritée.
| Période | Semaines négociées classées BTC latéral | Capital base USD | DD MTM horaire | PF paniers | Capital stress USD |
| 2024 (nécessite 180 jours DVOL, pas année complète) | 17 | **1066,45** | 5,99% | 1,754 | 1041,44 |
| 2025 | 30 | **995,03** | 8,57% | 0,971 | **954,06** |
| Janv–sept2026 | 22 | **1054,67** | 7,14% | 1,631 | **1022,73** |
La méthode ne démontre donc ni >5%/semaine ni profit en 2025 : **REJETÉE** sous le critère figé, malgré l'alpha publié sur un univers différent. En 2024 le retour commence seulement après le préchauffage180j, la comparaison n'est PAS à couverture annuelle égale.

## 3. L'option est-elle au moins économiquement chère pendant les régimes plats ?
Comparer le DVOL BTC 30 jours (implied annual volatility) connu chaque lundi00UTC à la volatilité annualisée **réalisée pendant les 720 heures futures** d'un perp BTC. Fenêtres de 30jours qui se chevauchent, bootstrap mois (pas observation indépendante). BTC plat connu sur14jours à chaque départ. Aucun dérivé négocié ou supposé executable.
| Année, BTC plat au départ | N lundis maturés | IV moyenne annualisée | Réalisée future annualisée | IV moins réalisée | N prime IV>RV |
| 2024 | 23 | 57,97% | 48,47% | +9,49 points vol | **20/23** |
| 2025 | 31 | 45,99% | 42,53% | +3,46 points vol | **22/31** |
| 2026 (seulement observations arrivées à maturité d'ici sept30) | 19 | 42,82% | **44,96%** | **−2,14 points vol** | **6/19** |
Le critère antérieur « prime moyenne ET médiane positive en 2025 ET 2026 sous BTC latéral » **ÉCHOUE en 2026**. Dans **13/19** semaines 2026 classées plates, la volatilité réalisée30j > IV30 mesurée avant. **Ne pas présenter la vente d'options comme un moteur gagnant en range.** Ce diagnostic ne permet pas non plus de présenter l'achat d'options comme profitable.

## Contrôles numériques
- Calculs effectués localement avec Python/scipy sur sources historiques revérifiées.
- **26 comptes/scénarios** réconciliés à la somme des trades/semaines (tolérance <1e-6 USD) et valeurs finales de chaque courbe MTM; journal entier et SHA256 des sources inclus dans l'archive technique.
- Le dashboard HTML autonome `philbot_recherche_deux_mecanismes_20261030.html` et l'archive `philbot_recherche_deux_mecanismes_preuves_20261030.zip` ont été créés en conversation et testés : archive ZIP intègre, rendu Chromium mobile sans erreur JS ni dépassement horizontal.
- Pas de funding/lot/marge/liquidation/slippage réellement observé, ni book Deribit, ni parité des fills ; 2025 et 2026 historiquement connus par le projet ne sont PAS un vrai test prospectif jamais observé.

## Décision
**Aucun troisième moteur qualifié, aucun nouveau bot créé.** Deux propositions de mécanismes ont été falsifiées sur le rendement de compte, et une troisième source de prime a échoué sur 2026 BTC plat. Ne pas inverser les signaux ni ajuster les seuils après avoir vu les PNL. La prochaine recherche ne doit pas recycler ces architectures sans donnée réellement nouvelle ni mécanisme économique distinct.
