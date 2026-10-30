# PhilBot — Nouvel angle EXTERNE : information publique et pouvoir prédictif crypto
30 octobre 2026. **ÉTUDE EFFECTUÉE, PISTE ÉCONOMIQUE NOUVELLE, MAIS BOT NON QUALIFIÉ.** Lecture seule ; aucun ordre, service, compte, configuration de risque ou stratégie live modifié. **R20 complètement exclu.**

## Pourquoi cette famille est réellement différente
Après >104 familles/rounds PhilBot documentés (STC/AlgoAlpha, retour à moyenne, funding/spreads, order-flow et régimes), explorer un mécanisme où le signal provient de **l'analyse point-in-time d'informations et catalyseurs publics** avant le rendement, et non du seul cours. Un préprint académique de 2026 propose une telle approche sur un panel quotidien de 100 cryptos. La promesse de profit n'est PAS adoptée sans contrôle.

Sources externes pertinentes :
- Xinyu Sun, Zhiyi Wang, Huaxi Zhang, *Agentic AI Nowcasting and Cryptocurrency Return Predictability* (SSRN 7231679, posted 5 août 2026), 9300 évaluations sur 93 jours du 29 avril au 30 juillet 2026. Les auteurs prétendent une collecte prospective quotidienne en temps réel. URL: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7231679 .
- Dépôt public des auteurs : https://github.com/Moonooo24/agentic-ai-crypto-nowcasting ; score panel `data/crypto_panel_data_public.csv` et résultats `results/tables/execution_portfolio_daily.csv`; Git blob exact de la table daily `4dbd7a78d94fc0ce412b7f1c164b2f2953040f32`.
- Ba Chu et Ilias Tsiakas, *Media Coverage and the Cross-Section of Cryptocurrency Returns* (juin 2026, SSRN 6805101), fondée sur **7.6 millions d'articles** ; couverture large / répétée corrélée à rendements futurs plus faibles, **nouveauté** de l'information corrélée à des rendements futurs plus forts. Ce résultat observationnel est distinct de la stratégie de Sun et n'est PAS une validation de notre projet. https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6805101 .
- Yifei Wang et Zhenling Pang, *Predictability on the Move* (posted 6 oct 2026, SSRN 7556359) : 1043 signaux et jusqu'à 750960 candidats ; tests globaux de sélection échouent initialement à démontrer un alpha stable, mais des fenêtres glissantes révèlent des signaux changeants, en particulier liquidité/activité; résultat uniquement en coûts bas. Ne justifie pas un nouveau réglage de moteur déjà rejeté. https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7556359 .

## PROVENANCE — avertissement critique
Les scores sont décrits par les auteurs comme produits AVANT les rendements futurs. **Impossible de vérifier cela indépendamment** : le repository Github des scores a été publié le **5 août 2026**, et mis à jour le **12 août 2026**, donc après la dernière date d'étude (30 juillet 2026). Les auteurs ne publient **ni prompts, ni journaux d'agent horodatés, ni narrations ni rendements par crypto/fills**. L'archive publique ne démontre pas à elle seule une validation prospective. Ne pas inférer qu'ils ont triché ; **niveau de preuve insuffisant pour PhilBot live**.

## Notre expérience écrite AVANT le regroupement par marché BTC plat
Protocole source vérifié dans ce repo : `research/2026-10-30_information_publique_signal_prereg.md`, commit `f6b9b6e2fe8b35e89544d36f1405b18a46332518`.
- Reprendre UNIQUEMENT les 93 rendements d'exécution Binance avec **entrée 15min après signal**, coût nominal publié **25bp par jambe**, funding **estimé par les auteurs**, variante stress **50bp par jambe**.
- Le portefeuille publié a 100% notionnel LONG top10 + 100% notionnel SHORT bottom10 = **2× brut**. Pour simuler un **nouveau capital théorique de 1000 USD avec 1× brut et delta-neutre**, investir 50% LONG/50% SHORT, retours quotidiens = 0.5 × les retours publiés. Cette conversion est un indice arithmétique, **pas un replay de vingt fills d'un vrai compte**.
- Définir BTC faiblement directionnel de manière **causale** : |variation BTCUSDT sur les 14 jours précédents la décision 00UTC|<=5%. Données Binance USD-M perp 1h d'archives officielles SHA256, préchauffage antérieur 2026 ; aucun futur pour déterminer le jour admissible. **47/93 jours admissibles**, cash les 46 autres.
- Calculer compte composé, PF$ de journées de portefeuille (pas PF des trades), gain, DD aux clôtures quotidiennes, chaque mois fixé, corrélation BTC quotidienne, stress coûts. **Aucune optimisation post-résultat**.
- Pré-enregistrement impose PNL total >0, PNL positif en marché peu directionnel, PF sous coûts stress >=1.5 et aucune fenêtre mensuelle en perte.

## Résultats vérifiés de la reconstruction sur compte 1000 USD fictif
| Scénario | Fin USD | PNL net simulé | DD au close quotidien | PF$ journées | Fréquence active |
|---|---:|---:|---:|---:|---:|
| Tous 93 jours, coûts auteurs 25bp/jambe | **1422.48** | **+42.25%** | **12.25%** | **1.673** | 93 jours |
| Tous 93 jours, stress 50bp/jambe | **1128.00** | **+12.80%** | **13.68%** | **1.199** | 93 jours |
| 47 jours de BTC plat, cash le reste, 25bp/jambe | **1166.69** | **+16.67%** | **12.25%** | **1.602** | 47 jours |
| 47 jours de BTC plat, stress 50bp/jambe | **1037.56** | **+3.76%** | **13.68%** | **1.124** | 47 jours |

Fenêtres calendaires, chacune calculée comme un NOUVEAU compte de 1000 USD :
- 29 avr–31 mai : +11.86% base, +3.02% stress, PF base 2.15.
- Juin : +29.85% base, +20.53% stress, PF base 2.858.
- Juillet 1–30 : **−2.06% base** et **−9.16% stress**, PF base 0.913. **Pire jour −10.88% sur le portefeuille 1×**, 24 juillet.
- 47 jours BTC plat, moyenne par jour ACTIF +0.352% base, +0.102% stress. Bootstrap des semaines synchronisées, 12 semaines, intervalle95% **[−0.127%; +0.798%]** du rendement moyen journalier base : inclut zéro.
- Corrélation **−0.031** entre retours quotidiens BTC et retours stratégie tous jours dans cette petite période. Ce n'est ni l'indépendance prouvée avec Swing/Sélectif ni l'absence de facteur commun.

**Gate pré-enregistré : ÉCHEC** — juillet perdant et PF stress du sous-ensemble BTC plat 1.124 <1.5. **Rien à promouvoir en live.** Source externe sur seulement 93 jours (aucun 2024/2025), aucune date postérieure à fin juillet dans l'étude publiée, donc aucun vrai test multi-années ni futur vierge.

## Audit de l'arithmétique
- Source CSV 93 lignes au filtre exact `delay_minutes=15, portfolio=perpetual_long_short_after_funding_net_25bps`, et 93 lignes stress `net_50bps`.
- Rendements CSV recopiés dans le script de preuve arrondis à 10⁻⁶ en fraction, erreur maximale **< 5×10⁻⁷ par observation** ; moyenne originale du rendement **2×** net25 `0.007994584457432783`, audit arrondi `0.007994548387096774`.
- Mêmes 93 dates et horizons pour données BTC ; vérification SHA256 de la source initiale des ZIP Binance, sans fuite de fichiers de stratégie PhilBot. Recalcul de 4 courbes MTM journalières depuis 1000 USD, registre de 93 journées.
- Fichiers livrés dans le conteneur de conversation : `philbot_information_publique_recherche_20261030.html` (rapport Chrome autonome), `philbot_information_publique_preuves_20261030.zip` (script, CSV jours, JSON complet, manifest SHA256). Ces outputs ne sont pas déployés dans un serveur.
- Contraintes manquantes : vrais fills des 20 positions/jour (~50 USD notionnels chacune), taille minimale, marge, arrondis, liquidation, funding indépendamment vérifié, DD intrajournalier, prix disponibles au seuil de retard, latence, registre d'ordres.

## Décision et prochain travail rationnel
La source **information publique / nouveauté catalyseurs** mérite d'être étudiée **comme hypothèse économique distincte**, car l'observation narrative serait disponible au moment du trade et pourrait, en principe, prévoir les décalages entre cryptos même sans tendance générale. Mais l'implémentation universitaire **n'est PAS validée comme bot PhilBot** sous notre propre gate, et la provenance temporelle publique laisse un blocage majeur. **Ne pas optimiser son 25bp, mois ou seuil 14j à posteriori.**

Si cette famille est poursuivie, **première preuve à obtenir** : collecter réellement et horodater chaque signal d'information et sa source *avant* les résultats futurs (monitoring prospective sans ordre ni risque), avec protocole gelé et témoin prix-only, puis vérifier gains par fenêtre de marché, 2025/2026 historique indépendant si données d'information point-in-time disponibles, frais en taille de compte. Ce n'est pas fait ni planifié en tâche de fond : ne pas prétendre le contraire.
**État : vérification de source externe + 93 rendements reconstruits terminées ; aucune validation d'une stratégie rentable et déployable ; zéro modification de bots live et R20 exclu.**
