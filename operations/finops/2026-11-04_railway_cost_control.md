# FinOps PhilBot — 4 novembre 2026 — 29 services Railway, nouveau reçu payé

**Date** : 4 novembre 2026, autour de 08:51–09:05 EST / 13:51–14:05 UTC (fenêtres glissantes). **Projets audités** : zesty-learning (21 services), philbot-rafale2-dp60 (5), philbot-recent40-observer (1), philbot-r20-shadow (2), total **29**. Sources Railway : `list_projects`, `list_services`, `describe_environment`, `environment_status`, `describe_service` (ciblés HWR et B&C), `get_service_metrics` **CPU_USAGE, MEMORY_USAGE_GB, NETWORK_RX_GB, NETWORK_TX_GB sur 1 h, 24 h et 168 h pour les 29 services**, `get_logs` (HWR, PERSONAL, R7/R9, RECENT40, B&C, HWR-qualify et R20 shadow). Descripteurs de déploiement et volumes contrôlés. **Aucune intervention sur les services.**

## Coûts et principaux postes

- **CPU + RAM, projection à charge constante** des moyennes 24 heures : **71.95 USD/mois**; sur moyennes 7 jours : **68.62 USD/mois**. Équivalent mathématique `20 USD/vCPU-mois × moyenne CPU + 10 USD/Go-mois × moyenne RAM`; **ni facture ni coût constaté**, hors volumes et réseau. Référence projet 3 nov : 72,09 USD/mois, comparabilité partielle par plages/deploiements.
- **Seuil 10 USD/mois** : `hybrid-r4-read-check` 31.57 USD (ne signifie pas que le service est inutile). Principaux postes restants : `philbot-r20-hl` 4.24 USD, `recent40-observer` 3.56 USD, `philbot-signer` 3.50 USD, `philbot-outsider-hl-validation` 3.46 USD, `r20-shadow` 2.29 USD.
- **Hausse CPU + RAM >25 %** moyenne 24h vs moyenne 7j : `triple-blofin` +102.9% (2.00 USD/mois), `philbot-bandecycle-shadow` +250.5% (1.69 USD/mois), `philbot-rafale2-swing-shadow` +44.3% (1.08 USD/mois), `triple-relay` +81.3% (0.92 USD/mois), `philbot-personal-snapshots` +250.8% (0.78 USD/mois), `philbot-suivi` +124.1% (0.60 USD/mois). Les nouveaux services / mises en service depuis moins de 7 jours rendent le ratio structurellement trompeur; diagnostiquer avant modification.
- **Réseau** : moyennes par échantillon 15 min RX/TX dans le tableau; indicateurs intégrés (`moyenne × 97 points`) 24h = environ **7.41 Go RX / 3.66 Go TX**, 7 jours TX environ **21.07 Go**. ATTENTION : ces métriques Railway ne sont **pas une assiette de facturation egress validée**; réseau interne/flux, unités et échantillonnage peuvent différer. À titre illustratif seulement, TX 24h ×30 ×0,05 ferait **5.49 USD/mois** si tout était egress public. Tarif officiel egress public 0,05 USD/Go. Aucun trafic anormal payé n'a été démontré par cette seule intégration.
- **Dernière heure CPU/RAM à zéro (61 points)** : `philbot-control-shadow-read-proxy` (**SLEEPING**, pas de coût compute horaire), `philbot-rafale2-blofin` (**ONLINE, 1/1 réplique, GET /health 200 à 14:01 UTC et BARRE 13:02 UTC**). Dans le deuxième cas, zéro métrique malgré des preuves du service LIVE en ligne : **ne surtout pas le considérer terminé ou stoppable**. Les jobs de recherche supprimés ou terminés hors inventaire n'ont pas de projection de coût futur; consommation antérieure facturée au prorata.
- **État Railway** : 29 services présents; 1 incident actuel `philbot-personal-snapshots` cron FAILED, HTTP401 récurrents toutes 15 min, dernier 13:47Z; HWR 5 changements de configuration STAGED **non déployés**; Control proxy SLEEPING; les autres derniers déploiements affichent SUCCESS. SUCCESS ne certifie ni ordres ni stops natifs.

## HWR comparé à sa base pré-correctif

- HWR `hybrid-r4-read-check` id `79ebd36d-3960-4535-adf8-16f9e1265b94` : moyenne **24h 0.122910 vCPU / 2.9114 Go RAM => 31.57 USD/mois**; moyenne **7j 0.144354 vCPU / 2.8824 Go RAM => 31.71 USD/mois**.
- Référence **avant le correctif du 28 oct 2026** : **0,758 vCPU et 3,507 Go RAM = 50,23 USD/mois** si charge constante. Écart descriptif **-18.66 USD/mois**, **PAS d'économie payée, prouvée, ni attribuable causalement au correctif**. Une fenêtre 24h **mixte avant/après** ne prouve pas un gain post-déploiement; même si la fenêtre actuelle est postérieure au 28 octobre, variations de charge et déploiement du 2 novembre empêchent l'attribution.
- Runtime HWR `06cf6aeb-349d-445c-bb72-55c198821cfc` SUCCESS, branche `feat/hwr-c-sans-diamant-20261102`, volume `hybrid-r4-public-candles` monté sur /data, 5 modifications de configuration STAGED. Collecteur ~1/min, messages `PREPARED_RUNTIME NO_FRESH_BOUNDARY` entre bougies, `MARKET_STREAM_PARTIAL_SILENCE` ponctuels; pas de boucle infinie ni fuite prouvée. **Proposé non testé/ni installé** : profiler historique/cache/recalculation et fréquence du collecteur hors production, tests de neutralité d'exécution et rollback avant tout changement LIVE.

## Causes ciblées, recommandations réversibles

- **PERSONAL snapshots #82 :** cron `*/15` retourne `PERSONAL_SNAPSHOT_HTTP_401` (12:49,13:02,13:19,13:34,13:47Z), cause observable = autorisation rejetée, pas preuve d'une fuite de CPU ni d'un coût majeur. Vérifier token et droits sans l'exposer, restaurer le flux sur clone et valider ≥2 exécutions effectives successives sans masquer l'alerte; ne pas désactiver le service de monitoring.
- **REPLAY R7/R9 :** nombreuses erreurs `PUBLIC_HTTP_429` groupées autour de 12:30,13:00,13:31Z alors que le proxy répond HTTP200 aux appels. Cause suspectée : burst de requêtes/quotas upstream ou cache absent. **Proposer** cache/déduplication sur symboles-bougies, backoff jitter borné et tests replay sur clone; aucune modification des entrées marché et aucune correction installée.
- **R20 shadow :** GET `/control-card` et `/shadow/positions` toutes ~30 secondes observés dans les logs, HTTP200. Mesurer les requêtes et dépendances avant éventuelle déduplication côté lecteur non critique; ne jamais casser les stats en temps réel et ne pas confondre coût actuel modeste et économie potentielle certifiée.
- **HWR qualify node22 :** service encore consommateur 1h, mais environ 0.86 USD/mois à charge constante; dernier log inexistant dans le relevé. Vérifier dépendances et utilité de recherche, aucune suppression autorisée sans preuves et rollback.
- **RETOURS 0 CPU /0 RAM** : proxy Control SLEEPING, pas un poste de coûts futurs tant qu'il dort. B&C LIVE a une mesure 1h nulle malgré online/health 200, ne pas traiter comme job terminé.

## Factures, plafonds et rentabilité réelle

- **Railway, reçu acquitté #2308-0620 : 71,91 USD payés le 3 novembre 2026**, période d'utilisation **3 oct–3 nov**; reçu Gmail le 4 nov 01:54:18Z, id `1a1a443a7f09c53c`. Ventilation du reçu : mémoire **54,66 USD**, CPU **6,84 USD**, réseau **9,21 USD**, disk **0,38 USD**, agent usage **0,82 USD**, somme **71,91 USD**. Forfait Hobby **5 USD** du 3 nov au 3 déc et crédit d'utilisation **-5 USD** se compensent; **ne pas les compter deux fois**. Reçu Railway couvrant le workspace/fournisseur, non exclusivement ces quatre projets.
- Ancien avis de **60,08 USD utilisés / plafond alors 80 USD** le 30 oct, date de reset annoncée alors **4 nov**. **Nouvelle preuve plus récente : cycle 3 nov–3 déc** selon reçu; les dates affichées diffèrent, et l'usage/plafond **courants** du nouveau cycle sont **non vérifiés par les sources disponibles**. On ne peut certifier un arrêt sous 24–48h ni accroître les limites automatiquement. Le 28 oct, usage 55,08 USD avec limite alors 55 USD avait provoqué un arrêt global.
- Tarif officiel Railway : CPU **20 USD/vCPU-mois**, mémoire **10 USD/Go-mois**, sortie réseau **0,05 USD/Go**, volume **0,15 USD/Go-mois**, facturation prorata; https://docs.railway.com/pricing/plans (consulté 4 nov).
- Claude Pro reçu **32,19 CAD taxes incluses** le 19 octobre, tandis que Max a un reçu plus récent distinct (ne pas additionner Pro comme récurrence Max). Aucune facture universelle ChatGPT/Claude/n8n/TradingView sans sources vérifiées. PnL réels consolidés sur 30 jours (réalisé + flottant, dépôts/retraits neutralisés, frais déjà déduits, même devise) **non disponibles**; bénéfice net projet PhilBot **non calculable**. Ne pas faire de total global trompeur.

## État d'avancement et limites

**DÉTECTÉ** : vraie facture 71,91 USD, RAM majoritaire, incidents PERSONAL 401 et Replay 429, HWR charge dominante. **PROPOSÉ** : profilage/cache/backoff tests hors LIVE, contrôle dépendances et autorisations. **TESTÉ** : lecture vérifiée des sources et mesures, **pas de correctif de code testé**. **INSTALLÉ** : documentation FinOps uniquement ; **aucune correction technique installée**. **OBSERVÉ 24 h après correctif** : sans objet. Aucune optimisation financière facturée affirmée; ne pas toucher aux ressources LIVE, Health/Guardian, volumes, positions, ordres, stops, sizing, risque, capital, plafonds.
 
## Inventaire mesuré — valeurs moyennes des échantillons, 24 heures et 7 jours

`RX`/`TX` sont des indicateurs en Go par échantillon Railway; les agrégats réseau ne représentent **pas** directement une facture.

| Projet | Service | Dernier état déploiement | 24h vCPU | 24h RAM Go | 24h RX Go/point | 24h TX Go/point | 24h CPU+RAM USD/mois | 7j vCPU | 7j RAM Go | 7j RX Go/point | 7j TX Go/point | 7j CPU+RAM USD/mois | 1h CPU/RAM |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| zesty-learning | `hybrid-r4-read-check` | SUCCESS (5 STAGED) | 0.122910 | 2.9114 | 0.018284 | 0.004174 | 31.57 | 0.144354 | 2.8824 | 0.018044 | 0.004218 | 31.71 | activité |
| philbot-r20-shadow | `philbot-r20-hl` | SUCCESS | 0.073506 | 0.2768 | 0.004325 | 0.001636 | 4.24 | 0.066874 | 0.2531 | 0.002754 | 0.001035 | 3.87 | activité |
| philbot-recent40-observer | `recent40-observer` | SUCCESS | 0.009100 | 0.3375 | 0.006231 | 0.001599 | 3.56 | 0.007524 | 0.3056 | 0.004411 | 0.001268 | 3.21 | activité |
| zesty-learning | `philbot-signer` | SUCCESS | 0.073780 | 0.2022 | 0.000608 | 0.000469 | 3.50 | 0.075715 | 0.2387 | 0.000549 | 0.000516 | 3.90 | activité |
| zesty-learning | `philbot-outsider-hl-validation` | SUCCESS | 0.011510 | 0.3229 | 0.005171 | 0.001823 | 3.46 | 0.011857 | 0.3312 | 0.004586 | 0.001741 | 3.55 | activité |
| philbot-r20-shadow | `r20-shadow` | SUCCESS | 0.015585 | 0.1974 | 0.005425 | 0.001210 | 2.29 | 0.015398 | 0.1775 | 0.005135 | 0.001155 | 2.08 | activité |
| zesty-learning | `philbot-snapback-v10r1` | SUCCESS | 0.005583 | 0.2083 | 0.000201 | 0.000170 | 2.19 | 0.005710 | 0.2141 | 0.000203 | 0.000171 | 2.26 | activité |
| zesty-learning | `philbot-replay-r7-native` | SUCCESS | 0.002496 | 0.2112 | 0.002248 | 0.011937 | 2.16 | 0.003350 | 0.1728 | 0.002128 | 0.008463 | 1.79 | activité |
| philbot-rafale2-dp60 | `triple-blofin` | SUCCESS | 0.000740 | 0.1989 | 0.001196 | 0.000137 | 2.00 | 0.000455 | 0.0979 | 0.001831 | 0.000080 | 0.99 | activité |
| philbot-rafale2-dp60 | `rafale2-blofin-dp60` | SUCCESS | 0.003181 | 0.1684 | 0.000822 | 0.000300 | 1.75 | 0.005878 | 0.1699 | 0.002747 | 0.001054 | 1.82 | activité |
| zesty-learning | `philbot-bandecycle-shadow` | SUCCESS | 0.000058 | 0.1691 | 0.000005 | 0.000003 | 1.69 | 0.000040 | 0.0482 | 0.000102 | 0.000002 | 0.48 | activité |
| zesty-learning | `philbot-rafale2-blofin` | SUCCESS | 0.000551 | 0.1434 | 0.000449 | 0.000399 | 1.44 | 0.002891 | 0.1651 | 0.005089 | 0.000669 | 1.71 | 0 CPU/RAM* |
| zesty-learning | `philbot-rafale2-hl` | SUCCESS | 0.000979 | 0.1345 | 0.007363 | 0.000225 | 1.36 | 0.000567 | 0.1307 | 0.003828 | 0.000417 | 1.32 | activité |
| zesty-learning | `philbot-snapback` | SUCCESS | 0.000423 | 0.1327 | 0.000029 | 0.000016 | 1.34 | 0.000769 | 0.1391 | 0.000079 | 0.000069 | 1.41 | activité |
| zesty-learning | `philbot-rafale2-swing-shadow` | SUCCESS | 0.000822 | 0.1066 | 0.008922 | 0.000693 | 1.08 | 0.000675 | 0.0736 | 0.005197 | 0.000724 | 0.75 | activité |
| zesty-learning | `philbot-rafale2-bitunix` | SUCCESS | 0.000430 | 0.1065 | 0.000196 | 0.000828 | 1.07 | 0.000494 | 0.1043 | 0.000192 | 0.000758 | 1.05 | activité |
| zesty-learning | `philbot-health` | SUCCESS | 0.003399 | 0.0890 | 0.005280 | 0.000788 | 0.96 | 0.003710 | 0.0952 | 0.005588 | 0.000821 | 1.03 | activité |
| philbot-rafale2-dp60 | `triple-relay` | SUCCESS | 0.000169 | 0.0918 | 0.000439 | 0.001065 | 0.92 | 0.000164 | 0.0505 | 0.000661 | 0.001761 | 0.51 | activité |
| zesty-learning | `hybrid-hwr-qualify-node22-20261010` | SUCCESS | 0.000363 | 0.0853 | 0.000492 | 0.000098 | 0.86 | 0.000962 | 0.0870 | 0.002344 | 0.000214 | 0.89 | activité |
| zesty-learning | `philbot-guardian` | SUCCESS | 0.002729 | 0.0772 | 0.000547 | 0.000199 | 0.83 | 0.002637 | 0.0970 | 0.000588 | 0.000227 | 1.02 | activité |
| zesty-learning | `philbot-personal-snapshots` | CRASHED (cron) | 0.000006 | 0.0779 | 0.000000 | 0.000000 | 0.78 | 0.000003 | 0.0222 | 0.000000 | 0.000000 | 0.22 | activité |
| zesty-learning | `philbot-trains-bitunix` | SUCCESS | 0.000052 | 0.0676 | 0.000021 | 0.000142 | 0.68 | 0.000039 | 0.0894 | 0.000015 | 0.000103 | 0.89 | activité |
| zesty-learning | `philbot-bitunix-phoenix-shadow-v1` | SUCCESS | 0.003821 | 0.0589 | 0.007831 | 0.009495 | 0.67 | 0.003511 | 0.0609 | 0.007868 | 0.005543 | 0.68 | activité |
| philbot-rafale2-dp60 | `philbot-suivi` | SUCCESS | 0.003236 | 0.0536 | 0.000046 | 0.000013 | 0.60 | 0.001488 | 0.0239 | 0.001831 | 0.000051 | 0.27 | activité |
| philbot-rafale2-dp60 | `philbot-dp60-readonly` | SUCCESS | 0.000230 | 0.0213 | 0.000091 | 0.000254 | 0.22 | 0.000181 | 0.0279 | 0.000049 | 0.000116 | 0.28 | activité |
| zesty-learning | `faithful-passion` | SUCCESS | 0.000003 | 0.0213 | 0.000000 | 0.000000 | 0.21 | 0.000003 | 0.0433 | 0.000000 | 0.000000 | 0.43 | activité |
| zesty-learning | `philbot-control-shadow-read-proxy` | SLEEPING | 0.000224 | 0.0205 | 0.000180 | 0.000068 | 0.21 | 0.000189 | 0.0200 | 0.000130 | 0.000040 | 0.20 | 0 CPU/RAM* |
| zesty-learning | `philbot-personal-readonly` | SUCCESS | 0.000188 | 0.0187 | 0.000032 | 0.000018 | 0.19 | 0.000198 | 0.0151 | 0.000046 | 0.000027 | 0.15 | activité |
| zesty-learning | `philbot-range-wave-readonly` | SUCCESS | 0.000152 | 0.0118 | 0.000005 | 0.000003 | 0.12 | 0.000297 | 0.0130 | 0.000275 | 0.000057 | 0.14 | activité |
 
*B&C LIVE : métriques 1h à zéro sans arrêt ni sleeping selon Railway; le contrôle de disponibilité est fondé sur l'état replica, les logs et HTTP200. Proxy Control SLEEPING : aucun calcul facturé observé en dernière heure.*
