# PhilBot FinOps — contrôle du 21 novembre 2026 (13:50 UTC)

## Périmètre et preuves
Inventaire Railway production : zesty-learning 22 services, philbot-rafale2-dp60 4, philbot-recent40-observer 1, philbot-r20-shadow 1 = **28 services**. environment_status : zesty 1 incident (PERSONAL snapshots, cronFailed depuis 06/11), les trois autres sans incident courant; DP60 conserve un patch staged sur reader, R20 un patch staged sans changements. Mesures get_service_metrics CPU_USAGE, MEMORY_USAGE_GB, NETWORK_RX_GB, NETWORK_TX_GB, fenêtres 24h et 168h obtenues pour les 28 services. Mesures 1h vérifiées sur HWR, BRIQUES, REPLAY, SIGNER, R20, RECENT40, CASCADE, ROTATION, ALIGNEMENT, SWING et proxy. describe_service sur HWR, BRIQUES, REPLAY et journaux correspondants. Aucun changement de production.

Tarif officiel https://railway.com/pricing consulté le 21/11 : CPU 0,00000772 USD/vCPU/s (~20 USD/vCPU/mois), RAM 0,00000386 USD/Go/s (~10 USD/Go/mois), egress service 0,05 USD/Go. Facturation à la seconde. Projection indicative ci-dessous = 20×CPU moyen + 10×RAM moyenne, sur mois conventionnel; exclut egress, volumes, abonnements, crédits, taxes, Agent. Les NETWORK_RX/TX sont des mesures échantillonnées, **pas des volumes cumulés facturés** : aucun coût egress extrapolé sans validation de leur sémantique.

## Chiffres vérifiés
Projection CPU+RAM 24h **85,99 USD/mois** et 7j **86,64 USD/mois**, contre projection du 20/11 de 84,25 USD/mois (+1,74, +2,1 %). Ce sont des scénarios à charge constante, **ni usage réellement facturé ni facture**.

| Service | CPU 24h / 7j (vCPU) | RAM 24h / 7j (Go) | RX 24h / 7j (Go métrique) | TX 24h / 7j (Go métrique) | Projection 24h / 7j USD/mois |
|---|---|---|---|---|---|
| HWR hybrid-r4-read-check | .17217 / .15313 | 3.06930 / 3.02304 | .001537 / .001226 | .000343 / .000276 | 34.14 / 33.29 |
| BRIQUES | .02856 / .03003 | .88664 / 1.03154 | .000179 / .000342 | .0000184 / .0000275 | 9.44 / 10.92 |
| REPLAY | .001654 / .003132 | .55959 / .55870 | .0001009 / .0001097 | .0000867 / .0001237 | 5.63 / 5.65 |
| SIGNER | .12259 / .11809 | .30743 / .31076 | .0000239 / .0000200 | .00000856 / .00000640 | 5.53 / 5.47 |
| CASCADE REAL | .01310 / .01222 | .39520 / .40688 | .000253 / .000271 | .0000850 / .0000767 | 4.21 / 4.31 |
| BANDE & CYCLE | .01063 / .002867 | .38985 / .24385 | .000224 / .0000828 | .0000892 / .0000263 | 4.11 / 2.50 |
| R20 | .06982 / .07194 | .26396 / .27221 | .0001448 / .0001445 | .0000700 / .0000699 | 4.04 / 4.16 |
| OUTSIDER validation | .01178 / .01266 | .33058 / .31482 | .000334 / .000423 | .000126 / .000132 | 3.54 / 3.40 |
| autres 20 services | agrégés dans total | | | | 15.35 / 15.11 |

HWR référence pré-correctif 28/10 : CPU 0,758 vCPU, RAM 3,507 Go (~50,23 USD/mois à charge constante). 24h actuelles 0,17217 et 3,06930; baisse apparente, **pas de preuve d'économie causale**. Une fenêtre 24h mixte avant/après déploiement ne suffit pas. Nouveau déploiement HWR SUCCESS le 21/11 08:54Z : pas de conclusion post-déploiement sur une fenêtre mixte.

## Investigations et décisions
- **BANDE & CYCLE** : hausse 64,7 % de projection 24h vs 7j (+1,62 USD/mois) et hausse RX/TX. Journaux montrent cycles toutes les 5 minutes, récupération directe et traitement lent 24–50 s, mais service LIVE; ne pas réduire polling, modifier règles ou couper sans accord. **DÉTECTÉ**; examiner temps d'exécution et éventuelle répétition de fetch hors chemin métier sur clone. Aucun correctif testé.
- **REPLAY** : HTTP proxy /replay-r9/proxy renvoie 200, mais extrait des 100 dernières requêtes montre rafales de GET à quelques centaines de millisecondes d'intervalle, deux clients node, plus Recent40 GapRepair. Trafic potentiellement redondant; les 429 historiques ne sont pas confirmés dans cet extrait. **DÉTECTÉ**, proposer déduplication/coalescence et cache TTL sur clone avec parité des réponses et sans ralentir les données nécessaires au LIVE. Pas d'intervention sans preuve de dépendances.
- **BRIQUES** : cron hourly réussi, 146–151 s, reconstruit 1944 trades historiques. Journal distingue simulation et exécuteur **REEL**, équité réelle observée 658,45 USD, 5 positions, 9 trades fermés; pas une preuve de PnL consolidé. CPU actuel 0 et RAM métrique courante 1,026 Go malgré cron terminé; vérifier facturation réelle du conteneur, ne pas conclure fuite. Proposer cache incrémental avec parité stricte, aucun changement LIVE.
- ROTATION et ALIGNEMENT : cronSucceeded et 0 CPU / 0 RAM sur 1h, malgré moyennes RAM 24h non nulles. QUATRE, PERSONAL snapshots, proxy shadow : 0 CPU/RAM 24h; aucune économie supplémentaire attribuée à leur suppression.
- HWR et Health/Guardian online. Aucun nouveau service identifié vs 20/11. Réseau observé sans preuve de trafic egress facturé anormal; analyse détaillée REPLAY requise.

## Billing et rentabilité
Recherche Gmail Railway postérieure au 7 novembre : **aucune nouvelle alerte d'usage**; dernier avis vérifié 10,04 USD au 07/11/2026, facture payée 71,91 USD le 03/11/2026 (source du contrôle antérieur). Cycle historiquement annoncé au 04/12; plafond HARD actuel et usage réel actuel inconnus : impossible de certifier ou d'exclure un arrêt sous 24–48h. Ne jamais modifier les limites automatiquement.
Claude Pro : reçu 32,19 CAD du 19/10 (historique vérifié). Les factures ChatGPT/n8n/TradingView et PnL net réel consolidé 30j ne sont pas disponibles dans ce contrôle : **aucun total de rentabilité projet**.

## Statut des actions
DÉTECTÉ : hausse relative Bande & Cycle, rafales de polling REPLAY, recalcul BRIQUES. PROPOSÉ : analyse cache/déduplication REPLAY, benchmark incrémental BRIQUES, profilage Bande & Cycle hors LIVE. TESTÉ : métriques, inventaire, états, logs et tarifs en lecture seule, pas de correctif logiciel. INSTALLÉ : aucun correctif FinOps. OBSERVÉ 24H APRÈS : sans objet.
Aucun bot LIVE, Health/Guardian, volume, protection, stratégie, ordre, risque, capital, limite de facturation ou nouveau service modifié.
