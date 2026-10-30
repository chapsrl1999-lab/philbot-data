## ADDENDUM — suite d'attribution 34 actifs

Les comparateurs additionnels de cette étude ont été exécutés le 29 oct. 2026, documentés dans [v2, 34 actifs](./2026-10-29_swing_stc_aa_attribution_34assets_results_v2.md). Corriger toute impression que l'entrée STC serait sans valeur : **son timing à horizon fixe n'a pas prouvé un avantage**, mais **l'interaction entrée STC + sortie AA** affiche un surplus moyen descriptif d'environ +0,99 point en 2025 et +0,88 point en jan–sept2026 sur 34 actifs (IC95 englobant zéro), avec un contrôle transversal 12 actifs non optimisés. Ce **n'est pas une rentabilité démontrée**, pas une confirmation prospective, et ne déclenche aucun nouveau bot. La simple fermeture "gagnant et plus fort que BTC à72h" a été testée et rejetée. Les résultats et limites historiques plus haut dans ce document restent inchangés.

---

# PhilBot — Étude d'attribution Swing 1h vs Sélectif/Recent40 (29 octobre 2026)
**STATUT : expériences historiques calculées hors ligne ; résultats exploratoires et non validés en live. AUCUN bot modifié. R20 totalement exclu.**

## Verdict en une phrase
Le **timing STC de Swing est favorable en 2024 mais ne démontre pas d'avantage stable en 2025–2026** ; la **durée de détention AA** explique davantage les résultats simulés de certaines fenêtres, MAIS est défavorable dans d'autres ; le **score Sélectif ne démontre pas d'avantage sur ses 240 candidats archivés de septembre 2026**. Ne pas créer de bot ou modifier les deux survivants sur cette base.

## Sources contrôlées
- Swing : version réellement installée Railway `83a20ec47f18b30d31ee5bdc3a58434c03585771`, règles STC(200/75/125/.05), AA(350/5.5), LONG/SHORT, sortie `AA_FLIP` ou délai 720h, **aucun SL natif**. L'implémentation utilisée pour les indicateurs est une transcription Python du Pine, NON une parité certifiée TradingView pour chaque signal.
- Sélectif/Recent40 : version Railway `34501482f85e993e7473a51d6b52bfa03a3e4efb`, `recent40/tests/september_features.json` 240 candidats et percentiles d'origine, `recent40/tests/policy_trace.json` trades admis; modèle septembre gelé, score 0.60, 78 recettes 15m/30m.
- Prix : archives **officielles Binance USD-M perp** 1h (22 cryptos depuis août 2023 jusqu'à septembre 2026) + 15m septembre 2026 (44 cryptos), 877/880 checksums archivés initialement + **3 alias natifs 1000PEPE, 1000SHIB, 1000FLOKI vérifiés séparément**; final **880/880 prix requis récupérés et SHA-256 vérifiés**. Archive source GitHub Actions publique `philbot-data` workflow run `40987169370` et 3 alias run `40987405056`. Les données et calculs complets ne sont pas un ordre exécuté.
- Un essai complémentaire octobre 2026 a récupéré 594/616 archives quotidiennes (1–27 oct), toutes les 22 du 28 octobre étaient absentes lors du contrôle. Une partie des positions aurait été encore ouverte à la borne : **aucune conclusion d'AA exit octobre n'est retenue ici**.
- Les fichiers du simulateur et les registres détaillés existent uniquement dans le laboratoire local lors de cette étude; pas de prétention que le rapport GitHub les reproduit entièrement.

## A — Swing : test du signal d'entrée STC
Étude événementielle, **notionnels égaux par signal**, entrée au prochain open 1h après signal STC/AA; rendement directionnel sur 72h, coûts **0,16 point de % aller-retour**, témoin autres entrées du même actif/mois/direction AA et même statut de BTC, éloignées de 72h. Bootstrap par semaines calendaires ; pas de composition ni d'exposition de portefeuille.
| Période UTC | Signaux | Rendement moyen 72h / signal | Avantage du STC vs témoin | IC95% avantage (points) |
|---|---:|---:|---:|---|
| 2024 | 272 | +2,59 % | +3,16 pts | [+0,75 ; +5,49] |
| 2025 | 213 | −1,17 % | −0,91 pt | [−3,10 ; +1,36] |
| Jan–sept 2026 | 168 | +0,95 % | +1,70 pt | [−0,56 ; +3,66] |
| Jan–sept 2026 et BTC classé latéral | 87 | −0,36 % | +0,48 pt | [−2,05 ; +2,60] |

**Interprétation :** intéressant en 2024, aucune prime stable du timing STC prouvée en 2025/2026; les données ont été exploitées dans des recherches précédentes, pas un OOS vierge.

## B — Swing : test de la patience AA
Sur ces mêmes entrées, sorties au flip AA / 720h comparées aux sorties **fixées 72h**, avec le même coût de 0,16 point pour un round trip. Les durées différentes engendrent un risque et capital immobilisé différents. Ce n'est PAS un comparateur de portefeuille à exposition normalisée.
| Période | Moyenne par entrée, sortie 72h | Moyenne par entrée, sortie AA/720h | Durée médiane AA |
|---|---:|---:|---:|
| 2024 | +2,59 % | +2,84 % | 260,5 h |
| 2025 | −1,17 % | +1,56 % | 503 h |
| Jan–sept 2026 | +0,95 % | +4,46 % | 417 h |
| Juil–sept 2026 quand BTC classé latéral | +1,25 % | +6,24 % | 307 h |

**Contre-exemple obligatoire** : en 2024, lorsque BTC était classé latéral, AA/720h rapportait en moyenne **−3,29 % par entrée**, contre +3,06 % avec 72h. Il ne faut pas conclure « garder plus longtemps gagne toujours ». Le risque des positions sans SL natif, la marge, le financement et les frais effectifs ne sont pas simulés. Ces statistiques sont conditionnées aux événements mesurés et ne sont pas des profits réalisables par capital de 1000 $.

## C — Sélectif : score et contrôle, septembre 2026 seulement
240 candidats gelés ; 92 au percentile >=0.60, 148 refusés par le seuil. 24h contrefactuelles, entrée prochain open 15m, coût **0,12 point %** aller-retour; SL proxy par distance estimée et stop-first intrabougie (pas le replay exact AA_FLIP).
| Groupe de candidats | n | Retour moyen 24h sans sorties dynamiques | Retour moyen avec SL proxy |
|---|---:|---:|---:|
| Score >=0.60 | 92 | **−1,91 %** | **−1,04 %** |
| Score <0.60 | 148 | **−0,02 %** | **+0,01 %** |
Le contrôle apparié (même semaine, direction, timeframe, distance de stop comparable, **85 sélectionnés appariés**) donne un écart moyen **−0,14 point** (IC95% par semaine **[−2,08 ; +1,24]**). Le score **n'a pas démontré de capacité prédictive nette** sur ces rendements à 24h ; cela ne prouve pas qu'il est inutile en 2024/2025 ni avec ses vrais stops/AA.

## D — Vérification du portefeuille reconstitué Sélectif
Parmi les 92 candidats dépassant le seuil dans la fixture de septembre, **76 figurent dans `policy_trace.json` comme opérations**. Les 16 autres ne sont pas nécessairement invalides; la gestion simultanée du portefeuille, la marge et les verrous expliquent que candidat sélectionné ≠ trade admis. Sur ces 76 opérations :
- **20 LONG :** R moyen **+1,52**, taux de réussite ~45%.
- **56 SHORT :** R moyen **−0,40**, taux de réussite ~16%.
- Ensemble **+0,10 R/trade** dans cette fenêtre. Six opérations terminées `FIN` sont incluses; les simulations ne reflètent pas les fills réels de fin octobre. Réalisé/flottant du compte réel NON récupérés dans cette étude.

## Décision
**Rien à déployer, aucune recette à modifier.** Direction de recherche conservée : **un marché BTC latéral peut contenir des tendances locales exploitables; l'élément à expliquer est la différence entre opportunité, timing d'entrée et temps d'exposition**, et non une nouvelle optimisation STC. Priorité scientifique : attribuer correctement la source du PnL *réel* et la contribution de la sortie à une exposition comparable, avant de prétendre que la durée AA ou le score est une source de rendement démontrée.

### Limites non négociables
Survivorship de l'univers 22 actifs, pas de parité TradingView complète, pas de notionnel du portefeuille, funding/exécution venue/SL/liquidation non simulés, inventaire ouvert et corrélation entre cryptos, intervalle de confiance conditionnel à des paramètres connus; 2026 **pas hors échantillon vierge**. Les gains présentés comme « par signal » ne peuvent pas être additionnés pour annoncer un rendement de compte. Tous les contrôles sont observationnels, pas une expérience aléatoire ni un test futur.
