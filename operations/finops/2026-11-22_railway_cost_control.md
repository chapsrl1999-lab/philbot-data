# Contrôle FinOps PhilBot — 22 novembre 2026 (EST)

## Périmètre et sources
Railway list_services, environment_status, get_service_metrics, describe_service et get_logs consultés. **29 services** : zesty-learning 23, DP60 4, Recent40 1, R20 1. CPU_USAGE, MEMORY_USAGE_GB, NETWORK_RX_GB, NETWORK_TX_GB **24h et 168h sur 29/29**; 1h ciblée sur crons et services inactifs. Statuts : PERSONAL snapshots offline (auxiliaire), autres environnements sans incident de déploiement signalé; DP60 et R20 conservent leurs patchs staged, non appliqués.

Tarifs Railway officiels : CPU 20 USD/vCPU-mois, RAM 10 USD/Go-mois, egress 0,05 USD/Go, volumes 0,15 USD/Go-mois (https://docs.railway.com/pricing/plans). Facturation proratisée à la durée effective. Moyennes RX/TX lues pour tous les services mais non assimilables directement à des Go d'egress facturés. Projections CPU+RAM **85,15 USD/mois (moyennes 24h)** et **85,92 USD/mois (moyennes 7j)**, contre 85,99 USD/mois 24h au 21/11. Projections à charge constante, ni dépenses constatées ni factures; hors egress, volumes, Agent, abonnement, taxes et crédits. Aucune économie réalisée démontrée.

## Postes et anomalies
- **HWR** : 24h CPU 0,148319 vCPU, RAM 3,040006 Go, projection **33,37 USD/mois**; 7j 0,154779 et 3,032963, projection 33,43. Base avant 28 octobre CPU 0,758 / RAM 3,507, projection 50,23. Valeurs plus basses mais **aucun gain causal ni économie facturée prouvés**. Une fenêtre 24h mixte avant/après n'est pas probante. Dernier déploiement SUCCESS 21/11, volume /data intact. Logs : 11 408 records et ~25,9 secondes d'évaluation, pas de boucle infinie prouvée.
- **BRIQUES** : 24h 0,029837 vCPU / 0,913862 Go = **9,74 USD/mois**, 7j 10,59. Cron horaire réussi, logs 22/11 : 1 947 trades historiques recalculés, 153 secondes, exécuteur **REEL**, ouverture FIL-USDT, 6 positions. Ne pas intervenir sur LIVE. Benchmark incrémental uniquement sur clone avec parité stricte et rollback.
- **REPLAY** : 24h 0,001585 / 0,559646 = **5,63 USD/mois**, 7j 5,63. Logs HTTP : rafales de GET /replay-r9/proxy en 200 espacées d'environ 0,38 seconde et parfois doublées à la même milliseconde. Polling redondant suspecté; cache/déduplication réversible proposé, non testé.
- **SIGNER 5,26**, **CASCADE REAL 4,26**, **R20 4,02**, **OUTSIDER validation 3,58** USD/mois projetés (24h).
- **BANDE & CYCLE** : 24h 0,011270 vCPU / 0,361766 Go = **3,84 USD/mois**, 7j 2,74, soit **+40,3% relatif**, mais +1,10 USD/mois seulement. Logs 5 minutes direct avec traitements slowMs environ 24–50s; plusieurs déploiements dans fenêtre. Profilage non intrusif proposé, aucune modification LIVE.
- **RECENT40** : 1,59 USD/mois 24h, 2,71 sur 7j; aucune économie causale inférée.
- **Nouveau REBOND + ÉLAN ombre** : service créé 21/11, cron horaire réussi 22/11, volume persistant 5 GB; 24h CPU 0,0000827 / RAM 0,096960 = **0,97 USD/mois théoriques**. Logs : 154 perps, 39 spot, 39 ratios, 999h, compte fictif 1000 USD, zéro trade et position, état envoyé à PhilBot Suivi. Utilité non encore démontrée, pas de suppression ni modification du volume.
- QUATRE, PERSONAL snapshots et proxy shadow : **CPU=RAM=0 sur 1h/24h/7j**; aucun gain à revendiquer en les arrêtant. ROTATION et ALIGNEMENT : **CPU=RAM=0 sur 1h**, jobs terminés; RAM courante non nulle sur 24h ne prouve pas la facturation après exécution. PERSONAL snapshots demeure offline (1 critical service), sans preuve d'impact LIVE.
- Aucun trafic egress facturable anormal démontré; RX/TX relevés pour 29/29, mais pas convertis abusivement en facturation.

## Billing et rentabilité
Gmail Railway consulté (novembre et depuis 14/11) : dernier usage confirmé **10,04 USD le 07/11 21:16 UTC**, soft limit 5 USD, fin de cycle annoncée **04/12/2026** par mail du 05/11. Reçu historique Railway payé 71,91 USD le 03/11. Aucun nouvel avis de billing retrouvé. Usage et HARD cap actuels inconnus : **arrêt dans 24–48h non calculable**; ancien plafond 55 USD du 28/10 non réutilisé, aucune hausse de limite. Reçus Claude CAD historiques distincts des factures USD; factures complètes ChatGPT, n8n, TradingView non vérifiées. PnL nets réels consolidés 30j et transferts non réconciliés : rentabilité nette globale non calculable.

## Actions
**DÉTECTÉ** : REPLAY polling possiblement redondant; B&C +40,3% relatif (+1,10 USD/mois); BRIQUES recalcul 1947 trades avec exécuteur réel; nouveau REBOND fictif avec volume.
**PROPOSÉ** : déduplication/cache REPLAY sur clone après preuve de non-dépendance; profilage B&C sans toucher à la stratégie; benchmark incrémental BRIQUES sur clone et tests de parité; revoir utilité REBOND après historique.
**TESTÉ** : métriques, inventaire, états, descriptions, journaux, tarifs et courriels, en lecture seule. Aucun patch de code FinOps testé.
**INSTALLÉ** : aucun correctif FinOps.
**OBSERVÉ 24h APRÈS** : sans objet.
Aucun bot LIVE, Health/Guardian, volume, ordre, stop, stratégie, capital, alerte ou plafond modifié.

Suivi : https://github.com/chapsrl1999-lab/philbot-signer/issues/67
