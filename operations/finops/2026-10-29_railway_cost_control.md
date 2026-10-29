# Contrôle FinOps PhilBot — jeudi 29 octobre 2026

**Preuves observées** : Railway projets `zesty-learning` (30 services), `philbot-rafale2-dp60` (2), `philbot-recent40-observer` (1) et `philbot-r20-shadow` (2) ; mesures `get_service_metrics` 24h et 168h couvrant les fenêtres se terminant vers **2026-10-29 12:48–12:52 UTC** (08:48–08:52 Québec). Métrologie à la minute, chaque moyenne est une moyenne des points de la fenêtre et peut comprendre des redéploiements/downtime ; service `SUCCESS` n'est pas un indicateur de capacité métier. Inventaire `describe_environment` (aucun changement staged dans zesty/recent40/r20 ; patch ancien staged DP60 sans contenu exposé, laissé intact), `environment_status`, `describe_service`, journaux `get_logs`. 35/35 services couverts 24 h et 7 jours. **Seule projection CPU+RAM**, sans stockage/egress/abonnement, et non la facture.

## TARIFS ET QUALIFICATION

Railway officiel : **20 USD / vCPU-mois** ; **10 USD / Go RAM-mois** ; **0,05 USD / Go egress** ; **0,15 USD / Go-mois volume** ; facturation prorata du temps. https://docs.railway.com/pricing/plans . `équiv. USD/mois` = `20 × CPU moyen + 10 × RAM moyenne` **sous hypothèse purement illustrative de maintien de cette même charge pendant 30 jours**. Les colonnes RX/TX sont les **valeurs moyennes brutes de `NETWORK_RX_GB` / `NETWORK_TX_GB` par point** ; **ne pas multiplier par 30 jours comme des compteurs de GB transmis sans vérification du pas et de la sémantique**. Un réseau sortant anormal n'est pas établi simplement par la RX. Les volumes Railway sont présents et préservés, les capacités allouées ne prouvent pas le Go réellement facturé.

**Somme des équivalents CPU+RAM aux fenêtres** : 24h **83.29 USD/mois**, 7j **76.48 USD/mois** ; ces sommes ne sont pas une prévision d'encaissement et **incluent des travaux de recherche déjà terminés**, l'arrêt global Railway du 28 oct et des déploiements récents. On ne les assimile ni à la facture réelle ni à une dépense future certaine. Chiffrage exact du cycle par facture seulement.

## RELEVÉS PAR SERVICE ET PROJET

| Projet | Service | CPU moyen 24h | RAM Go 24h | RX GB moy. 24h | TX GB moy. 24h | CPU moyen 7j | RAM Go 7j | RX GB moy. 7j | TX GB moy. 7j | équiv. 24h USD/mois | équiv. 7j USD/mois | Classe de service |
|:--|:--|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|:--|
| zesty | HWR hybrid-r4-read-check | 0.302414 | 2.712559 | 0.001099 | 0.000271 | 0.421727 | 3.22379 | 0.001052 | 0.000255 | 33.17 | 40.67 | LIVE/volume |
| zesty | philbot-signer CONTINUATION | 0.078835 | 0.2365 | 0.000025 | 0.000025 | 0.102604 | 0.235864 | 0.000028 | 0.000033 | 3.94 | 4.41 | LIVE/volume |
| zesty | philbot-outsider-hl-validation | 0.012106 | 0.312672 | 0.00026 | 0.000104 | 0.009584 | 0.323888 | 0.000256 | 0.000103 | 3.37 | 3.43 | LIVE/volume |
| zesty | philbot-health | 0.003755 | 0.085335 | 0.000373 | 0.000052 | 0.004149 | 0.089157 | 0.000476 | 0.000053 | 0.93 | 0.97 | PROTECTION/volume |
| zesty | philbot-guardian | 0.002306 | 0.08935 | 0.000036 | 0.000012 | 0.002296 | 0.08426 | 0.000035 | 0.000014 | 0.94 | 0.89 | PROTECTION/volume |
| zesty | philbot-trains-bitunix | 0.000032 | 0.106894 | 4.88e-7 | 9.70e-8 | 0.000015 | 0.032939 | 1.93e-7 | 3.70e-8 | 1.07 | 0.33 | SHADOW/volume |
| zesty | philbot-rafale2-swing-shadow | 0.000503 | 0.056375 | 0.000072 | 0.000035 | 0.0041 | 0.063684 | 0.004183 | 0.000081 | 0.57 | 0.72 | SHADOW/volume |
| zesty | hybrid-hwr-qualify-node22-20261010 | 0.005351 | 0.095299 | 0.000973 | 0.000066 | 0.004638 | 0.078695 | 0.000809 | 0.000096 | 1.06 | 0.88 | QUALIFICATION |
| zesty | philbot-r20-hl | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0.00 | 0.00 | SUCCESS/aucune consommation mesurée |
| zesty | philbot-rafale2-hl | 0.000577 | 0.096274 | 0.000035 | 0.000051 | 0.000398 | 0.109525 | 0.000032 | 0.000056 | 0.97 | 1.10 | LIVE/volume |
| zesty | philbot-rafale2-bitunix | 0.000643 | 0.085521 | 0.000013 | 0.000037 | 0.000585 | 0.097437 | 0.000015 | 0.000043 | 0.87 | 0.99 | volume |
| zesty | philbot-rafale2-blofin | 0.003671 | 0.166772 | 0.000419 | 0.00004 | 0.002777 | 0.152546 | 0.000315 | 0.000032 | 1.74 | 1.58 | volume |
| zesty | philbot-snapback-v10r1 | 0.005685 | 0.194491 | 0.000013 | 0.000011 | 0.005734 | 0.204627 | 0.000014 | 0.000011 | 2.06 | 2.16 | LIVE/volume |
| zesty | philbot-snapback | 0.000948 | 0.137106 | 0.000012 | 0.000006 | 0.000602 | 0.165953 | 0.000007 | 0.000006 | 1.39 | 1.67 | LIVE |
| zesty | philbot-bitunix-phoenix-shadow-v1 | 0.00315 | 0.058336 | 0.000506 | 0.000096 | 0.011535 | 0.095451 | 0.000624 | 0.004448 | 0.65 | 1.19 | SHADOW/PAS VOLUME |
| zesty | philbot-bitunix-phoenix-dual-shadow | 0.003066 | 0.055692 | 0.0005 | 0.000044 | 0.004329 | 0.099542 | 0.000505 | 0.000044 | 0.62 | 1.08 | SHADOW/PAS VOLUME |
| zesty | philbot-grid-range-v1 | 0.000037 | 0.475097 | 0.000047 | 0.000001 | 0.000005 | 0.067911 | 0.000007 | 1.65e-7 | 4.75 | 0.68 | JOB FINI 1h=0 |
| zesty | philbot-reversal-research | 0.000455 | 1.518651 | 0.000198 | 0.000005 | 0.000065 | 0.217079 | 0.000028 | 6.56e-7 | 15.20 | 2.17 | JOB FINI 1h=0 |
| zesty | philbot-personal-snapshots | 0.000002 | 0.001017 | 3.00e-9 | 3.00e-9 | 0.000004 | 0.01714 | 6.00e-9 | 3.00e-9 | 0.01 | 0.17 | CRON |
| zesty | philbot-r20-shadow-probe | 0.000147 | 0.019044 | 0.000025 | 0.000004 | 0.000153 | 0.019235 | 0.000025 | 0.000004 | 0.19 | 0.20 | SHADOW PROBE |
| zesty | venue-research-rafale2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0.00 | 0.00 | FONCTION/0 |
| zesty | philbot-personal-readonly | 0.000203 | 0.017778 | 0.000003 | 0.000002 | 0.000263 | 0.02106 | 0.000003 | 0.000002 | 0.18 | 0.22 | READONLY |
| zesty | philbot-range-wave-readonly | 0.000308 | 0.010437 | 0.000015 | 0.000004 | 0.00019 | 0.016655 | 0.00001 | 0.000003 | 0.11 | 0.17 | READONLY |
| zesty | philbot-replay-r7-native | 0.001937 | 0.111712 | 0.000123 | 0.000309 | 0.004137 | 0.251507 | 0.000063 | 0.000232 | 1.16 | 2.60 | REPLAY |
| zesty | faithful-passion | 0.000006 | 0.058557 | 1.00e-9 | 3.00e-9 | 0.000004 | 0.027031 | 1.00e-9 | 3.00e-9 | 0.59 | 0.27 | RÔLE À QUALIFIER |
| zesty | philbot-vortex | 0.000005 | 0.02132 | 0 | 0 | 0.000001 | 0.051489 | 0 | 0 | 0.21 | 0.51 | SLEEPING |
| zesty | philbot-r1-oos-proxy | 0.000002 | 0.018567 | 0 | 0 | 0 | 0.002654 | 0 | 0 | 0.19 | 0.03 | SLEEPING |
| zesty | philbot-replay-r16-smoke | 0.000005 | 0.05123 | 5.50e-8 | 7.00e-9 | 0.000001 | 0.007323 | 8.00e-9 | 1.00e-9 | 0.51 | 0.07 | SLEEPING |
| zesty | philbot-control-shadow-read-proxy | 0.000099 | 0.019731 | 0.000001 | 0.000001 | 0.000091 | 0.036172 | 0.000006 | 0.000005 | 0.20 | 0.36 | SLEEPING |
| zesty | philbot-range-rejection-forward-lab | 0.000001 | 0.000749 | 0 | 0 | 0 | 0.000107 | 0 | 0 | 0.01 | 0.00 | SLEEPING |
| dp60 | rafale2-blofin-dp60 | 0.012675 | 0.163439 | 0.000546 | 0.000192 | 0.011152 | 0.156907 | 0.000427 | 0.000114 | 1.89 | 1.79 | LIVE/volume |
| dp60 | philbot-dp60-readonly | 0.000158 | 0.030087 | 0.000001 | 8.27e-7 | 0.000096 | 0.028523 | 7.69e-7 | 5.71e-7 | 0.30 | 0.29 | READONLY |
| recent40 | recent40-observer | 0.004241 | 0.082799 | 0.000363 | 0.000091 | 0.006512 | 0.196822 | 0.000364 | 0.000104 | 0.91 | 2.10 | OBSERVATEUR/volume |
| r20 | philbot-r20-hl | 0.030039 | 0.098964 | 0.000067 | 0.000009 | 0.004294 | 0.014146 | 0.00001 | 0.000001 | 1.59 | 0.23 | R20/volume |
| r20 | r20-shadow | 0.015757 | 0.162335 | 0.000286 | 0.000075 | 0.015687 | 0.223483 | 0.000284 | 0.000083 | 1.94 | 2.55 | SHADOW |


## ARBITRAGES CONCRETS

1. **HWR** est le principal coût continu. CPU/RAM 24h `0,3024 vCPU / 2,7126 Go` => **33,17 USD/mois** équivalent ; 7j `0,4217 / 3,2238` => **40,67 USD/mois** ; **1h** `0,1114 / 2,8402` => **30,63 USD/mois** *si charge permanente*. **Base avant correctif du 28 oct 16:46 Québec** `0,758 vCPU / 3,507 Go` => **50,23 USD/mois** équivalent. La 24h mixte avant/après et l'arrêt de budget **ne prouvent pas une économie post-déploiement** ; faire lecture de la fenêtre strictement POST à partir du 29 oct 16:46 Québec. Logs 12:41–12:51Z : `HYBRID_R4_COLLECTOR` par minute, `PREPARED_RUNTIME NO_FRESH_BOUNDARY` et `MARKET_STREAM_SILENT` EPICUSDT avec multiples reconnects ; `CURRENT_HISTORY_GAP` / refus SAND éphémère. Hypothèses profiler : cache/mémoire des 113 séries, reconnexions WS, cadence du recalcul, lecture d'historiques, taille des logs. **Ces hypothèses ne sont pas des causes certifiées ni des correctifs déployés.** Ticket [#67](https://github.com/chapsrl1999-lab/philbot-signer/issues/67), dépendances de sécurité [#62](https://github.com/chapsrl1999-lab/philbot-signer/issues/62).
2. **Jobs `philbot-reversal-research` et `philbot-grid-range-v1`** : Railway **61/61 échantillons CPU=RAM=0 dans la dernière heure**, malgré une RAM moyenne de **1,519 et 0,475 Go sur 24h**. Logs d'exécution le 28 oct 13:15–13:19Z. Ce sont des coûts d'exécutions **passées**, non permanents : **aucune « économie mensuelle » à annoncer en les coupant maintenant**. Le dernier `current` des fenêtres 24h peut être la dernière valeur non nulle périmée ; le 1h plus récent a préséance pour identifier l'inactivité.
3. **SHADOW Phoenix-v1 et dual** sans volume persistant : Vault HTTP404 (restore + backups répétés toutes 5–20 secondes dans les logs 28 oct 13:21–13:27Z), RAM moyenne ~**0,0583 + 0,0557 Go** sur 24h ; vérifier backoff et intégrité du registre avant changement. Ne pas financer indéfiniment un doublon sans avantage validé, **mais ne pas supprimer un ledger sans sauvegarde ni preuve de dépendance**. Ticket [#65](https://github.com/chapsrl1999-lab/philbot-signer/issues/65). `NETWORK_TX_GB` Phoenix-v1 7j `0,004448` vs 24h `0,0000956` par point : anomalie historique diminuée, causation non démontrée.
4. **Autres dépenses à qualifier, pas à désactiver aveuglément** : `hybrid-hwr-qualify-node22-20261010` ~**1,06 USD/mois** équivalent sur 24h (vérifier lecteurs, dépendances, suppression réversible); `philbot-replay-r7-native` ~**1,16 USD/mois** équivalent. Aucun service supplémentaire créé. Health et Guardian conservent volumes et CPU nécessaires ; ne pas dégrader leur couverture.
5. Hausse relative 24h vs 7j observée sur les **nouveaux jobs/volumes de charge** (R20-HL dans projet r20 et TRAINS) ; **absence de baseline historique à charge égale**, donc pas d'alerte de fuite >25% certaine. HWR a au contraire des moyennes 24h plus faibles que 7j. Pas de pic sortant majeur actuel justifiant un arrêt.
6. **État Railway** : projets zesty 30 services `SUCCESS` ou `SLEEPING` (5 sleeping : vortex, OOS proxy, replay R16 smoke, control shadow proxy, range rejection lab) ; `philbot-personal-snapshots` est un cron réussi ; zesty 4 échecs de builds sur 24h concernant Health, OUTSIDER, TRAINS, HWR avec service actuellement ONLINE, DP60 1 build FAILED plus récent SUCCESS, R20 3 builds FAILED plus récent SUCCESS, Recent40 ONLINE. **DP60 affiche un vieux patch staged** non touché. Aucune réplique LIVE supprimée ni limite modifiée.

## BUDGET ET VRAIES FACTURES (DEVISes non agrégées)

- **Facture acquittée Railway** : reçu Stripe `#2835-4324` (03 octobre 2026), **28,40 $** sur consommation **03 sept–03 oct** + abonnement Hobby du cycle suivant compensé par un crédit inclus de 5 $ sur le total ; ne pas rajouter 5 $ à 28,40 $. Le reçu indique CPU 0,82 $, mémoire 16,68 $, réseau 0,76 $, disque 0,13 $, agent 10,01 $ et Hobby 5 $ moins crédit 5 $ ; ce n'est **pas** la facture actuelle d'octobre.
- **Usage déclaré Railway 26 octobre 23:12 UTC** : **50,03 USD** ; **28 octobre 12:26 UTC** : **55,08 USD**, dépassement du **plafond de 55 USD en vigueur à cet instant**, notification de **suspension globale**. L'alerte du 23 oct indiquait **fin du cycle le 04 novembre 2026**. Services Railway revenus en ligne ensuite, mais **nouvelle limite effective et usage courant non disponibles via connecteur Railway ni e-mails plus récents à ce contrôle** : interdiction de calculer un compte à rebours de 24–48h inventé, de relever la limite, ou de garantir protection du LIVE contre prochain arrêt.
- **Reçu acquitté Anthropic Claude Pro** : 19 octobre, **CA$32,19 taxes incluses** pour 19 oct–19 nov (base CA$28 + TPS CA$1,40 + TVQ CA$2,79). **Ne pas additionner à des USD** sans taux/date de change, et ne pas assimiler à la facture complète du projet.
- Pas de factures courantes vérifiées ChatGPT, n8n, TradingView ; **pas de total fournisseur inventé**. Pas de PnL net réalisé + flottant consolidé sur les comptes réels, ni transferts neutralisés / frais contrôlés => **rentabilité consolidée 30j = NON CALCULABLE**. Ne pas déclarer le projet bénéficiaire.

## SUIVI D'EXÉCUTION

- **DÉTECTÉ** : HWR domine la dépense permanente et montre des reconnexions et un cache de marché massif à diagnostiquer; Vault Phoenix 404 récurrents; services de recherche finis; budget actuel inconnu.
- **PROPOSÉ** : instrumentation temporaire sur clone isolé, profil mémoire/cache CPU, déduplication des relectures, recul exponentiel Vault en état sûr, comparaison 24h *strictement post-correctif* et bilan des dépendances avant fermeture de service.
- **TESTÉ PAR CETTE EXÉCUTION** : seulement lecture métriques, logs et sources. **AUCUN patch technique testé**.
- **INSTALLÉ PAR CETTE EXÉCUTION** : ticket [#67](https://github.com/chapsrl1999-lab/philbot-signer/issues/67) et ce document de preuves versionné ; aucun déploiement, aucune coupure, aucun changement d'ordres.
- **OBSERVÉ 24H APRÈS** : non atteint ; revue distincte après 29 oct 16:46 Québec, à preuve homogène.

### Références de preuves
Railway via connecteur (projets et serviceIds conservés dans la table/inventaire, pas de dashboard facturation accessible), [prix officiels](https://docs.railway.com/pricing/plans), [incident budget #60](https://github.com/chapsrl1999-lab/philbot-signer/issues/60), [ticket FinOps #67](https://github.com/chapsrl1999-lab/philbot-signer/issues/67), Gmail message IDs `1a18279cdac87c27` (Railway 28 oct), `1a16989c06f0de33` (Railway reset), `1a17a7cf839c928d` (usage 26), `1a1049f13222ea5e` (reçu Railway 03 oct), `1a15439482a96ad7` (reçu Claude 19 oct). Aucune nouvelle source d'écritures LIVE utilisée.
