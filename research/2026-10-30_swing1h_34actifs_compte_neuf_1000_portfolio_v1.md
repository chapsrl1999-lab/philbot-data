# PhilBot — Replay en compte neuf, Swing 1h, univers réduit 34 actifs
Date : 30 octobre 2026 (Québec). **REPLAY HISTORIQUE OFFLINE, NON VALIDÉ POUR TRADING LIVE.** Aucune modification de bot, service ou compte. **R20 non utilisé, ni témoin ni variante.**

## Pourquoi ce replay
Les précédents résultats « +0,88 point par événement » n'indiquaient ni capital final ni PnL$ d'un portefeuille. Le présent rapport présente les capitaux réels de **la simulation**, frais et flottant, chaque scénario depuis **un véritable compte virtuel neuf de 1 000 USD** et zéro position, et non une courbe continue renormalisée.

## Résultats principaux — hypothèses de simulation décrites ci-dessous
| Départ UTC, compte neuf 1000 USD | Sortie théorique | Capital final USD | PNL % | Drawdown maximal avec flottant | PF en dollars | Trades | Frais USD | Moyenne hebdo composée |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| 2024-01-01 | 2025-01-01 | **2267,25** | **+126,73%** | **70,99%** | 1,37 | 352 | 68,02 | +1,53% |
| 2025-01-01 | 2026-01-01 | **1753,95** | **+75,39%** | **42,25%** | 1,21 | 285 | 69,12 | +1,07% |
| 2026-01-01 | 2026-10-01 | **3828,82** | **+282,88%** | **27,74%** | 2,30 | 210 | 84,00 (arrondi) | +3,41% |
| 2026-07-01 | 2026-10-01 | **1984,95** | **+98,49%** | **25,04%** | 2,92 | 82 | 22,86 | +5,02% |
| 2026-10-01 | 2026-10-28 (prix au 27 oct. 23h UTC) | **912,76** | **−8,72%** | **18,66%** | 0,59 | 34 | 6,91 | −1,81% |
| 2026-01-01 | 2026-10-28 | **3417,91** | **+241,79%** | **27,74%** | 1,82 | 242 | 105,72 | +2,83% |
| 2024-01-01 | 2026-10-28 compte CONTINU distinct | **9284,53** | **+828,45%** | **70,99%** | 1,47 | 862 | 468,90 | +1,51% |

**Très important :** chiffres NETS DE FRAIS / GLISSEMENT **MODÉLISÉS**, mais **PAS nets du funding réel ni des coûts complets venue**. La simulation ne certifie pas les profits effectivement exécutables ni le rendement futur. Le choix des actifs et les périodes ont déjà été influencés par recherches historiques. Le bot live BloFin utilise un autre univers (65 actifs); ce replay n'est PAS son véritable compte.

## Causalité et exécution approximative
- 34 cryptos, subset seulement, toutes avec données officielles Binance USD-M 1h du 1 août 2023 au 27 oct 2026, **vérifiées sans trou et checksums SHA256** sur les archives mensuelles et journalières. Les 34 incluent 22 initiales et 12 nouvelles de l'analyse « interaction STC + AA ».
- **Indicateurs causaux préchauffés** depuis août 2023, mais états des témoins directionnels virtuels **remis à zéro à chaque date de compte neuf**. Pas de position réelle héritée; sortie de période par liquidation théorique des positions ouvertes à la dernière clôture connue (pas un fill de venue).
- STC `200/75/125/0,05`, AA `350/5,5`, zones `25/75`, recul `9` identiques sur chaque actif. Entrée au prochain `open` 1h après signal confirmé; sortie AA_FLIP ou `720h` selon l'algorithme original. **Aucun stop-loss fixe.**
- Sizing : risque de référence `1,75% de l'equity` entre entrée et bande AA **SANS STOP**, budget de risque ouvert à l'entrée 40%, par sens 28%, marge projetée 60%, levier max 7x. Ordres simultanés en ordre alphabétique (sensibilité de priorité inversée calculée).
- Hypothèses coûts : `0,06% taker par côté` plus `0,02% slippage par côté`. Funding réel **non obtenu et assumé nul**, liquidation et limites de tailles/arrondis/levier par actif non reproduits.
- Capital total marqué chaque heure avec flottant + provision de frais de sortie. PF$ et PF R recalculés du journal des trades ; PNL$ des trades somme exacte à variation du capital final dans les huit comptes, tolérance inférieure à 1e−7 USD. Drawdown calculé avec floating, durée sous sommet et PNL par semaine/mois disponibles dans HTML+JSON.
- Contrôle des signaux : **652/654** événements précédemment archivés (22 actifs, période d'étude) correspondent précisément à l'actif, au sens et à l'heure; deux événements `FET SHORT` et `XLM LONG` de l'ancien registre surviennent à la même bougie que l'expiration virtuelle de 720h du précédent trade. Le Pine live interdit une ré-entrée sur la bougie de sortie, et le présent replay suit cette interdiction. **Parité 100% avec TradingView/BloFin non certifiée**, ne pas intégrer au Replay Maître sans comparaison complète et tolérances fixées.

## Robustesse et limites de généralisation
Sous-ensemble historique (compte neuf, période identique) :
- **2025 :** premiers 22 actifs → 2074,38 USD / DD28,86%; **12 autres actifs** → 659,92 USD / DD41,51%. ***Le résultat change fortement avec l'univers***, critère de fragilité.
- **Juil–sept 2026 :** 22 premiers → 1376,76 USD / DD22,56%; 12 autres → 1442,55 USD / DD13,82%; réunis 34 → 1984,95 USD / DD25,04%. Les comptes séparés ne doivent pas être additionnés comme un portefeuille unique.
- **Frais + slippage doublés, juil–sept2026** : 1943,34 USD final / DD25,08%.
- **Sizing réduit moitié, juil–sept2026** : 1406,21 USD final / DD17,60%.
- **Inversion de priorité des signaux, juil–sept2026** : 1985,01 USD final / DD25,04%.
- Sur juillet–septembre 2026, cinq plus gros gagnants totalisent environ **+609 USD**, sur **+985 USD** de PNL total du compte. Résultat concentré en quelques mouvements, ne pas extrapoler une régularité hebdomadaire.
- **Octobre 2026 nouveau compte** : **912,76 USD, PF0,59**, une période récente négative. Ce compte **ne possède pas** les positions SHORT héritées de septembre par le compte Swing live, donc ce n'est pas la performance réelle de Swing.

## Décision et prochaine vérification nécessaire
Ce replay démontre uniquement qu'un moteur historiquement connu, avec une même recette STC + AA et une gestion de position de type Swing, **peut être profitable dans le modèle de compte** sur certaines périodes y compris juil–sept2026. Cela n'identifie **PAS** un nouvel alpha exploitable hors échantillon, ne prouve **PAS** la survie aux drawdowns ou la liquidation BloFin, ne qualifie **PAS** un bot de range.
À ne pas mettre live sur cette base. Avant toute promotion : comparaison complète des décisions TradingView et fills, marges/liquidations exactes, funding sur heures détenues, levier tiers/minimums et validation prospective strictement après gel, avec vrai compte de 1000 USD et plusieurs départs.
**Dossier de preuves local :** `philbot_replay_swing1h_34actifs_compte1000_2026.html` (2,35 Mo, fonctionne hors ligne dans Chrome, navigation entre 8 comptes, graphique, courbes, semaines, mois, transactions), `philbot_compte1000_swing34_audit.json` (registres et métriques), script Python recherche `swing_replay.py`. Ces fichiers ont été produits et contrôlés pendant la conversation du 30 octobre, **pas déployés dans un service live**.
