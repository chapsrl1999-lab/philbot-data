# Contrôle FinOps PhilBot — 19 novembre 2026 (08:10–08:30 EST)

## Périmètre et preuves
- Inventaire Railway vérifié : 28 services, zesty-learning 22, philbot-rafale2-dp60 4, philbot-recent40-observer 1, philbot-r20-shadow 1. Mesures CPU_USAGE, MEMORY_USAGE_GB, NETWORK_RX_GB et NETWORK_TX_GB obtenues sur 24h et 168h pour les 28 services; métriques 1h ciblées pour HWR, BRIQUES, QUATRE, PERSONAL snapshots et proxy shadow. Les valeurs réseau sont des moyennes d'échantillons de mesure, **pas** des volumes totaux de transfert ni une facture egress.
- Tarifs Railway officiels confirmés le 19/11 : CPU 20 USD/vCPU-mois, RAM 10 USD/Go-mois, egress 0,05 USD/Go, stockage volume 0,15 USD/Go-mois, calcul facturé au prorata du temps. Source https://docs.railway.com/pricing .
- Projection théorique **85,36 USD/mois** CPU+RAM (somme des moyennes 24h × tarifs, hypothèse charge constante). Comparaison 18/11 : 83,86 USD/mois, soit +1,50 USD/mois (+1,8 %). Ni dépense constatée ni facture. Exclut egress, volumes, Agent, crédits, taxes, autres projets et fournisseurs. Les cron terminés peuvent rendre la projection fondée sur moyenne brute peu représentative de la facturation réelle : confirmer par usage Railway avant de parler d'économie.

## Principaux postes 24h (CPU vCPU, RAM Go, projection USD/mois)
| Service | CPU | RAM | Projection |
|---|---:|---:|---:|
| hybrid-r4-read-check HWR | 0,13136 | 3,01330 | 32,76 |
| philbot-briques-ombre (cron, **exécuteur réel**) | 0,02597 | 0,92713 | 9,79 |
| philbot-replay-r7-native | 0,00155 | 0,55966 | 5,63 |
| philbot-signer | 0,12136 | 0,30869 | 5,51 |
| philbot-r20-hl | 0,07652 | 0,29359 | 4,47 |
| philbot-cascade-shadow (**REAL/LIVE**) | 0,01228 | 0,40268 | 4,27 |
| philbot-outsider-hl-validation | 0,01303 | 0,32153 | 3,48 |
| philbot-alignement-ombre (cron) | 0,00013 | 0,30560 | 3,06 |
| recent40-observer | 0,00377 | 0,28766 | 2,95 |
| philbot-rafale2-blofin | 0,00008 | 0,20438 | 2,05 |

HWR 7j : 0,14459 vCPU et 2,99991 Go, projection 32,89 USD/mois; 24h 32,76. Référence **avant 28 octobre** : 0,758 vCPU et 3,507 Go, projection théorique 50,23 USD/mois. Mesures inférieures, sans attribution causale ni économie facturée démontrée; une fenêtre 24h mixte avant/après déploiement ne constitue pas une preuve de gain.

BRIQUES 7j : 0,02496 vCPU, 0,89125 Go (projection 9,41 USD/mois); 24h 9,79 (+4 %). Cron horaire SUCCESS, dernier passage 19/11 12:15Z, 146–151 secondes; journaux : 1 936 trades historiques rejoués, lecture de 10 cryptos, 7 positions réelles, équité ~285,94 USD. CPU instantané 0 mais RAM instantanée 0,956 Go après exécution : **ne pas** conclure que cette mémoire est facturée après fin du cron sans contrôle d'usage Railway. Proposer cache/reprise incrémentale isolée, tests de parité intégrale et rollback, sans changer fréquence ni opérations.

REPLAY : 24h 5,63 vs 7j 4,93 USD/mois (+14,2 %). Journaux récents contiennent encore de multiples PUBLIC_HTTP_429 et quelques PUBLIC_HTTP_400. Cause probable : appels publics répétitifs, backoff/cache insuffisant; proposition réversible : jitter, backoff et cache sur clone, validation de parité et du nombre de requêtes. **Non testé ni installé**.

SIGNER : 24h 5,51 vs 7j 5,39 USD/mois; R20 4,47 vs 7j 4,16; CASCADE 4,27 vs 7j 4,27. Pas de hausse matérielle confirmée. Aucun nouveau service depuis l'inventaire du 18/11. Aucune anomalie de réseau facturable démontrée par les moyennes RX/TX; pas de coût egress calculable sans volume sortant cumulé.

QUATRE, PERSONAL snapshots et proxy shadow : CPU et RAM nuls sur 1h et 24h; QUATRE cron configuré pour une date annuelle lointaine, PERSONAL snapshots cronFailed depuis 6/11, proxy sleeping. **Aucune économie additionnelle à attribuer à leur arrêt**. QUATRE 7j encore non nul car la fenêtre contient l'activité historique. ALIGNEMENT et ROTATION sont des crons réussis, non des processus continus; BRIQUES est un cron réel, à protéger. Ne pas désactiver des services sans vérifier leurs dépendances.

Statuts Railway : Health/Guardian/HWR/CASCADE/R20/RECENT40 et Triple online; BRIQUES/ALIGNEMENT/ROTATION cronSucceeded; PERSONAL snapshots cronFailed; QUATRE cronReady; patch DP60 reader toujours staged, patch R20 staged sans changements; aucun déploiement ou patch appliqué par FinOps. Le statut online ne prouve pas la conformité métier ou des stops.

## Factures, budget et rentabilité
- Recherche Gmail Railway après 07/11 : **aucun nouvel avis de consommation ou hard limit**. Dernier avis 07/11 21:16Z : 10,04 USD utilisés; dernière facture vérifiée 03/11 : 71,91 USD payés; cycle annoncé se terminant le 04/12. Plafond HARD actuel inconnu. L'arrêt sous 24–48h n'est ni confirmé ni exclu par ces sources; pas de modification automatique du plafond.
- Claude Pro 32,19 CAD taxes incluses le 19/10 est une référence de reçu historique; aucune facture globale ChatGPT/Claude/n8n/TradingView déduite. PnL nets réalisés + flottants 30j, transferts et frais fournisseurs non consolidés : revenu net global PhilBot non calculable.

## Actions
- **DÉTECTÉ** : HWR principal coût; BRIQUES exécuteur réel avec relecture historique; 429 REPLAY persistants; PERSONAL snapshots en échec mais sans CPU/RAM sur 24h.
- **PROPOSÉ** : cache/reprise incrémentale BRIQUES sur clone avec parité, backoff+jitter REPLAY sur clone, vérification métriques facturées des crons; ne pas toucher aux services LIVE ni aux protections.
- **TESTÉ** : lectures Railway, statuts, métriques, journaux, Gmail et tarifs officiels. Aucun correctif de code FinOps testé.
- **INSTALLÉ** : aucun correctif FinOps.
- **OBSERVÉ 24h après** : sans objet.

Issue de suivi : https://github.com/chapsrl1999-lab/philbot-signer/issues/67 . Aucun ordre, sizing, stop, capital, stratégie, volume, protection, alerte ou plafond modifié.
