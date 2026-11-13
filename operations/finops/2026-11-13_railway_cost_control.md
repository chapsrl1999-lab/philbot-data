# Contrôle FinOps PhilBot — 13 novembre 2026 (≈08:53 EST)

## Périmètre et preuve
Railway list_projects/list_services/environment_status: zesty-learning 21 services, DP60 4, Recent40 1, R20 1 = **27**. Un nouvel auxiliaire `philbot-rotation-ombre` et `philbot-alignement-ombre` apparaissent depuis la photographie FinOps du 12/11 (25); les deux sont des jobs fictifs, non des moteurs LIVE. Aucun arrêt effectué. Le statut détaillé de zesty-learning a une limite de 10 services par appel; inventaire complet établi par list_services, mais pas toutes les lignes de statut détaillé obtenues. Les quatre projets répondent.

Tarifs officiels Railway consultés le 13/11 : CPU 0,00000772 USD/vCPU/s (~20 USD/vCPU-mois), RAM 0,00000386 USD/Go/s (~10 USD/Go-mois), egress service 0,05 USD/Go; unités facturées au prorata du temps. https://railway.com/pricing

Mesures Railway CPU_USAGE, MEMORY_USAGE_GB, NETWORK_RX_GB, NETWORK_TX_GB: **24h pour les 27 services**. Les métriques 1h/7j ont été obtenues pour HWR, QUATRE, ALIGNEMENT; 24h/7j pour SIGNER, R20, RECENT40, CASCADE, OUTSIDER, Replay; 24h et certains 1h pour ROTATION. Les requêtes 1h/7j de plusieurs services ont été limitées par Railway (rate limit), donc aucune affirmation de couverture complète 7j. Les moyennes réseau RX/TX sont des valeurs de métriques, **pas** des totaux d'egress facturés; pas de conversion en facture réseau sans intégration temporelle et séparation egress facturable.

## Projection CPU + RAM — moyenne 24h, USD/mois, charge constante
**≈79,19 USD/mois** pour 27 services (arrondis intermédiaires), contre 79,95 USD/mois au 12/11 sur 25 services. Écart ≈−0,76 USD/mois, mais inventaires et charges différents, aucune économie attribuable ni facture. Exclut egress, disque, volumes, Agent, abonnement, taxes, crédits.

| Service | CPU vCPU 24h | RAM Go 24h | Projection USD/mois |
|---|---:|---:|---:|
| HWR hybrid-r4-read-check | 0,12830 | 3,00678 | 32,63 |
| QUATRE ombre | 0,00470 | 0,98818 | 9,98 |
| SIGNER | 0,11185 | 0,30880 | 5,33 |
| R20 HL | 0,07260 | 0,26965 | 4,15 |
| CASCADE REAL (nom Railway shadow) | 0,01296 | 0,37606 | 4,02 |
| RECENT40 | 0,00391 | 0,32636 | 3,34 |
| OUTSIDER validation | 0,01330 | 0,29471 | 3,21 |
| Replay R7 | 0,00331 | 0,24835 | 2,55 |
| ALIGNEMENT ombre | 0,00036 | 0,22697 | 2,28 |
| Bande & Cycle | 0,00036 | 0,18917 | 1,90 |
| TRIPLE BloFin | 0,00080 | 0,17605 | 1,78 |
| R3 HL | 0,00061 | 0,14659 | 1,48 |
| Guardian | 0,00202 | 0,11308 | 1,17 |
| SWING | 0,00046 | 0,10475 | 1,06 |
| Health | 0,00255 | 0,07308 | 0,78 |
| PhilBot Suivi | 0,00413 | 0,06901 | 0,77 |
| Triple Relay | 0,00018 | 0,07362 | 0,74 |
| HWR market-data | 0,00026 | 0,06231 | 0,63 |
| Soldes relay | 0,00005 | 0,05117 | 0,51 |
| ROTATION ombre | 0,00022 | 0,03560 | 0,36 |
| PERSONAL readonly | 0,00018 | 0,01153 | 0,12 |
| DP60 readonly | 0,00036 | 0,01092 | 0,12 |
| RANGE readonly | 0,00015 | 0,01081 | 0,11 |
| OUTSIDER ledger | 0,00013 | 0,00904 | 0,09 |
| CASCADE readonly | 0,00018 | 0,00657 | 0,07 |
| SHADOW proxy | 0,00001 | 0,00165 | 0,02 |
| PERSONAL snapshots | 0 | 0 | 0 |

## Comparaisons et diagnostics
- HWR base avant 28/10 : 0,758 vCPU et 3,507 Go (50,23 USD/mois théoriques). Aujourd'hui 0,12830 / 3,00678 (32,63). Pas de preuve de gain causal/facturé; un échantillon 24h mixte avant/après ne démontre pas de gain post-déploiement. Service LIVE, volume /data; journaux montrent PREPARED_RUNTIME READY et ordersPossible=true à 13:46Z, puis NO_FRESH_BOUNDARY sur des minutes intermédiaires; aucun changement autorisé.
- QUATRE : cron `5 * * * *`, dernier succès 13:10Z, durée 56 s, compte fictif; 24h 9,98 USD/mois vs 7j 5,88 USD/mois (0,00563 vCPU / 0,57636 Go), comparaison 7j mélange anciens régimes. 24h inférieur aux 12,96 USD/mois du 12/11; baisse non attribuable à un correctif FinOps. CPU courant 0 après cron mais RAM métrique courante 0,986 Go; possible mémoire retenue ou mesure périmée, pas preuve de facturation en dehors du cron. Garder fréquence horaire, tester replay incrémental sur clone et comparer exactement les résultats.
- ALIGNEMENT : cron horaire, dernier succès 13:20Z, 6 s, 62 actifs, compte fictif. 1h CPU=0 RAM=0; 24h 2,28 USD/mois extrapolés, fenêtre de démarrage courte et non représentative du régime stable. Pas de désactivation.
- ROTATION : cron quotidien, dernier succès 00:22Z; 24h 0,36 USD/mois; log du 13/11 affiche un reset de la simulation à 1000 USD vs état précédent 860,72 USD, à réconcilier côté recherche, pas un coût matériel. Ne pas confondre PnL fictif avec PnL réel.
- SIGNER 24h 5,33 vs 7j 4,74 USD/mois (+12,4 %). CASCADE REAL 24h 4,02 vs 7j 2,87 (+40 %, ≈1,15 USD/mois), hausse relative >25 % mais faible montant; garder sous surveillance, ne pas couper. R20 24h 4,15 vs 7j 4,29; RECENT40 3,34 vs 3,44; OUTSIDER 3,21 vs 3,37; Replay 2,55 vs 2,47. Aucune preuve de hausse >10 USD/mois sur un service.
- PERSONAL snapshots CRASHED/cronFailed depuis 06/11, CPU=RAM=0 24h. SHADOW proxy quasi inactif. Aucun gain financier de calcul à revendiquer en les arrêtant. Zesty compte un build OUTSIDER validation FAILED le 12/11 20:47Z puis déploiement SUCCESS 20:52Z; Health/Guardian en ligne. DP60 reader a un patch staged non appliqué; aucun commit réalisé.
- Recommandations proposées et **non installées** : snapshot/cache incrémental QUATRE (clone et parité stricte 7 clôtures), mesure RAM au niveau durée de cron, cache/backoff Replay 429, examen de dépendances de tout auxiliaire avant suppression. Aucun changement métier.

## Factures / risque budget
Recherche Gmail Railway après 07/11 : dernier avis de consommation toujours 10,04 USD au 07/11 21:16Z; reçu Railway 71,91 USD payé 03/11 pour cycle précédent, distinct de l'usage actuel. Cycle annoncé fin 04/12, hard cap courant et usage réel courant inconnus; impossible de certifier risque d'arrêt 24–48h. Courriel du 13/11 : rapport de sécurité Railway et bulletin général de compensation pour usage de jetons non autorisé, **aucun crédit spécifique PhilBot établi**. Aucun plafond modifié.
Reçus antérieurs distincts : Claude Pro 32,19 CAD (19/10), Claude Max 142,75 CAD (01/11) avec crédit 15,84 CAD; pas de total consolidé ChatGPT/Claude/n8n/TradingView sans sources complètes. PnL réel 30j net et transferts non réconciliés : bénéfice net global non calculable.

## Statut de travail
- DÉTECTÉ : CASCADE +40% de consommation relative vs 7j (faible coût), QUATRE RAM métrique résiduelle après cron, nouveaux jobs ALIGNEMENT et ROTATION à coût limité, reset de simulation ROTATION à clarifier.
- PROPOSÉ : cache QUATRE, contrôle mémoire par durée d'exécution, revue dépendances et tests de non-régression, diagnostic reset ROTATION.
- TESTÉ : inventaires, 27 mesures 24h, échantillons 1h/7j, statuts, configurations/logs ciblés, tarifs, Gmail; aucun correctif de code FinOps testé.
- INSTALLÉ : aucun correctif FinOps.
- OBSERVÉ 24H APRÈS : sans objet.
- Aucune intervention sur LIVE, Health/Guardian, volumes, alertes, ordres, stops, stratégies, capital, limites budgétaires. Aucune économie réalisée revendiquée.

Suivi : https://github.com/chapsrl1999-lab/philbot-signer/issues/67
