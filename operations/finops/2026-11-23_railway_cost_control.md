# Contrôle FinOps PhilBot — 23 novembre 2026, 08 h 20 EST

## Sources et portée
Lecture en direct : Railway list_projects/list_services, environment_status, get_service_metrics (CPU_USAGE, MEMORY_USAGE_GB, NETWORK_RX_GB, NETWORK_TX_GB, 24 h et 168 h sur 29/29 services), describe_service HWR/BRIQUES/REPLAY/REBOND, get_logs HWR/BRIQUES/REPLAY/REBOND/ALIGNEMENT/B&C, Gmail recherche Railway après 7 novembre, révision courante de operations/PHILBOT_OPERATING_STATE_V1.md. Inventaire : zesty-learning 23, DP60 4, recent40 1, R20 1. Pas d'accès au panneau de facturation en direct ni aux PnL nets 30 jours consolidés.

Tarifs officiels Railway vérifiés le 23/11 : https://railway.com/pricing — CPU 0,00000772 USD/vCPU/s (~20 USD/vCPU-mois), RAM 0,00000386 USD/Go/s (~10 USD/Go-mois), egress 0,05 USD/Go; stockage volume séparé. CPU/RAM facturés au prorata du temps réellement utilisé. Les moyennes RX/TX sont des mesures de débit/usage et ne sont pas directement des Go facturés. **Projection CPU+RAM 24h : 88,19 USD/mois; 7j : 86,48 USD/mois**, à charge constante, sur 29 services. Comparatif 22/11 : 85,15 USD/mois; variation +3,04 USD (+3,57%), pas une facture ni un gain/perte constaté. Les projections 24h des crons n'impliquent PAS qu'ils restent facturés tout le mois après leurs exécutions; les métriques 1h et état cron servent à vérifier le repos.

## Mesures principales (CPU vCPU / RAM Go / RX Go / TX Go, moyennes Railway)
| Service | 24 h CPU | 24 h RAM | 7 j CPU | 7 j RAM | Projection 24h USD/mois | 7j USD/mois |
|---|---:|---:|---:|---:|---:|---:|
| HWR | 0,141177 | 3,064584 | 0,152936 | 3,039514 | 33,47 | 33,45 |
| BRIQUES (cron) | 0,028941 | 0,933571 | 0,028301 | 0,945702 | 9,91 | 10,02 |
| REPLAY | 0,001593 | 0,557916 | 0,001710 | 0,559383 | 5,61 | 5,63 |
| SIGNER | 0,120573 | 0,288814 | 0,119962 | 0,305845 | 5,30 | 5,46 |
| R20 | 0,071749 | 0,280237 | 0,071890 | 0,275678 | 4,24 | 4,19 |
| CASCADE REAL | 0,012408 | 0,384946 | 0,012470 | 0,400318 | 4,10 | 4,25 |
| BANDE & CYCLE | 0,011359 | 0,365625 | 0,006039 | 0,292155 | 3,88 | 3,04 |
| OUTSIDER validation | 0,012304 | 0,343748 | 0,012701 | 0,325774 | 3,68 | 3,51 |
| ALIGNEMENT (cron) | 0,000103 | 0,357112 | 0,000075 | 0,219566 | 3,57 | 2,20 |
| RECENT40 | 0,000832 | 0,160800 | 0,002417 | 0,244080 | 1,62 | 2,49 |
| REBOND+ÉLAN (cron) | 0,000112 | 0,120501 | 0,000028 | 0,032975 | 1,21 | 0,33 |
| ROTATION (cron) | 0,000158 | 0,124243 | 0,000143 | 0,163408 | 1,25 | 1,64 |
Les autres services (SUIVI, TRIPLE, TRIPLE_RELAY, DP60_READ, RAFALE3, SWING, HEALTH, GUARDIAN, MARKET, SOLDES, PERSONAL_READ, OUTSIDER_LEDGER, RANGE_READ, CASCADE_READ) sont inclus dans les totaux. QUATRE, PERSONAL snapshots et PROXY = CPU/RAM 0 sur 24h et 7j. Réseau RX/TX 24h et 7j relevé sur les 29/29; aucune preuve d'egress facturable anormal. Exemple HWR : RX 0,000892/0,001112, TX 0,000213/0,000257; B&C RX 0,000262/0,000155, TX 0,000115/0,000058 (24h/7j).

## États et diagnostics
- HWR ONLINE, dernier déploiement SUCCESS 21/11, volume /data intact. Base avant correctif 28/10 : 0,758 vCPU, 3,507 Go, ~50,23 USD/mois théoriques. Maintenant 0,141177 / 3,064584, 33,47 théoriques. Différence descriptive, **pas une économie facturée ni preuve causale**; une fenêtre 24h mixte avant/après ne permet pas d'attribution. Logs : cycles PREPARED_RUNTIME et 11 414 enregistrements source, répétitions NO_FRESH_BOUNDARY, MARKET_STREAM_PARTIAL_SILENCE ponctuelles sans échec consécutif. Pas de modification LIVE.
- BRIQUES cron réussi, exécuteur **REEL** avec équité observée ~1191,06 USD et cinq positions; 1947 trades historiques recalculés, 142 s. CPU 1h ~0,024596 et RAM moyenne 1h 0,123959 Go malgré RAM courante 1,098883 : mesure instantanée post-job ne prouve pas un conteneur actif ni une facture. Optimisation incrémentale seulement sur clone, parité stricte, rollback, accord si impact LIVE.
- REPLAY ONLINE, 5,61 USD/mois théoriques. Logs HTTP du 23/11 13:20 UTC : paires de GET /replay-r9/proxy HTTP 200 simultanés environ toutes les 0,38 s. **Polling possiblement redondant, non prouvé inutile**. Proposer déduplication/cache TTL court sur clone et test de non-dépendance avant tout déploiement. Pas de correctif testé.
- B&C LIVE ONLINE, +27,6 % en projection 24h vs 7j (+0,84 USD/mois), sous seuil absolu 10 USD. Logs DUO 5 min et LIVE horaire, pas de boucle fautive démontrée; profilage lecture seule sans toucher à la cadence nécessaire au trading.
- ALIGNEMENT cron terminé 4–6 s, CPU/RAM 1h=0, projection 24h 3,57 contre 2,20 7j (+62,6%) mais **pas une preuve de consommation après fin de job**. ROTATION cronSucceeded (dernier 23/11 00:49Z), CPU/RAM 1h=0, donc pas d'alerte coût continu. REBOND cronSucceeded, 154 perps/39 spot/39 ratios et 999 heures lus chaque heure, aucun trade fictif depuis création, volume persistant 5 GB; première fenêtre 7j non homogène, ne pas extrapoler hausse 265% comme dérive. Vérifier utilité après échantillon suffisant; ne pas supprimer volume.
- QUATRE, PERSONAL snapshots, proxy shadow : zéro CPU/RAM 24h/7j, aucune économie nouvelle à revendiquer.
- Statut Railway : 29 services inventoriés, PERSONAL snapshots OFFLINE non-LIVE; pas de nouveaux déploiements FAILED/CRASHED dans les quatre projets. DP60 et R20 conservent des patchs staged non appliqués. Un statut Railway ONLINE ne certifie pas la disponibilité métier : l'état opérationnel lu ce matin documente RECENT40 et R20 bloqués; aucun redémarrage ni changement de sécurité.

## Billing et économie
Gmail Railway consulté le 23/11 : dernier avis d'usage trouvé 10,04 USD du 7 novembre, reçu historique 71,91 USD payé le 3 novembre (preuve antérieure). Aucune nouvelle alerte hard limit trouvée. Cycle annoncé au 4 décembre dans contrôle précédent, **non revérifié dans ce passage**. Plafond actuel et usage courant non vérifiés : **risque d'arrêt dans 24–48 h indéterminable**, ne jamais réutiliser automatiquement l'ancien plafond 55 USD du 28/10. Pas d'augmentation de limite. Reçu Claude Pro CA$32,19 du 19/10 = référence historique seulement; factures ChatGPT, Claude récentes, n8n et TradingView non consolidées. PnL nets réels réalisés + flottants sur 30 jours et dépôts/retraits non réconciliés : revenu net projet non calculable, aucun total partiel présenté comme global.

## Actions et états
**DÉTECTÉ** : REPLAY appels proxy rapprochés/doublés; B&C +27,6 % relatif (+0,84 USD/mois); ALIGNEMENT +62,6 % relatif mais cron arrêté 1h; REBOND encore sans avantage testé; BRIQUES relecture historique et exécuteur REEL.
**PROPOSÉ** : cache/déduplication REPLAY avec tests de parité et rollback; profilage B&C non intrusif; BRIQUES clone avec incrémental et comparaison de 7 cycles; suivi d'utilité REBOND sans toucher au volume.
**TESTÉ** : uniquement lectures métriques/états/config/logs et vérification des tarifs/courriels. Aucun patch testé.
**INSTALLÉ** : aucun correctif FinOps.
**OBSERVÉ 24H APRÈS** : sans objet.
Aucun bot LIVE, Health/Guardian, ordre, stop, stratégie, capital, volume, alerte ou plafond modifié. Issue https://github.com/chapsrl1999-lab/philbot-signer/issues/67
