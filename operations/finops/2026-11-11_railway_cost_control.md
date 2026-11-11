# PhilBot — contrôle FinOps, 11 novembre 2026

**Statut : DÉTECTÉ + PROPOSÉ. Aucun correctif technique TESTÉ ni INSTALLÉ.** Mesures Railway réalisées le 11/11 matin heure de Montréal (~13h25–13h45 UTC), quatre environnements production : **19 zesty-learning, 4 philbot-rafale2-dp60, 1 philbot-recent40-observer, 1 philbot-r20-shadow = 25 services**. Sources : `get_service_metrics` pour **1h, 24h, 168h**, `describe_environment`, `environment_status`, `describe_service` (QUATRE/HWR/replay/snapshots), `get_logs` et journaux de flux. Les statuts déploiements ne prouvent pas l'exécution correcte des ordres ni des stops.

## Chiffres vérifiés et méthodologie

- **Projection indicative CPU + RAM sur moyenne des échantillons 24h : 77.77 USD/mois à charge identique**, contre **66,21 USD/mois** dans le relevé du 10/11 (différence **+11.56 USD/mois**, **+17.5%**). Fenêtre **7 jours : 65.62 USD/mois à charge identique**, non facture. L'augmentation globale provient surtout du nouveau cron horaire QUATRE, et les deux fenêtres ne correspondent pas à des périodes opérationnelles identiques.
- Tarif officiel Railway : **20 USD/vCPU-mois, 10 USD/Go RAM-mois, egress 0,05 USD/Go, volumes 0,15 USD/Go-mois**, ressources facturées *prorata du temps* et non à une ligne fixe par service : https://docs.railway.com/pricing/plans . Ces coûts-proxy sont **sans frais réseau facturés, volumes, agent, forfait ou remises** et ne prédisent pas une facture exacte.
- Les valeurs **NETWORK_RX_GB/NETWORK_TX_GB sont des moyennes d'échantillons de métrique, PAS le trafic facturé du cycle** : ne pas multiplier aveuglément par 24h/7j et facturer l'egress. Le journal réseau-flux a été échantillonné sur QUATRE et replay mais est limité aux dernières entrées, non exhaustif.
- **Dernière facture payée effectivement prouvée** : reçu Gmail Railway **71,91 USD le 03/11**, usage 03/10–03/11, mémoire 54,66, réseau 9,21, CPU 6,84, disque 0,38, Agent 0,82; Hobby 5,00 compensé par crédit de 5,00, sans double addition. **Consommation du cycle courant distincte** : dernier avis Gmail **10,04 USD au 07/11 21h16 UTC**; aucune nouvelle alerte *billing* depuis cette date dans la recherche du 11/11. Reçu d'abonnement plan daté **03/11–03/12**; prochaine échéance au voisinage du 03–04/12, **reset du compteur et plafond de coupure courants non accessibles**. Impossible de chiffrer honnêtement un arrêt sous 24–48 h; ancien arrêt 55,08/55 le 28/10 historique, ne pas réutiliser le plafond. Aucune modification de limite.
- Autre preuve partielle : reçu Anthropic **Claude Max 142,75 CAD payé 01/11**, dont crédit Pro 15,84 CAD; référence Claude Pro **32,19 CAD payé 19/10**. Ni facture complète ChatGPT/n8n/TradingView ni PnL réalisés+flottants réconciliés 30j sur comptes réels, neutralisés des transferts, accessibles dans ce contrôle. **Aucun total net global ni conversion CAD↔USD inventé.**

## Les 25 services — CPU vCPU / mémoire Go / réseau Go moyens par échantillon

**Ordre des mesures 24h et 7j conforme aux réponses Railway.** En dernière colonne, coût de charge constante seulement; pour un cron, la RAM échantillonnée moyenne mêle activité et sommeil.

| Projet | Service | CPU 24h | RAM 24h | RX/TX 24h | CPU 7j | RAM 7j | RX/TX 7j | CPU/RAM 1h | $/mois 24h constant | $/mois 7j constant |
|---|---|---:|---:|---|---:|---:|---|---|---:|---:|
| zesty | QUATRE SHADOW | 0.011085 | 1.1206 | 0.001636 / 0.000050 | 0.002284 | 0.1921 | 0.000373 / 0.000010 | 0.020445 / 0.5458 | 11.43 | 1.97 |
| zesty | CASCADE lecture seule | 0.000199 | 0.0080 | 0.000002 / 0.000001 | 0.000078 | 0.0037 | 0.000000 / 0.000000 | 0.000253 / 0.0060 | 0.08 | 0.04 |
| zesty | Soldes relay | 0.000050 | 0.0473 | 0.000005 / 0.000004 | 0.000039 | 0.0248 | 0.000003 / 0.000002 | 0.000031 / 0.0477 | 0.47 | 0.25 |
| zesty | HWR market-data | 0.000263 | 0.0627 | 0.000033 / 0.000007 | 0.000196 | 0.0457 | 0.000024 / 0.000005 | 0.000261 / 0.0627 | 0.63 | 0.46 |
| zesty | CASCADE REAL | 0.005765 | 0.2484 | 0.000306 / 0.000017 | 0.005791 | 0.1659 | 0.000249 / 0.000011 | 0.005711 / 0.2599 | 2.60 | 1.77 |
| zesty | Outsider ledger | 0.000128 | 0.0089 | 0.000000 / 0.000000 | 0.000125 | 0.0114 | 0.000000 / 0.000000 | 0.000163 / 0.0089 | 0.09 | 0.12 |
| zesty | Range-wave read-only | 0.000147 | 0.0112 | 0.000000 / 0.000000 | 0.000143 | 0.0116 | 0.000000 / 0.000000 | 0.000143 / 0.0111 | 0.11 | 0.12 |
| zesty | PERSONAL snapshots cronFailed | 0.000000 | 0.0000 | 0.000000 / 0.000000 | 0.000001 | 0.0101 | 0.000000 / 0.000000 | 0.000000 / 0.0000 | 0.00 | 0.10 |
| zesty | PERSONAL read-only | 0.000171 | 0.0112 | 0.000002 / 0.000001 | 0.000180 | 0.0111 | 0.000002 / 0.000001 | 0.000254 / 0.0118 | 0.12 | 0.11 |
| zesty | OUTSIDER | 0.012531 | 0.3206 | 0.000355 / 0.000122 | 0.011772 | 0.3107 | 0.000285 / 0.000119 | 0.012159 / 0.3220 | 3.46 | 3.34 |
| zesty | HWR | 0.127207 | 2.9910 | 0.001179 / 0.000271 | 0.135939 | 2.9712 | 0.001130 / 0.000262 | 0.130814 / 2.9892 | 32.45 | 32.43 |
| zesty | Proxy SHADOW sleeping | 0.000010 | 0.0276 | 0.000000 / 0.000000 | 0.000032 | 0.0312 | 0.000001 / 0.000000 | 0.000000 / 0.0000 | 0.28 | 0.31 |
| zesty | Replay R9 | 0.002745 | 0.2383 | 0.000182 / 0.000398 | 0.003868 | 0.2338 | 0.000185 / 0.000482 | 0.001837 / 0.2611 | 2.44 | 2.42 |
| zesty | SWING 1h | 0.000461 | 0.1044 | 0.000024 / 0.000055 | 0.000596 | 0.1050 | 0.000217 / 0.000051 | 0.000601 / 0.1007 | 1.05 | 1.06 |
| zesty | Guardian | 0.002077 | 0.0930 | 0.000030 / 0.000014 | 0.002393 | 0.0843 | 0.000032 / 0.000014 | 0.002179 / 0.0792 | 0.97 | 0.89 |
| zesty | Health | 0.002331 | 0.0886 | 0.000220 / 0.000039 | 0.002614 | 0.0921 | 0.000234 / 0.000040 | 0.002318 / 0.0831 | 0.93 | 0.97 |
| zesty | RAFALE3 | 0.000962 | 0.1333 | 0.000079 / 0.000016 | 0.001801 | 0.1298 | 0.000138 / 0.000026 | 0.000644 / 0.1525 | 1.35 | 1.33 |
| zesty | BANDE & CYCLE | 0.000280 | 0.1881 | 0.000013 / 0.000012 | 0.000113 | 0.1782 | 0.000004 / 0.000003 | 0.000701 / 0.2000 | 1.89 | 1.78 |
| zesty | SIGNER | 0.105327 | 0.3086 | 0.000019 / 0.000006 | 0.085035 | 0.2599 | 0.000019 / 0.000008 | 0.104212 / 0.3482 | 5.19 | 4.30 |
| dp60 | Suivi | 0.003785 | 0.0942 | 0.000030 / 0.000014 | 0.004151 | 0.0764 | 0.000022 / 0.000018 | 0.000136 / 0.0902 | 1.02 | 0.85 |
| dp60 | Triple relay | 0.000161 | 0.0974 | 0.000028 / 0.000068 | 0.000182 | 0.1067 | 0.000038 / 0.000096 | 0.000195 / 0.1142 | 0.98 | 1.07 |
| dp60 | TRIPLE BLOFIN | 0.000764 | 0.1904 | 0.000080 / 0.000009 | 0.000808 | 0.1902 | 0.000109 / 0.000010 | 0.000813 / 0.1822 | 1.92 | 1.92 |
| dp60 | DP60 lecture seule | 0.000380 | 0.0100 | 0.000007 / 0.000019 | 0.000351 | 0.0109 | 0.000007 / 0.000018 | 0.000483 / 0.0100 | 0.11 | 0.12 |
| recent40 | RECENT40 | 0.008656 | 0.3623 | 0.000444 / 0.000110 | 0.008722 | 0.3363 | 0.000426 / 0.000108 | 0.007515 / 0.3604 | 3.80 | 3.54 |
| r20 | R20 LIVE | 0.071531 | 0.2967 | 0.000147 / 0.000070 | 0.073079 | 0.2879 | 0.000179 / 0.000078 | 0.071425 / 0.3260 | 4.40 | 4.34 |

**Sommes calculées depuis valeurs arrondies du tableau** : CPU/RAM 24h ≈77.77 USD/mois, 7j ≈65.62 USD/mois. Pour la précision, les appels originaux non arrondis montrent 24h **77,77** et 7j **65,62**.

## Diagnostic hiérarchisé et action réversible

### 1. QUATRE MOTEURS — changement concret de consommation d'un service de recherche
- QUATRE (`339f50bd-16b4-4aad-9ed6-eb4799b0462c`) est **SHADOW, fictif, aucun ordre**, mais transmet ses états à **PhilBot Suivi**. Le déploiement Railway du **10/11 à 14h23 UTC**, commit `980224584340762821c2c6167ba782c9ae94146e`, documente une **demande explicite de mise à jour plus fréquente** : ancien calcul quotidien → nouveau cron **`5 * * * *`** (horaire). **Ne pas revenir au quotidien ni supprimer** sans accord métier ; cela réduirait la fraîcheur demandée.
- **24h : 0,011085 vCPU, 1,12056 Go RAM = 11,43 USD/mois à charge constante**, contre **1,52 USD/mois** au 10/11 (+9,91 théoriques). **7j : 1,97 USD/mois** (fenêtre surtout avant changement), soit hausse 24h/7j **+481%**, base non homogène. Ce n'est **PAS** +9,91 USD déjà payés.
- **Cause démontrée** : les logs de **26 démarrages de conteneur du 10/11 12:05Z au 11/11 13:05Z**, cadence ~horaire depuis ~15Z, montrent **343 séries directes** téléchargées par passage, **281 cryptos × 4 669 heures** reconstruites depuis 01/05/2026 et 62 cryptos minute; calcul **60–104 s par passage** (une exécution 421 s après incident). Le code réel `quatre/job.py` du SHA `728c9c385bbe645337612fe25e5dd2678016487a` dit explicitement **recalcul au COMPLET chaque heure** depuis QUATRE_START, cache local `/tmp/quatre_cache`, alors que les conteneurs cron ne restent pas actifs entre passages et **aucun volume** n'est monté. Le cache temporaire n'est donc pas une persistance inter-cron. Cela explique une hausse structurelle de fréquence et des données refaites, **sans quantifier la part évitable**.
- Courriel Railway du **11/11 à 08:10Z** : exécution a échoué quand les bougies 1m couvraient **47/62** cryptos. **Rétabli** : déploiement actuel SUCCESS, cron **13:07Z succeeded**, état fictif transmis à PhilBot Suivi; ne pas annoncer panne actuelle.
- **PROPOSÉ (non testé/installé)** : préserver **exactement** une valeur d'état par heure et les contrôles d'intégrité, en benchmarkant le moteur réel sur un *clone isolé* avec snapshots incrémentaux ou réemploi d'archives journalières seulement si persistance déjà existante et sauvegardée; vérifier parité binaire des événements/PNL fictif, frais, panier et horodatages face au full-replay pour **au moins sept clôtures horaires**, reprise après manque 1m et crash, backoff Binance et rollback. Ne pas toucher à CASCADE REAL, à la config risque ni au récepteur Suivi. **Aucune économie garantie**; alternative cache de lot inter-exécution exige preuve stockage/absence de dépendances et consentement si altération du flux métier.

### 2. HWR et autres postes
- HWR `79ebd36d-3960-4535-adf8-16f9e1265b94` : **0,127207 vCPU / 2,990987 Go 24h = 32,45 USD/mois à charge constante**; 7j 0,135940 / 2,971180 = **32,43**. Référence *avant correctif 28/10* 0,758 vCPU / 3,507 Go = **50,23**. Référence historique et premières fenêtres **24h mixtes avant/après ne prouvent aucune baisse causale**; même cette fenêtre 100% ultérieure ne certifie pas une économie *facturée* ni l'innocuité métier. Logs `COLLECTOR`, `NO_FRESH_BOUNDARY` et `MARKET_STREAM_PARTIAL_SILENCE` EPIC : surveiller qualité des données, **ne pas retirer** un cycle de surveillance/trading pour économiser sans profiling et validation.
- SIGNER : **5,19 USD/mois constant 24h contre 4,30 sur 7j** (+20,8%, seuil >25% non franchi dans la projection globale), volume présent, service OBSERVE CONTINUATION selon état antérieur : ne pas arrêter.
- R20 LIVE **4,40**, RECENT40 LIVE **3,80**, OUTSIDER LIVE **3,46**, CASCADE **REAL** sous ancien nom `cascade-shadow` **2,60** ; aucun de ces services ou leurs protections n'a été désactivé. CASCADE est +46% 24h/7j mais lié au lancement récent et coût individuel modeste; pas de fuite prouvée. HWR market-data, soldes-relay, cascade-readonly ont des hausses relatives >25% sur faibles bases d'ancienneté, sans surcoût matériel prouvé.
- Replay R7/R9 **2,44 USD/mois constant**, logs 11/11 `PUBLIC_HTTP_429` répétés par groupes **13:00, 13:30 UTC**; côté service les requêtes HTTP retournent 200, ce qui n'invalide pas les refus **upstream**. Trafic TX moyen 24h 0,000398 Go/échantillon vs 0,000060 hier : hausse **non égale à l'egress facturé**. **PROPOSÉ** cache TTL / déduplication / backoff sur clone, validation routes et données réelles avant déploiement, rollback documenté, pas de baisse fictive annoncée.
- Deux services avec **CPU=0 ET RAM=0 sur toute la dernière heure** : PERSONAL snapshots `cronFailed` depuis 06/11, et proxy SHADOW SLEEPING. **Aucune économie CPU/RAM à revendiquer à leur arrêt**. PERSONAL snapshots logs du 06/11 `PERSONAL_SNAPSHOT_HTTP_401`, tâche cron configurée annuelle `0 0 1 1 *` alors que les journaux montrent auparavant des exécutions répétées 15min : conformité métier à auditer en maintenance, ne pas déclencher de suppression ou restauration implicite.
- 4 projets / 25 services (même périmètre que le 10/11), volumes persistants dont plusieurs détachés **préservés** ; aucun nouveau service ajouté par FinOps. Projet DP60 conserve un patch staged ancien sur `philbot-dp60-readonly` **non appliqué**.

## États à ne pas confondre
**DÉTECTÉ** : hausse matériellement significative des coûts théoriques QUATRE, cause récurrence horaire/full-recompute vérifiée, bruit 429 R9, HWR premier poste. **PROPOSÉ** : benchmark d'incrémentalité/parité et cache sur clone isolé, backoff replay, profiling HWR. **TESTÉ** : inventaires, métriques 1h/24h/7j, dépôts de source, journaux et factures partiels relus; **aucun correctif de code testé**. **INSTALLÉ** : aucune modification technique, seuls suivi documentaire et issue FinOps. **OBSERVÉ 24h après patch technique** : sans objet. Stratégies, ordres, SL, volume, seuils, capital, service LIVE, Health/Guardian, budget **inchangés**.

**Sources :** Railway API lecture seule; reçus Gmail Railway #2308-0620 et Anthropic #2205-7093-5830; https://docs.railway.com/pricing/plans ; suivi https://github.com/chapsrl1999-lab/philbot-signer/issues/67 ; état https://github.com/chapsrl1999-lab/philbot-data/blob/main/operations/PHILBOT_OPERATING_STATE_V1.md .
