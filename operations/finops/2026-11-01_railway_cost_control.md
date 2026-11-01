# PhilBot — contrôle FinOps Railway du 1 novembre 2026

**Relevé : 1 novembre ~13:39–13:46 UTC (08:39–08:46 Québec).** Source : outils Railway `list_projects`, `list_services`, `get_service_metrics` (CPU_USAGE, MEMORY_USAGE_GB, NETWORK_RX_GB, NETWORK_TX_GB; fenêtre 24h échantillonnée 120s/721 points, 168h 600s/1009 points), `describe_environment`, `environment_status`, sept `describe_service` ciblés, journaux de six services et Gmail. **38 services : zesty 31 + DP60 4 + RECENT40 1 + R20 2**, dont **34 derniers déploiements SUCCESS, 4 SLEEPING**; un build RANGE échoué 12:33Z puis remplacé par SUCCESS à12:40Z, pas incident runtime permanent. Aucune ressource LIVE coupée et aucune modification de configuration ou stratégie. Les 2 nouveaux services TRIPLE (créés/déployés récemment) rendent certaines moyennes 24h/7j non stationnaires.

## Synthèse des coûts — valeurs à ne pas confondre
- **Équivalent CPU+RAM à charge 24h constante : 68.55 USD/mois** ; équivalent fenêtre 7j : **77.69 USD/mois**. Cette extrapolation n'est **ni usage réellement facturé, ni facture**. Elle exclut egress, volumes, suppléments, crédits et abonnements. Comparaison publication du 31oct **67,01 USD/mois**; la charge a varié et l'inventaire augmenté de 36 à 38.
- Tarif officiel Railway au 1nov : **20 USD/vCPU-mois**, **10 USD/Go-mois RAM**, **0,05 USD/Go d'egress**, **0,15 USD/Go-mois de volume** ; facturation proratisée au temps ; coût de souscription Hobby 5 USD/mois appliqué à l'usage inclus, pas à additionner aveuglément. Source https://docs.railway.com/pricing/plans .
- **Dernière preuve d'usage du cycle Gmail** : mail support Railway 30oct **16:12 UTC**, **60,08 USD consommés / plafond 80,00 USD**, solde **19,92 USD à cette date**, reset annoncé **4nov**. Ancien arrêt 28oct **55,08/55 USD** est historique ; **usage et limite aujourd'hui non accessibles en temps réel, aucune alerte plus récente repérée**. Le taux constaté 28→30 oct ne justifie pas à lui seul une alerte d'arrêt garanti sous 24–48h. **Aucun plafond augmenté.** Sources Gmail IDs `1a18d953fea0ab31`, `1a18279cdac87c27` ; courriel 1nov `1a1971a9af7fee75` est un *build failed* finalement remplacé.
- Reçus (montants effectivement vérifiés séparément) : Railway **28,40 USD payé le 3oct pour cycle antérieur**, Claude Pro **32,19 CAD taxes comprises payé le 19oct**. Recherche Gmail depuis oct : TradingView annonce prélèvement prochain, mais pas facture payée vérifiée; autres abonnements n8n/ChatGPT et PnL nets consolidés des comptes réels non disponibles. **Aucun PnL net 30j après abonnements calculable**, ne jamais additionner CAD et USD sans conversion datée ni mélanger reçus de périodes différentes.

## Attribution et détection de hausses
**Principaux postes 24h CPU+RAM**, en USD/mois à charge constante, non économies réalisées : `hybrid-r4-read-check` 30.73 (7j 35.62); `philbot-signer` 4.04 (7j 4.32); `philbot-r20-hl` 4.03 (7j 1.99); `philbot-outsider-hl-validation` 3.69 (7j 3.53); `recent40-observer` 3.69 (7j 2.71); `philbot-snapback-v10r1` 2.31 (7j 2.22); `r20-shadow` 2.09 (7j 2.30); `philbot-replay-r7-native` 2.02 (7j 1.84); `rafale2-blofin-dp60` 1.91 (7j 1.83).
- **HWR** `hybrid-r4-read-check` (**serviceId 79ebd36d-3960-4535-adf8-16f9e1265b94**) : CPU 24h **0,113785 vCPU**, RAM **2,845703 Go** = **30.73 USD/mois** constants; 7j **0,273336/3,015002** = **35.62 USD/mois**. Référence AVANT correctif 28oct **0,758 vCPU/3,507 Go = 50,23 USD/mois**. Fenêtre 24h intégralement postérieure au correctif du 28oct et au dernier déploiement du 31oct 13:25Z ; **baisse descriptive**, ni causalité isolée ni économie payée prouvée. Journaux 12:28–13:45Z : 140 PREPARED_RUNTIME, 139 COLLECTOR, 107 MARKET_STREAM, 28 APPROVED_PROJECTION_ERROR; interruptions INCOMPLETE_SIGNALS/CURRENT_HISTORY_GAP puis READY, silence partiel de paires (EPIC, NEO, GRT, SNX...). **Ne pas ralentir le calcul LIVE ou les alertes pour économie sans validation et rollback.**
- **RECENT40** : RAM moyenne 24h **0,357320 Go** vs 7j **0,257548** : **+38,7 % relatif** ; CPU 24h **0,005581** vs 7j **0,006877** ; coûts équivalents CPU+RAM **3.68 vs 2.71 USD/mois**. Déploiement identique depuis 29oct, hausse mémoire **DÉTECTÉE, cause et croissance active non démontrées**; le 7j inclut période d'arrêt, comparer fenêtres homogènes et snapshots avant patch. Aucun seuil >10 USD/mois.
- **R20/HL** `philbot-r20-hl` : CPU 24h **0,068133** vs 7j **0,034739** (+96 %), RAM **0,267147 vs 0,129626** (+106 %) ; équivalent **4.03 vs 1.99 USD/mois**, hausse relative liée en partie à l'historique de démarrage/7j contenant inactivité; pas une fuite prouvée et pas >10 USD/mois. Consultation journaux R20 **REFUSÉE par l'API (viewer role)**, donc aucune cause confirmée par logs.
- **Nouvel inventaire** : `triple-relay` et `triple-blofin` dans projet DP60, dernières releases 1nov 00:41Z et 13:33Z, reliés au moteur SHADOW; **1.32 USD/mois** CPU+RAM sur moyenne 24h MIXTE (démarrage récent) donc projection *sous-estimant ou sur-estimant* le régime futur. Pas de dépendance inutile prouvée; ne pas arrêter.
- **Replays R7** `philbot-replay-r7-native` : dernier 201 logs 00:15–13:31Z = **151× PUBLIC_HTTP_429, 35× PUBLIC_HTTP_418, 15× PUBLIC_QUERY_NOT_ALLOWED**; échec HTTP répété, probablement throttling/refus upstream, mais cause/exposition exactes non certifiées. Coût compute 24h **2.02 USD/mois** théoriques et trafic TX moyen par point 0,001252 Go; **proposer** backoff/circuit breaker côté RECHERCHE sans affecter API ni résultats LIVE, après traçage dépendances et tests. Aucune dépense réseau facturée chiffrée depuis ces seules moyennes.
- **HWR qualify** `hybrid-hwr-qualify-node22-20261010` : tient en continu 0,085175 Go RAM sur 24h et 1h ; dernier log explicite 28oct qualification PASSED ; **0.86 USD/mois** théorique, mais **aucune preuve d'inutilité/d'absence de dépendance** ; audit de référence/consommateurs avant toute hypothèse d'arrêt. Ne pas le confondre avec job fini.
- **Recherche terminée** `philbot-reversal-research` et `philbot-grid-range-v1` : les 61 points 1h montrent **0 CPU et 0 RAM**, toutes mesures 24h à zéro (moyenne 7j non nulle = exécution passée). **0 coût CPU+RAM présent, aucune économie fictive à décompter**. `philbot-replay-r16-smoke`/autres SLEEPING similaires également 0 sur 24h. Deux SHADOW Phoenix sans volume continuent avec faible RAM, historiques backup HTTP_404 du 28oct, **pas de preuve d'un échec courant** ; ne jamais effacer une donnée/arrêter sans sauvegarde et contrôle source.
- **Réseau** : métriques RX/TX par échantillon reportées ci-dessous. Max TX moyen 24h parmi services actifs visibles : R7 0,001252 Go/point et PhoenixV1 0,000736 Go/point; pics 7j PhoenixV1 0,023949 Go/point. **Ce sont des moyennes de métriques, PAS les Go d'egress intégrés sur un cycle** ; n'en déduire ni facture egress, ni économie chiffrée. Qualifier la hausse historique avec journaux `network-flow` avant patch.

## Relevé exhaustif 38 services — moyennes des fenêtres
**¹** 20×CPU_moyen_24h + 10×RAM_moyenne_24h. SLEEPING est état du dernier déploiement, SUCCESS ne certifie pas LIVE métier. Les valeurs nulles de jobs ne sont pas imputées comme consommation future. Échantillonnage 721/1009 points par service pour toutes les mesures.

| Projet | Service | Statut déploiement | CPU 24h / 7j (vCPU) | RAM 24h / 7j (Go) | RX 24h / 7j (Go, moy./point) | TX 24h / 7j (Go, moy./point) | USD/mois CPU+RAM 24h¹ |
|---|---|---|---:|---:|---:|---:|---:|
| zesty | `philbot-audit-positions-telegram-20261029` | SUCCESS | 0.000000 / 0.000000 | 0.000000 / 0.000000 | 0.000000 / 0.000000 | 0.000000 / 0.000000 | 0.00 |
| zesty | `philbot-r20-hl` | SUCCESS | 0.000000 / 0.000000 | 0.000000 / 0.000000 | 0.000000 / 0.000000 | 0.000000 / 0.000000 | 0.00 |
| zesty | `philbot-trains-bitunix` | SUCCESS | 0.000021 / 0.000028 | 0.092905 / 0.072976 | 0.000001 / 0.000005 | 0.000006 / 0.000017 | 0.93 |
| zesty | `philbot-range-wave-readonly` | SUCCESS | 0.000366 / 0.000298 | 0.015100 / 0.017518 | 0.000037 / 0.000180 | 0.000010 / 0.000045 | 0.16 |
| zesty | `philbot-personal-snapshots` | SUCCESS | 0.000003 / 0.000004 | 0.002621 / 0.002044 | 0.000000 / 0.000000 | 0.000000 / 0.000000 | 0.03 |
| zesty | `philbot-personal-readonly` | SUCCESS | 0.000191 / 0.000198 | 0.011318 / 0.013004 | 0.000006 / 0.000034 | 0.000004 / 0.000020 | 0.12 |
| zesty | `philbot-outsider-hl-validation` | SUCCESS | 0.011116 / 0.011697 | 0.346414 / 0.329935 | 0.000602 / 0.003000 | 0.000232 / 0.001138 | 3.69 |
| zesty | `hybrid-hwr-qualify-node22-20261010` | SUCCESS | 0.000249 / 0.004636 | 0.085175 / 0.086788 | 0.000066 / 0.008089 | 0.000013 / 0.000957 | 0.86 |
| zesty | `philbot-replay-r16-smoke` | SLEEPING | 0.000000 / 0.000001 | 0.000000 / 0.023461 | 0.000000 / 0.000000 | 0.000000 / 0.000000 | 0.00 |
| zesty | `hybrid-r4-read-check` | SUCCESS | 0.113785 / 0.273336 | 2.845702 / 3.015001 | 0.001828 / 0.011583 | 0.000444 / 0.002785 | 30.73 |
| zesty | `philbot-grid-range-v1` | SUCCESS | 0.000000 / 0.000005 | 0.000000 / 0.278510 | 0.000000 / 0.000067 | 0.000000 / 0.000002 | 0.00 |
| zesty | `philbot-control-shadow-read-proxy` | SUCCESS | 0.000084 / 0.000120 | 0.019221 / 0.031063 | 0.000007 / 0.000061 | 0.000002 / 0.000039 | 0.19 |
| zesty | `philbot-bitunix-phoenix-shadow-v1` | SUCCESS | 0.003487 / 0.007316 | 0.059480 / 0.079878 | 0.001045 / 0.005724 | 0.000736 / 0.023949 | 0.66 |
| zesty | `philbot-bitunix-phoenix-dual-shadow` | SUCCESS | 0.003271 / 0.003659 | 0.067705 / 0.081634 | 0.001026 / 0.005085 | 0.000089 / 0.000443 | 0.74 |
| zesty | `philbot-r20-shadow-probe` | SUCCESS | 0.000144 / 0.000148 | 0.018069 / 0.018954 | 0.000051 / 0.000254 | 0.000008 / 0.000042 | 0.18 |
| zesty | `philbot-range-rejection-forward-lab` | SLEEPING | 0.000000 / 0.000000 | 0.000000 / 0.000440 | 0.000000 / 0.000000 | 0.000000 / 0.000000 | 0.00 |
| zesty | `philbot-r1-oos-proxy` | SLEEPING | 0.000000 / 0.000000 | 0.000000 / 0.010895 | 0.000000 / 0.000000 | 0.000000 / 0.000000 | 0.00 |
| zesty | `philbot-replay-r7-native` | SUCCESS | 0.002562 / 0.002618 | 0.196736 / 0.178583 | 0.000302 / 0.000904 | 0.001252 / 0.003370 | 2.02 |
| zesty | `philbot-rafale2-swing-shadow` | SUCCESS | 0.000612 / 0.002410 | 0.061817 / 0.062928 | 0.000670 / 0.022462 | 0.000102 / 0.000661 | 0.63 |
| zesty | `philbot-guardian` | SUCCESS | 0.002528 / 0.002439 | 0.089747 / 0.087912 | 0.000080 / 0.000374 | 0.000031 / 0.000150 | 0.95 |
| zesty | `philbot-snapback-v10r1` | SUCCESS | 0.005875 / 0.005698 | 0.218890 / 0.210666 | 0.000027 / 0.000134 | 0.000023 / 0.000113 | 2.31 |
| zesty | `philbot-reversal-research` | SUCCESS | 0.000000 / 0.000065 | 0.000000 / 0.469923 | 0.000000 / 0.000283 | 0.000000 / 0.000007 | 0.00 |
| zesty | `philbot-health` | SUCCESS | 0.003647 / 0.003924 | 0.062093 / 0.090620 | 0.000694 / 0.004408 | 0.000109 / 0.000540 | 0.69 |
| zesty | `philbot-rafale2-hl` | SUCCESS | 0.000521 / 0.000433 | 0.150193 / 0.116785 | 0.000627 / 0.000889 | 0.000011 / 0.000494 | 1.51 |
| zesty | `philbot-rafale2-blofin` | SUCCESS | 0.003460 / 0.003587 | 0.169869 / 0.168678 | 0.000909 / 0.004311 | 0.000107 / 0.000457 | 1.77 |
| zesty | `venue-research-rafale2` | SUCCESS | 0.000000 / 0.000000 | 0.000000 / 0.000000 | 0.000000 / 0.000000 | 0.000000 / 0.000000 | 0.00 |
| zesty | `philbot-rafale2-bitunix` | SUCCESS | 0.000471 / 0.000511 | 0.109426 / 0.097834 | 0.000026 / 0.000121 | 0.000108 / 0.000447 | 1.10 |
| zesty | `philbot-snapback` | SUCCESS | 0.000854 / 0.000741 | 0.140992 / 0.153773 | 0.000011 / 0.000065 | 0.000011 / 0.000056 | 1.43 |
| zesty | `philbot-vortex` | SLEEPING | 0.000000 / 0.000001 | 0.000000 / 0.012518 | 0.000000 / 0.000000 | 0.000000 / 0.000000 | 0.00 |
| zesty | `faithful-passion` | SUCCESS | 0.000003 / 0.000004 | 0.049546 / 0.037702 | 0.000000 / 0.000000 | 0.000000 / 0.000000 | 0.50 |
| zesty | `philbot-signer` | SUCCESS | 0.070796 / 0.091786 | 0.262645 / 0.247901 | 0.000077 / 0.000313 | 0.000066 / 0.000371 | 4.04 |
| dp60 | `triple-relay` | SUCCESS | 0.000374 / 0.000053 | 0.035013 / 0.005077 | 0.000196 / 0.000140 | 0.000530 / 0.000379 | 0.36 |
| dp60 | `triple-blofin` | SUCCESS | 0.000783 / 0.000112 | 0.094354 / 0.014678 | 0.000589 / 0.000421 | 0.000019 / 0.000014 | 0.96 |
| dp60 | `philbot-dp60-readonly` | SUCCESS | 0.000145 / 0.000140 | 0.027654 / 0.035745 | 0.000002 / 0.000012 | 0.000002 / 0.000011 | 0.28 |
| dp60 | `rafale2-blofin-dp60` | SUCCESS | 0.008419 / 0.009686 | 0.173695 / 0.164140 | 0.000914 / 0.003859 | 0.000335 / 0.001130 | 1.91 |
| recent40 | `recent40-observer` | SUCCESS | 0.005581 / 0.006877 | 0.357320 / 0.257548 | 0.000277 / 0.003208 | 0.000104 / 0.000932 | 3.68 |
| r20 | `philbot-r20-hl` | SUCCESS | 0.068133 / 0.034739 | 0.267147 / 0.129626 | 0.000288 / 0.000708 | 0.000119 / 0.000266 | 4.03 |
| r20 | `r20-shadow` | SUCCESS | 0.014821 / 0.016004 | 0.179308 / 0.198032 | 0.000689 / 0.003213 | 0.000149 / 0.000796 | 2.09 |

## Décisions et statut de preuve
- **DÉTECTÉ** : mémoire RECENT40 +38,7% vs 7j, charge R20 +96/106% vs 7j non homogène, refus répétés R7, HWR principal poste, HWR-qualify toujours RAM, nouveaux TRIPLE. Une erreur build RANGE 1nov a été remplacée par déploiement SUCCESS, **aucun arrêt nouveau invoqué**.
- **PROPOSÉ** : profiler HWR RAM/replay de séries sur clone et journaliser le cache/reconnexions; isoler charge RECENT40/R20 et comparer périodes de service actif; backoff R7 après examen du contrat d'entrée et des dépendances, prévention d'effacements SHADOW; vérifier clients de HWR-qualify et prix egress exact par factures.
- **TESTÉ** : métriques/états/configs/logs et e-mails lus, pas de patch logiciel ni benchmark de réduction.
- **INSTALLÉ** : **seulement ce rapport et commentaire de suivi #67**; aucun service, volume, protection, stratégie, budget ou capital changé.
- **OBSERVÉ 24h APRÈS** : HWR observation descriptive après corrections antérieures ; aucun patch FinOps de cette exécution à certifier.
- Issue de suivi : https://github.com/chapsrl1999-lab/philbot-signer/issues/67 . Source de reprise : `operations/PHILBOT_OPERATING_STATE_V1.md`. L'état opérationnel reste prioritaire sur anciens messages; interventions concurrentes RANGE/TRIPLE observées, aucune mutation de ces moteurs faite ici.
