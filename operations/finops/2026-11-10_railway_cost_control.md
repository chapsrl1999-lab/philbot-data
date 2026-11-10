# FinOps PhilBot — 10 novembre 2026

**Lecture seule du périmètre Railway, aucun correctif technique installé.** Horodatage des requêtes: environ 2026-11-10 08:40–08:52 EST (13:40–13:52 UTC); quatre projets production (19 zesty-learning, 4 philbot-rafale2-dp60, 1 philbot-recent40-observer, 1 philbot-r20-shadow). Mesures get_service_metrics sur **1h / 24h / 168h**, quatre mesures CPU_USAGE, MEMORY_USAGE_GB, NETWORK_RX_GB, NETWORK_TX_GB; inventories describe_environment, environment_status et describe_service ciblés, journaux ciblés.

## Résumé vérifié / méthode

- Tarifs Railway officiels (relus 10/11/2026) : CPU **20 USD/vCPU-mois**, RAM **10 USD/Go-mois**, egress **0,05 USD/Go**, volume **0,15 USD/Go-mois** : https://docs.railway.com/pricing/plans . Ressources facturées au temps réel; forfait Hobby peut inclure 5 USD d'usage et ne doit pas être additionné deux fois.
- **Projection CPU+RAM à charge identique aux moyennes 24h : 66.21 USD/mois**; comparaison descriptive sur 168h **62.86 USD/mois**, non prévision de facture ni attribution d'économies. Ancienne projection le 09/11 : **64,49 USD/mois** selon rapport antérieur, écart descriptif **1.72 USD/mois**; le périmètre est passé de 24 à 25 services et les fenêtres/cycles de cron ne sont pas homogènes. Somme 1h **86.78 USD/mois SI cette seule heure se répétait continuellement** : ne pas extrapoler l'activité ponctuelle QUATRE à plein temps.
- Moyennes de *samples* réseau cumulées sur services (24h) : RX **0.00359 Go/échantillon**, TX **0.00092 Go/échantillon**; pas une mesure native d'egress facturé, ne pas convertir ces moyennes directement en facture. Les métriques 24h et 7j par service figurent dans la table et peuvent être confrontées aux factures réelles.
- **Facture payée confirmée par reçu Gmail Railway #2308-0620 : 71,91 USD le 03/11**, période d'usage 03/10–03/11: RAM 54,66, réseau 9,21, CPU 6,84, disque 0,38, agent usage 0,82, forfait Hobby 5 USD compensé par 5 USD inclus (pas de double comptage). **Usage courant distinct** : alerte Gmail du **07/11 à 21:16 UTC, 10,04 USD cumulés**, dernier avis repéré lors de la recherche au 10/11; **plafond actuel non trouvé, reset courant à confirmer dans dashboard** (historique indique cycle vers 03–04/12). Impossible d'affirmer risque d'arrêt à 24–48h ou absence définitive de risque.
- Claude Max: reçu **142,75 CAD payé 01/11**, crédit Pro 15,84 CAD inclus; Claude Pro **32,19 CAD payé 19/10**. Montants CAD/transactions distinctes, ne pas extrapoler facture future. Aucune facture complète disponible ici pour ChatGPT, n8n, TradingView; **PnL nets réalisés+flottants réconciliés sur 30 jours indisponibles** => bénéfice net global non établi.

## Services : CPU vCPU / RAM Go / réseau RX & TX Go moyens par point

Valeurs arrondies; 24h et 168h couvrent jusqu'au contrôle; 61 points 1h, ~1440 points 24h, ~10080 points 7j. *Coût* = CPU×20 + RAM×10, USD/mois constant illustratif. Les services dormant ou déclenchés en cron ne doivent pas recevoir cette projection comme une facture.

| Projet | Service | CPU24 | RAM24 | RX24 | TX24 | CPU7j | RAM7j | RX7j | TX7j | $24h constant | $7j constant | CPU1h / RAM1h |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| zesty | outsider-ledger | 0.000135 | 0.0089 | 0.000000 | 0.000000 | 0.000107 | 0.0102 | 0.000000 | 0.000000 | 0.09 | 0.10 | 0.00014 / 0.0089 |
| zesty | replay-r7 | 0.001860 | 0.2232 | 0.000085 | 0.000060 | 0.003837 | 0.2300 | 0.000180 | 0.000539 | 2.27 | 2.38 | 0.00194 / 0.2149 |
| zesty | personal-readonly | 0.000173 | 0.0111 | 0.000002 | 0.000001 | 0.000182 | 0.0122 | 0.000002 | 0.000001 | 0.11 | 0.13 | 0.00016 / 0.0111 |
| zesty | hybrid-market | 0.000266 | 0.0629 | 0.000032 | 0.000007 | 0.000159 | 0.0368 | 0.000019 | 0.000004 | 0.63 | 0.37 | 0.00030 / 0.0627 |
| zesty | personal-snapshots | 0.000000 | 0.0000 | 0.000000 | 0.000000 | 0.000002 | 0.0209 | 0.000000 | 0.000000 | 0.00 | 0.21 | 0.00000 / 0.0000 |
| zesty | range-wave-readonly | 0.000136 | 0.0115 | 0.000000 | 0.000000 | 0.000144 | 0.0117 | 0.000000 | 0.000000 | 0.12 | 0.12 | 0.00013 / 0.0114 |
| zesty | shadow-proxy | 0.000013 | 0.0094 | 0.000000 | 0.000000 | 0.000063 | 0.0295 | 0.000003 | 0.000001 | 0.09 | 0.30 | 0.00000 / 0.0000 |
| zesty | health | 0.002492 | 0.0867 | 0.000220 | 0.000039 | 0.002771 | 0.0921 | 0.000253 | 0.000042 | 0.92 | 0.98 | 0.00251 / 0.0933 |
| zesty | cascade-readonly | 0.000226 | 0.0118 | 0.000001 | 0.000001 | 0.000050 | 0.0026 | 0.000000 | 0.000000 | 0.12 | 0.03 | 0.00017 / 0.0121 |
| zesty | signer | 0.107779 | 0.2987 | 0.000018 | 0.000006 | 0.080645 | 0.2447 | 0.000022 | 0.000012 | 5.14 | 4.06 | 0.10392 / 0.3025 |
| zesty | bande-cycle | 0.000074 | 0.1790 | 0.000002 | 0.000002 | 0.000153 | 0.1728 | 0.000006 | 0.000006 | 1.79 | 1.73 | 0.00010 / 0.2001 |
| zesty | guardian | 0.002268 | 0.0860 | 0.000031 | 0.000016 | 0.002490 | 0.0820 | 0.000033 | 0.000014 | 0.91 | 0.87 | 0.00227 / 0.0769 |
| zesty | outsider | 0.011410 | 0.3152 | 0.000303 | 0.000120 | 0.011643 | 0.3110 | 0.000284 | 0.000119 | 3.38 | 3.34 | 0.01170 / 0.3202 |
| zesty | soldes-relay | 0.000059 | 0.0441 | 0.000005 | 0.000004 | 0.000032 | 0.0180 | 0.000002 | 0.000002 | 0.44 | 0.18 | 0.00004 / 0.0464 |
| zesty | quatre-ombre | 0.004895 | 0.1426 | 0.000973 | 0.000019 | 0.000700 | 0.0204 | 0.000139 | 0.000003 | 1.52 | 0.22 | 0.01025 / 2.2138 |
| zesty | cascade-REAL | 0.006435 | 0.2322 | 0.000028 | 0.000013 | 0.004974 | 0.1306 | 0.000205 | 0.000008 | 2.45 | 1.41 | 0.00640 / 0.2256 |
| zesty | rafale3 | 0.002366 | 0.1310 | 0.000058 | 0.000036 | 0.001806 | 0.1297 | 0.000198 | 0.000025 | 1.36 | 1.33 | 0.00246 / 0.1219 |
| zesty | HWR | 0.123463 | 2.9866 | 0.001062 | 0.000251 | 0.135532 | 2.9605 | 0.001139 | 0.000264 | 32.34 | 32.32 | 0.11446 / 2.9884 |
| zesty | swing1h | 0.000457 | 0.1032 | 0.000024 | 0.000053 | 0.000648 | 0.1053 | 0.000298 | 0.000050 | 1.04 | 1.07 | 0.00041 / 0.1017 |
| dp60 | triple-relay | 0.000161 | 0.0909 | 0.000026 | 0.000063 | 0.000184 | 0.1058 | 0.000039 | 0.000097 | 0.91 | 1.06 | 0.00017 / 0.0991 |
| dp60 | suivi | 0.004361 | 0.0765 | 0.000024 | 0.000013 | 0.004077 | 0.0706 | 0.000018 | 0.000016 | 0.85 | 0.79 | 0.00008 / 0.0644 |
| dp60 | triple-blofin | 0.000762 | 0.1884 | 0.000075 | 0.000009 | 0.000806 | 0.1914 | 0.000109 | 0.000010 | 1.90 | 1.93 | 0.00065 / 0.2091 |
| dp60 | dp60-readonly | 0.000369 | 0.0100 | 0.000007 | 0.000018 | 0.000330 | 0.0125 | 0.000007 | 0.000018 | 0.11 | 0.13 | 0.00033 / 0.0097 |
| recent40 | recent40-observer | 0.008467 | 0.3227 | 0.000438 | 0.000109 | 0.008798 | 0.3329 | 0.000422 | 0.000108 | 3.40 | 3.50 | 0.00858 / 0.3566 |
| r20 | r20-LIVE | 0.074796 | 0.2818 | 0.000174 | 0.000079 | 0.073574 | 0.2847 | 0.000199 | 0.000084 | 4.31 | 4.32 | 0.07283 / 0.2473 |

## Diagnostic hiérarchisé, causes vs hypothèses

1. **HWR LIVE principal** : 24h **0,123463 vCPU, 2,986598 Go**, soit **32.34 USD/mois** théoriques; 7j 0,135532 vCPU/2,960510 Go; 1h 0,114462/2,988351. Référence *avant 28/10*: 0,758 vCPU et 3,507 Go, soit **50,23 USD/mois théoriques**. Le 24h actuel est post-déploiement et plus faible, **mais AUCUNE économie payée causalement attribuée**, pas de profilage mémoire. Journal à 13:31–13:41Z : `HYBRID_R4_COLLECTOR` chaque minute et `PREPARED_RUNTIME NO_FRESH_BOUNDARY` entre clôtures de bougie, avec readiness READY et ordersPossible=true ; cette répétition peut être normale. Proposition non installée : audit du cache des 113 séries, logs et fréquence de collecte avec instrumentation ponctuelle sans modifier moteur/gestion des stops; benchmark sur clone puis observation >=24h à charge comparable, rollback testé.
2. **SIGNER** : 24h **5.14 USD/mois** vs 7j **4.06**, hausse relative **26.7 %** (CPU 0,107779 vs 0,080645, RAM 0,298680 vs 0,244694); volume /data et service OBSERVE CONTINUATION, donc aucune coupure. Journaux récents de batch 202 et un rejet BATCH_ALREADY_CLOSED (pas preuve de boucle CPU). **DÉTECTÉ**, cause non démontrée : profiler polling/quorum et recomputations, examiner répartition par endpoints avant de corriger; aucun changement du moteur ni de l'ingress sans tests.
3. **R20 LIVE** : **4.31 USD/mois** en 24h; incidents SOURCE_UNAVAILABLE dans la garde horaire connus, pas de fuite financière supplémentaire démontrée. **RECENT40 LIVE 3.40**, **OUTSIDER LIVE 3.38**, **CASCADE REAL Bitunix 2.45**; leur nécessité métier interdit toute désactivation de réduction de coûts. CASCADE a 15 gaps historiques et scans 5min, mais aucune source prouvant un surcoût >10 USD/mois; nom Railway « shadow » ne reflète PAS le mode réel.
4. **QUATRE MOTEURS SHADOW**, projet zesty : service cron quotidien **11:05 UTC**, statut cronReady après SUCCESS, déploiement renouvelé le 10/11 à 12:43Z. 1h moyenne **0,010248 vCPU / 2,213847 Go** car l'échantillon comprend le batch; 24h **0,004895 / 0,142644** (équivalent mixte **1.52 USD/mois**) vs 7j à **0.22**. **Ne pas extrapoler 2,21 Go 24/7 ni supprimer un job utile**. Aucun volume local; suivi sur volume distinct. Dernier cycle de la nouvelle instance non certifié après redeploy, responsabilité fiabilité hors FinOps.
5. **Replay R7/R9** à **2.27 USD/mois** : logs du 10/11 à 13:30Z multiples `PUBLIC_HTTP_429` dans une seconde sur API publique ; HTTP vers la page du service 200 n'invalide pas la limitation upstream. Cause probable du bruit et de requêtes inutiles : retries sans backoff / cache absent (à confirmer dans code). PROPOSÉ uniquement : déduplication/backoff exponentiel + cache avec TTL et nombre maximum de tentatives sur clone isolé, test sans dépendance métier, rollback, zéro retouche LIVE.
6. **HWR market-data** **0.63 USD/mois** 24h (projet HWR, service séparé) : +~70% vs 7j *partiellement lancé le 06/11*; jamais arrêter sans prouver l'absence de dépendance du HWR. **PERSONAL snapshots CRASHED**, cron planifié annuel dans la config (`0 0 1 1 *`), et **proxy SHADOW SLEEPING** : **CPU et RAM égaux à 0 sur la dernière heure**, pas de compute à économiser aujourd'hui. Incident fonctionnel PERSONAL à traiter dans suivi SRE, sans supposer profit potentiel de leur suppression. Les volumes détachés existent et peuvent être facturés indépendamment : aucun volume supprimé ni déclaré redondant sans identification de propriétaire et sauvegarde restaurable.

## Seuils, décisions et suivi d'installation

- Postes >10 USD/mois au sens CPU+RAM constant: **HWR seul**. Hausse relative >25% sur charges mixtes/naissantes : SIGNER (+26.7 %), QUATRE, HWR-market, CASCADE, soldes-relay, cascade-readonly (bases faibles/partielles). Distinction hausse observée de consommation versus fuite de coûts permanente; aucune facturation nouvelle associée certifiée. Pas d'augmentation d'egress facturé quantifiable depuis les moyennes.
- **DÉTECTÉ**: HWR premier poste, SIGNER hausse 24h/7j, bruit PUBLIC_HTTP_429 et services récents à justifier. **PROPOSÉ**: analyse de profiling/polling/cache et tests sur clone isolé. **TESTÉ**: relevés read-only 1h/24h/7j, inventaires et journaux; **aucun test de correctif sur clone aujourd'hui**. **INSTALLÉ**: aucune modification technique. **OBSERVÉ 24h après installation**: non applicable. Aucune économie attestée. Aucun bot LIVE/Health/Guardian, volume, stop, ordre, capital, stratégie, risque, plafond ou alerte modifié.

Sources: Railway get_service_metrics, describe_environment / environment_status / describe_service / get_logs dans les quatre projets, Gmail avis Railway 07/11 et reçu 03/11, reçu Anthropic 01/11, état officiel https://github.com/chapsrl1999-lab/philbot-data/blob/main/operations/PHILBOT_OPERATING_STATE_V1.md ; suivi https://github.com/chapsrl1999-lab/philbot-signer/issues/67 .
