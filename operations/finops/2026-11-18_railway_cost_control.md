# Contrôle FinOps PhilBot — 18 novembre 2026 (08:05–08:15 EST, relevés connecteurs)

## Périmètre et preuve
Railway production : zesty-learning 22 services, philbot-rafale2-dp60 4, philbot-recent40-observer 1, philbot-r20-shadow 1 = **28 services**. Inventaire list_services, environment_status (10 premiers par projet, totalServices complet), get_service_metrics CPU_USAGE, MEMORY_USAGE_GB, NETWORK_RX_GB, NETWORK_TX_GB 24h et 168h pour **28/28**; 1h contrôlée pour HWR, BRIQUES, SIGNER et CASCADE. describe_service ciblé sur HWR, BRIQUES, ROTATION, QUATRE et PERSONAL snapshots; journaux ciblés HWR, BRIQUES, REPLAY. Les moyennes réseau sont des mesures de séries échantillonnées, **pas un total d'egress facturable**.

Tarifs officiels : https://docs.railway.com/pricing et https://docs.railway.com/pricing/plans : CPU 20 USD/vCPU-mois, RAM 10 USD/Go-mois, egress 0,05 USD/Go, volumes 0,15 USD/Go-mois, ressources proratisées à la minute. Projection indicative = 20×CPU moyen + 10×RAM moyenne; elle n'est ni usage facturé ni facture, exclut egress/volumes/agent/crédits/taxes/abonnement. Pour les cron terminés, distinguer mémoire moyenne observée et mémoire réellement facturée; le point CPU courant 0 ne prouve pas RAM arrêtée.

## Projections CPU+RAM (USD/mois théoriques)
| Service | 24h | 7j |
|---|---:|---:|
| HWR hybrid-r4-read-check | 32,63 | 32,74 |
| BRIQUES | 10,16 | 8,01 |
| SIGNER | 5,46 | 5,38 |
| REPLAY R7/R9 | 5,63 | 4,48 |
| CASCADE REAL (nom Railway shadow) | 4,39 | 4,20 |
| R20 HL | 4,19 | 4,11 |
| OUTSIDER validation | 3,44 | 3,31 |
| RECENT40 | 2,92 | 3,29 |
| ROTATION cron | 1,83 | 0,53 |
| ALIGNEMENT cron | 1,29 | 1,95 |
| QUATRE retiré | 0,00 | 12,42 |
| Autres 17 services | 11,92 | 12,57 |
| **Total 28** | **83,86** | **92,99** |

Total 7j hors QUATRE déjà retiré = ~80,57 USD/mois; 7j mélange des régimes historiques, donc ne pas présenter 92,99 comme charge actuelle. Comparaison projection 24h 17/11 86,26 => baisse indicative ~2,40 USD/mois, **pas économie démontrée**.

HWR 24h CPU 0,13400 vCPU, RAM 2,99532 Go; 7j CPU 0,14403, RAM 2,98571. Base avant correctif 28/10 CPU 0,758, RAM 3,507, soit 50,23 USD/mois théoriques. La différence descriptive ne prouve ni gain causal ni réduction de facture; 24h mixte avant/après correctif non probant. Déploiement SUCCESS du 17/11 08:41Z, service LIVE avec volume /data : **ne pas modifier sans accord et rollback**.

## Anomalies, causes, état
- **BRIQUES** : 10,16 USD/mois 24h vs 8,01 sur 7j (+26,8%, +2,15 USD/mois indicatifs). Cron horaire, aucun volume; journaux 18/11 12:11–12:14Z : univers horaire 23s, Structure/Cassure/LIGNE 1933 trades 67s, Range Rejection prêt 140s, terminé 144s. **Exécuteur REEL** équité 286,99 USD, 6 positions et 3 trades fermés au relevé; aucun ordre nouveau ce cycle. La simulation fictive dans le même processus ne signifie pas que le service entier est shadow. **DÉTECTÉ** recalcul historique coûteux, **PROPOSÉ** snapshot incrémental/cache avec parité intégrale sur clone, **NON TESTÉ / NON INSTALLÉ**, aucune modification du live.
- **REPLAY** : 5,63 vs 4,48 (+25,7%, +1,15 USD/mois indicatifs). Journaux disponibles montrent anciennes rafales PUBLIC_HTTP_429/400 du 12/11, aucune preuve de persistance au 18/11 dans l'extrait. **PROPOSÉ** mesurer fraîchement les 429 et tester backoff/jitter/cache sur clone; pas de correction installée.
- **ROTATION** : 1,83 vs 0,53, fenêtre 7j mêlant lancement et fréquence quotidienne, ne pas qualifier automatiquement de fuite. Dernier cron réussi 18/11 00:47Z, pas de volume; pas de preuve de consommation anormale après fin.
- **QUATRE** : 0 CPU et RAM sur 24h, cron factice annuel, retiré; aucune économie nouvelle attribuée.
- **PERSONAL snapshots** : cronFailed depuis 06/11, 0 CPU et RAM 24h/7j, aucun gain compute à retirer. **SHADOW proxy** : 0 CPU et RAM 24h, aucune économie actuelle.
- **HWR** 1h CPU 0,12034, RAM 2,98131, CPU courant 0 mais RAM courante 2,8964 : service LIVE, ne pas interpréter CPU instantané nul comme arrêt. Logs 13:00Z PREPARED READY, projection 25,94s, MARKET_STREAM_PARTIAL_SILENCE ponctuel EPIC/NEO avec consecutiveFailures=0.
- **R20** online, Health/Guardian/RECENT40 online. Zesty 22 services, 1 incident PERSONAL snapshots; DP60 4/4 sans incident; R20 1/1, RECENT40 1/1 sans incident infrastructure. Les statuts Railway ne certifient pas le readiness métier.
- Aucune hausse globale >10 USD/mois à charge constante vs 17/11, aucun nouveau service inutile démontré, pas de trafic facturable anormal démontré. Egress réel non calculé avec les moyennes RX/TX; utiliser facturation Railway pour confirmer.

## Facturation et rentabilité
Gmail recherche Railway après 07/11 : seul courriel usage **10,04 USD au 07/11 21:16Z**, plus bulletin de sécurité 13/11, aucun avis plus récent de hard-stop. Ancien usage 55,08 USD/limite 55 USD au 28/10 historique, **plafond actuel inconnu**; cycle annoncé fin 04/12 mais non reconfirmé par source fraîche. Risque d'arrêt sous 24–48h **indéterminable**, ne pas augmenter le plafond. Facture Railway payée 71,91 USD le 03/11 (preuve des contrôles antérieurs, non relue ici). Claude Pro 32,19 CAD le 19/10, Claude Max 142,75 CAD le 01/11 sont des reçus historiques distincts, pas des factures USD Railway. Aucun total global ChatGPT/Claude/n8n/TradingView sans preuves. PnL net réel 30j (réalisé+flottant, dépôts/retraits neutralisés, sans double compte) indisponible : résultat économique global non calculé.

## Suivi
DÉTECTÉ : BRIQUES +26,8% relatif, REPLAY +25,7% relatif, aucune hausse matérielle >10 USD/mois. PROPOSÉ : benchmark incrémental BRIQUES sur clone, diagnostic REPLAY, vérification facturation RAM cron. TESTÉ : inventaire, métriques, états, configuration ciblée, journaux et tarifs. INSTALLÉ : aucun correctif FinOps. OBSERVÉ 24h APRÈS : sans objet. Aucune mutation LIVE/Health/Guardian/volume/stratégie/risque/capital/plafond. Suivi : https://github.com/chapsrl1999-lab/philbot-signer/issues/67.
