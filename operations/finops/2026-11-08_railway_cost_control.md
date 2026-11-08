# PhilBot — contrôle FinOps du 8 novembre 2026 (lecture seule, environ 13:15–13:29 UTC)

## Méthode et fiabilité des chiffres

- Révision **courante** de `operations/PHILBOT_OPERATING_STATE_V1.md` lue par GitHub `fetch_file` (SHA `0e9cb78d267313fe2a48d69c67df3868023db285`) puis **`fetch_blob`** (1 748 667 caractères, le `fetch_file` du grand fichier renvoie texte vide). État historique réconcilié avec métriques et déploiements du jour; ne pas transformer les anciennes observations en état actuel.
- Railway `list_projects`/`list_services`, `environment_status` et **`describe_service` sur 23/23**, métriques **`get_service_metrics` 1h, 24h, 168h sur 23/23** avec `CPU_USAGE`, `MEMORY_USAGE_GB`, `NETWORK_RX_GB`, `NETWORK_TX_GB`; réponse rate-limited momentanée reprise et validée (PERSONAL snapshots 24h et 168h). Logs `deploy`/`http`/`network-flow` échantillonnés sur HWR, market-data, CASCADE, PERSONAL, replay, soldes-relay; autres logs ciblés RECENT40, R20, signer, Health, Suivi, TRIPLE.
- Prix **officiels** revalidés le 8 novembre : https://docs.railway.com/pricing/plans ; **CPU 20 USD/vCPU-mois ; RAM 10 USD/Go-mois ; egress 0,05 USD/Go ; volume 0,15 USD/Go-mois.** Facturation au temps réel; projection d'un job terminé à zéro usage **≠ économies**. Les deux colonnes réseau sont des **moyennes des métriques RX/TX GB par échantillon**, NON des volumes d'egress public facturé. Projection CPU+RAM seulement; réseau, volumes, agents, abonnements exclus.
- Les compteurs sont indépendants dans le temps ; l'état Railway SUCCESS n'assure pas la disponibilité métier.

## Résultat agrégé

**Inventaire 23 services** : zesty-learning **17**, philbot-rafale2-dp60 **4**, philbot-recent40-observer **1**, philbot-r20-shadow **1** ; contre **22** le 7 novembre, nouveau `philbot-soldes-relay` (SUCCESS le 8 novembre 02:13Z, ~**0,42 USD/mois** théorique CPU+RAM). **Ne pas le qualifier d'inutile** sans dépendances ni tests d'intégration.
**Projection à charge constante CPU+RAM** : **63.44 USD/mois** sur 24h et **61.06 USD/mois** sur 7j (contre 63,25 USD/mois sur 24h le 7 novembre pour 22 services). Écart brut **+0.19 USD/mois**, composition différente ; **ni coût constaté, ni facture, ni gain**. Services avec moyenne CPU=0 et RAM=0 sur la dernière 1h : `philbot-personal-snapshots` (**CRON_FAILED ; 0 aussi sur 24h**) et `philbot-control-shadow-read-proxy` (**SLEEPING ; 0 aussi sur 24h**). **Ne leur attribuer aucune économie supplémentaire si on les supprime**. Tous les autres consomment au moins de la RAM.

## Détail vérifié — CPU vCPU, RAM Go et réseau RX/TX Go moyens par échantillon

| Projet | Service | CPU 24h | RAM 24h | RX/TX 24h | CPU 7j | RAM 7j | RX/TX 7j | Proj. CPU+RAM USD/mois sur 24h | Statut |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| zesty-learning | hybrid-r4-read-check | 0.120685 | 2.949926 | 0.000783/0.000192 | 0.133442 | 2.935121 | 0.001106/0.000258 | 31.91 | ONLINE |
| zesty-learning | hybrid-r4-market-data | 0.000255 | 0.066286 | 0.000033/0.000007 | 0.000082 | 0.018274 | 0.000010/0.000002 | 0.67 | ONLINE |
| zesty-learning | philbot-cascade-shadow | 0.011973 | 0.207372 | 0.000236/0.000013 | 0.002720 | 0.066291 | 0.000139/0.000004 | 2.31 | ONLINE |
| zesty-learning | philbot-personal-snapshots | 0.000000 | 0.000000 | 0.000000/0.000000 | 0.000003 | 0.030116 | 0.000000/0.000000 | 0.00 | CRON_FAILED; 1h 0/0 |
| zesty-learning | philbot-soldes-relay | 0.000080 | 0.042207 | 0.000005/0.000004 | 0.000011 | 0.006033 | 0.000001/0.000001 | 0.42 | ONLINE; nouveau |
| zesty-learning | philbot-outsider-ledger-readonly | 0.000122 | 0.009594 | 0.000000/0.000000 | 0.000069 | 0.007619 | 0.000000/0.000000 | 0.10 | ONLINE |
| zesty-learning | philbot-range-wave-readonly | 0.000138 | 0.011488 | 0.000000/0.000000 | 0.000187 | 0.012304 | 0.000006/0.000001 | 0.12 | ONLINE |
| zesty-learning | philbot-personal-readonly | 0.000185 | 0.011337 | 0.000003/0.000002 | 0.000186 | 0.013163 | 0.000002/0.000001 | 0.12 | ONLINE |
| zesty-learning | philbot-outsider-hl-validation | 0.011360 | 0.312975 | 0.000274/0.000121 | 0.011729 | 0.315044 | 0.000287/0.000118 | 3.36 | ONLINE |
| zesty-learning | philbot-control-shadow-read-proxy | 0.000000 | 0.000000 | 0.000000/0.000000 | 0.000140 | 0.023928 | 0.000008/0.000002 | 0.00 | SLEEPING; 1h 0/0 |
| zesty-learning | philbot-replay-r7-native | 0.009859 | 0.248264 | 0.000156/0.000284 | 0.005012 | 0.220162 | 0.000196/0.000682 | 2.68 | ONLINE; logs REPLAY-R9 429 |
| zesty-learning | philbot-rafale2-swing-shadow | 0.000403 | 0.102832 | 0.000022/0.000049 | 0.000747 | 0.098752 | 0.000434/0.000050 | 1.04 | ONLINE |
| zesty-learning | philbot-guardian | 0.002395 | 0.088035 | 0.000030/0.000014 | 0.002625 | 0.089573 | 0.000036/0.000014 | 0.93 | ONLINE; volume |
| zesty-learning | philbot-health | 0.002446 | 0.093430 | 0.000214/0.000039 | 0.003058 | 0.096689 | 0.000293/0.000047 | 0.98 | ONLINE; volume |
| zesty-learning | philbot-rafale2-hl | 0.002464 | 0.126091 | 0.000054/0.000034 | 0.001273 | 0.134489 | 0.000292/0.000017 | 1.31 | ONLINE; RAFALE3 |
| zesty-learning | philbot-rafale2-blofin | 0.000076 | 0.176582 | 0.000002/0.000002 | 0.000913 | 0.168328 | 0.000095/0.000017 | 1.77 | ONLINE; B&C |
| zesty-learning | philbot-signer | 0.070590 | 0.231149 | 0.000017/0.000007 | 0.072119 | 0.225121 | 0.000027/0.000018 | 3.72 | ONLINE; volume |
| philbot-rafale2-dp60 | philbot-suivi | 0.004065 | 0.064774 | 0.000019/0.000011 | 0.003698 | 0.065961 | 0.000127/0.000016 | 0.73 | ONLINE; volume |
| philbot-rafale2-dp60 | triple-relay | 0.000158 | 0.121261 | 0.000030/0.000074 | 0.000225 | 0.110443 | 0.000057/0.000149 | 1.22 | ONLINE |
| philbot-rafale2-dp60 | triple-blofin | 0.000777 | 0.185260 | 0.000085/0.000009 | 0.000825 | 0.188568 | 0.000156/0.000010 | 1.87 | ONLINE; volume |
| philbot-rafale2-dp60 | philbot-dp60-readonly | 0.000344 | 0.010806 | 0.000007/0.000019 | 0.000291 | 0.015384 | 0.000006/0.000017 | 0.11 | ONLINE; staged |
| philbot-recent40-observer | recent40-observer | 0.008628 | 0.339134 | 0.000424/0.000107 | 0.008455 | 0.337006 | 0.000369/0.000100 | 3.56 | ONLINE; volume |
| philbot-r20-shadow | philbot-r20-hl | 0.073529 | 0.303752 | 0.000208/0.000088 | 0.073381 | 0.285558 | 0.000219/0.000088 | 4.51 | ONLINE; volume |

## Principaux postes, seuils et diagnostics

1. **HWR** `hybrid-r4-read-check` (serviceId `79ebd36d-3960-4535-adf8-16f9e1265b94`) : **31.91 USD/mois** sur 24h ; 7j **32.02**, 1h **0,113384 vCPU / 2,937174 Go** ≈ **31.64 USD/mois** si durable. Base antérieure au correctif 28 octobre : **0,758 vCPU / 3,507 Go ≈ 50,23 USD/mois**. La réduction apparente d'équivalent à charge constante **NE PROUVE NI ÉCONOMIES PAYÉES NI CAUSALITÉ**, même avec une fenêtre purement postérieure : activité, marchés et redéploiements diffèrent. Logs : COLLECTOR 30/91, NO_FRESH_BOUNDARY répété 31/91, silences partiels EPIC/DYDX/SUSHI, `ordersPossible=true` dans derniers collecteurs, réponse proxy HTTP 200 sur 91/91 requêtes échantillonnées; pas de boucle causale confirmée. **PROPOSÉ :** profiler cache/stockage des séries, recalculs, bruit de log sur copie isolée; mesurer 24h homogènes et vérifier protections natives. **AUCUN correctif LIVE par FinOps.** Staged changes **5 en attente**, non appliqués.
2. **R20** ~**4,51 USD/mois**, `philbot-signer` ~**3,72**, **RECENT40** ~**3,56**, **OUTSIDER** ~**3,36** : services actifs au rôle opérationnel. Pas d'écart à la moyenne 7j dépassant 25% en coût total pour ces postes, pas de preuve de trafic facturable anormal; ne pas désactiver.
3. **CASCADE SHADOW** : **2,31 USD/mois** sur 24h contre **0,72** sur 7j (hausse **>25%**, **fenêtre 7j comprend lancement / montée en régime**). Journaux du 8 nov montrent scan toutes les **5 min**, appels données **~35–69 sec**, `gaps=36`, `trades=0`, `open=0`, `equity=1000`. Ce n'est **ni une stratégie condamnée ni une fuite démontrée**. **PROPOSÉ, NON TESTÉ :** examiner la cause des 36 gaps, vérification de l'incrémentalité/cache et des relectures historiques; collecter preuve de dépendance avant tout amortissement ou pause. Service **sans volume** et utilité du SHADOW non certifiée, donc aucune suppression automatisée.
4. **Replay R7/R9** : **2,68 USD/mois** théoriques, logs 91/91 du dernier échantillon `[REPLAY-R9] PUBLIC_HTTP_429`. Erreur récurrente existante; lecture seule prouve le bruit et les retours limités, pas le nombre de requêtes réelles ni la cause exacte. **PROPOSÉ, NON TESTÉ :** cache TTL, backoff jitter sur 429, requêtes conditionnelles et négative cache, sans couper le replay utile, sans toucher trading/alertes; benchmark avant/après et rollback.
5. **PERSONAL snapshots** : dernier état CRON_FAILED/CRASHED, logs `PERSONAL_SNAPSHOT_HTTP_401` et redémarrages du **6 novembre**, **CPU 0 / RAM 0 sur 1h et 24h** ; panne de lecture/fonctionnalité à corriger séparément, **pas une consommation à couper ni une économie à promettre**. `CONTROL shadow read-proxy` : SLEEPING et CPU/RAM nuls sur 24h, non responsable du coût.
6. **Nouveau soldes-relay** en continu (~0,42 USD/mois) : tests pre-deploy, /health OK, service sans volume, origine CASCADE. Nécessité à vérifier par appels/consommateurs avant toute décision, **pas de suppression**. HWR market-data ~0,67 USD/mois, associé à la qualification; pas d'interruption. Sur échantillons réseau, aucune preuve de hausse matérielle d'**egress public facturé**.

## Budget et factures : trois catégories DISTINCTES

- **Usage courant constaté par courriel Railway** : le **7 nov. 2026 à 21:16:59 UTC**, **10,04 USD utilisés** depuis début de cycle, mail `Railway usage alert`. Le **5 nov.** avis **soft limit** à 5 USD franchie pour 5,08 USD, ce **n'est PAS un plafond d'arrêt** ; cet avis précise **fin de cycle 4 décembre 2026**. Source Gmail IDs `1a1b7df31cecc612` / `1a1ad90eb0bee376`. **Aucun nouveau mail de plafond hard, arrêt ou débit après ce message lors de la recherche. Plafond HARD actuel inconnu.** Impossible de certifier un hard stop sous 24–48h ; la pente passée n'est pas un compteur en temps réel. **Ne jamais augmenter automatiquement les plafonds.**
- **Reçu réellement payé** Railway : **71,91 USD le 3 nov. 2026** (`1a1a443a7f09c53c`), usage 3 oct.–3 nov., RAM **54,66**, CPU **6,84**, réseau **9,21**, disk **0,38**, agents **0,82** USD, forfait Hobby 5 USD puis crédit Hobby inclus de 5 USD. **Ne pas ajouter une seconde fois les 5 USD.** Ce reçu n'est pas le coût du cycle courant et n'est pas la projection de 63,44.
- **Autres fournisseurs** : reçu ancien **Claude Pro 32,19 CAD taxes incluses le 19 octobre**, reçu **Claude Max 142,75 CAD payé le 1er novembre après crédit** cité dans précédent relevé, renouvellement futur inconnu; ne pas assimiler CAD/USD, net de taxes, ou un reçu à tous les frais. Nouvelles recherches Gmail après le 1er novembre : aucun reçu ChatGPT / n8n / TradingView identifié. Ne pas en inférer coût zéro.

**Rentabilité 30 jours : NON CALCULABLE.** Ni ledger complet réalisé + flottant de chaque compte réel ni tous les dépôts/retraits, frais et factures cohérents; les résultats du SHADOW ne sont pas revenus. Les frais de marché déjà reflétés dans les PnL ne seraient pas déduits deux fois. Préparer comparaison par devise/hors taxes quand preuves disponibles, sans inventer bénéfice net.

## Actions et garanties

- **DÉTECTÉ** : coût HWR majoritaire (RAM), CASCADE scan 5 min sans trades/gaps, replay limité en 429, PERSONAL CRON_FAILED mais 0 coût CPU/RAM, arrivée soldes-relay; prévisions non assimilées aux factures.
- **PROPOSÉ** : cache incrémental et backoff sur recherche/replay, preuves de dépendances/impact, profiler HWR sur clone, suivre fenêtres stables 24h. Aucun travail de stratégie ni réallocation d'argent proposé.
- **TESTÉ** : *uniquement vérifications en lecture seule* des états/configs/métriques/journaux/Gmail et comparaison prix. **Correctif technique testé = aucun.**
- **INSTALLÉ** : *documentation FinOps GitHub et suivi issue* seulement; **correctif technique = aucun**.
- **OBSERVÉ 24h après une installation FinOps** : **SANS OBJET**, aucun patch de coût déployé.
- **AUCUN BOT LIVE, Health/Guardian, volume, service indispensable, stop/risque/stratégie/capital, limite budgétaire, ou alertes modifiés** ; aucune tâche/services de surveillance créés.

Sources : https://docs.railway.com/pricing/plans ; Railway metrics+logs `get_service_metrics`/`describe_service`/`environment_status` ; Gmail avis de cycle et reçu ; GitHub source d'état courant + issue #67.
