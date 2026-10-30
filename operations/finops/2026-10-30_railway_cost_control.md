# PhilBot — contrôle FinOps du 30 octobre 2026 (vers 12:13–12:20 UTC / 08:13–08:20 Québec)

**État : DÉTECTÉ / OBSERVÉ 24 H POST-correctif HWR, aucune optimisation de code TESTÉE ou INSTALLÉE.** Contrôle lecture seule des projets Railway `zesty-learning`, `philbot-rafale2-dp60`, `philbot-recent40-observer`, `philbot-r20-shadow` : inventaire exhaustif de **36 services** (31 + 2 + 1 + 2), `get_service_metrics` sur 24 h et 168 h (CPU_USAGE, MEMORY_USAGE_GB, NETWORK_RX_GB, NETWORK_TX_GB), `describe_environment` et `environment_status` de chacun, `describe_service` ciblé et logs. Toutes les dernières versions de déploiement sont `SUCCESS` sauf **5 `SLEEPING`** dans zesty; SUCCESS n'implique ni ordre LIVE possible ni CPU actif. Aucun défaut Railway actif dans les résumés environment_status (fenêtre 24 h); l'API limite l'affichage des détails à 10 services par appel, l'inventaire des 36 est confirmé avec describe_environment. Un patch staged ancien et vide subsiste dans DP60; n'a pas été accepté.

## Résultat économique — mesures vs factures

Railway officiel : **20 USD/vCPU-mois, 10 USD/Go RAM-mois, sortie réseau 0,05 USD/Go, volume 0,15 USD/Go-mois**, selon https://docs.railway.com/pricing/plans consulté le 30 octobre. Le CPU et la RAM sont facturés au temps réellement consommé; les ressources d'un job terminé n'ont pas à être projetées comme une charge future. Hobby à 5 USD/mois **inclut** 5 USD de crédits d'usage, ne pas additionner deux fois.

**Somme des moyennes 24 h de CPU+RAM sur les 36 services, extrapolées à charge constante : 66.68 USD/mois**; fenêtre 7 jours extrapolée de même : **76.15 USD/mois**. Ces sommes sont des **équivalents théoriques** : PAS une consommation réelle du cycle, PAS une facture, PAS une économie acquise. Hors egress, volumes, agent, abonnement/crédit et autres ressources. Les colonnes RX/TX sont des **moyennes des échantillons NETWORK_RX_GB et NETWORK_TX_GB**, PAS des volumes GB totaux ou une facture réseau; les volumes agrégés ne peuvent pas être déduits simplement de ces moyennes.

**Budget réel non vérifiable aujourd'hui** : dernier e-mail Gmail Railway 28 octobre à 12:26 UTC : 55,08 USD usage déclaré et plafond **alors 55 USD**, arrêt global ; aucun e-mail billing plus frais retrouvé au 30 octobre. Dernier reset connu **4 novembre 2026** (courriel 23 octobre). La limite et la consommation actuelles ne sont **pas** accessibles par les méthodes Railway autorisées : aucun délai d'arrêt sur 24–48 h ne peut être calculé sans fabriquer un chiffre. Les services interrogés sont revenus online/healthy; cela ne prouve pas que le risque budgétaire est écarté. Ne pas augmenter de limite.

Vrais reçus distincts : Railway **28,40 USD acquittés** sur ancienne période 3 septembre–3 octobre (reçu 3 octobre); Claude Pro **32,19 CAD taxes comprises**, acquittés le 19 octobre. Aucune facture complète actuelle ChatGPT, n8n ou TradingView vérifiée, pas de PnL net réalisé+flottant consolidé, frais et dépôts/retraits neutralisés sur 30j. **Résultat NET du projet 30j : non calculable**, aucun jugement artificiel de rentabilité.

## Priorités et causalité

1. **HWR principal poste** (`hybrid-r4-read-check`, serviceId `79ebd36d-3960-4535-adf8-16f9e1265b94`): volume /data conservé, commit production **`28eea2b5f053eaca966f62656944fb3c39ba6a79`**, déployé le **28 octobre à 21:41 UTC**. Mesure 24 h recueillie le 30 octobre vers 12:13Z : **0,127212 vCPU / 2,871004 Go**, soit **31,25 USD/mois** *à charge constante CPU+RAM* ; 7 j : **0,314106 vCPU / 3,055872 Go**, soit **36,84 USD/mois** ; dernière heure : 0,117004 / 2,872319 Go. **Référence avant correctif 28 oct : 0,758 vCPU / 3,507 Go, soit 50,23 USD/mois**. Cette nouvelle 24h est **entièrement post-déploiement** (contrairement à la fenêtre mixte du 29), baisse descriptive environ **−83 % CPU / −18 % RAM, −18,98 USD/mois équivalent théorique** contre la référence; **ce n'est PAS une réduction de facture prouvée ni une comparaison contrôlée à charge de marché constante**. Logs 12:00Z : projection 11 113 enregistrements, évaluation 25 500 ms à une borne de 15 minutes; collector ~1/min, `MARKET_STREAM_SILENT` EPICUSDT et reprises multiples, `NO_FRESH_BOUNDARY`, brèves erreurs SAND/gap puis READY. Le cache 113 séries et les réabonnements sont des pistes, **aucune fuite mémoire causale prouvée**. À profiler sur clone, proposer backoff/journaux redondants **sans réduire vigilance, fraîcheur ni autorisations métier**, tester rollback et invariants avant toute opération sur LIVE. Issue #67; dépendance #62.
2. **R20-HL dédié** : 24h **0,071305 vCPU / 0,257747 Go**, soit **4,00 USD/mois** théorique contre 7 j **0,014181 vCPU / 0,049827 Go** (0,78 USD/mois). Relatif **CPU +403 % / RAM +417 %**, mais démarrage du déploiement **29 octobre à 15:01 UTC**, donc 7 j essentiellement inactifs, **pas une anomalie de fuite démontrée**, augmentation absolute seulement ~3,2 USD/mois théoriques. Code versionné `server.mjs` confirme un moteur monitor toutes 10s et vérification scan toutes 1s avec verrou d'exécution et seulement 2 tentatives à chaque frontière 15m ; source `monitor.mjs` met en cache les observations 30s. Logs proxy 12:06–12:18Z : deux /monitor par minute (un ~3,2s, un ~3–6ms), un /guardian par minute (rapide), retours 200. Garder protections; étudier les GET longs et les duplications **sur copie sans supprimer les lectures nécessaires**. Aucune modification des fréquences LIVE.
3. **Jobs finis et nouveau service** : `philbot-reversal-research`, `philbot-grid-range-v1` = **24h 0 CPU / 0 RAM / 0 réseau** et **61/61 points à zéro sur 1h**; vieux échantillons 7j de RAM sont du passé, pas une dépense continue. **Nouveau `philbot-audit-positions-telegram-20261029`** (déploiement 29 oct 22:06 UTC) : 24h/7j/1h CPU=RAM=réseau=0, sans volume, classé **job ponctuel probablement terminé**, vérifier dépendances et logs avant nettoyage; **aucune économie de compute possible à l'arrêter actuellement**.
4. **SHADOW Phoenix V1 + Dual** : sans volumes persistants, coût CPU+RAM 24h équivalent ~**1,43 USD/mois ensemble**, logs anciens Vault 404 fréquents (28 octobre), absence de logs frais ici n'atteste PAS restauration. Proposer backoff sûr du Vault sur clone et tests de sauvegarde/récupération avant toute modification. Issue #65.
5. **Autres postes** : signer ~4,03 USD/mois, OUTSIDER ~3,56, RECENT40 ~3,21, SNAPBACK V10 ~2,24, R20-shadow ~2,01. `hybrid-hwr-qualify-node22-20261010` tourne presque au repos ~0,87 USD/mois équivalent, sans preuve d'absence de lecteurs; qualifier la redondance avant suppression. Les 5 sleeping et les jobs 0 sont protégés de toute annonce d'économies fictives. Aucun pic soutenu de TX inhabituel justifiant un arrêt; Phoenix V1 TX 7j supérieur au 24h reflète des pics historiques, pas un egress facturé reconstitué.

## Métriques de TOUT l'inventaire (moyenne ponctuelle)

Railway `get_service_metrics`, production. Sur chaque ligne **CPU vCPU / RAM Go** et **RX Go / TX Go** pour 24h et 168h; les colonnes réseaux ne sont PAS sommables en facture egress. `zesty` = zesty-learning; `dp60` = philbot-rafale2-dp60; `recent40` = philbot-recent40-observer; `r20` = philbot-r20-shadow. Les valeurs non nulles infinitésimales restent distinctes de zéro exact. 1441 échantillons 24h et 10081 sur 7j par mesure.

| Projet | Service | CPU/RAM 24h | CPU/RAM 7j | RX/TX 24h (GB) | RX/TX 7j (GB) | USD/mois théorique 24h CPU+RAM |
|---|---|---|---|---|---|---:|
| zesty | philbot-audit-positions-telegram-20261029 | 0 / 0 | 0 / 0 | 0 / 0 | 0 / 0 | 0.00 |
| zesty | philbot-r20-hl [sonde ancienne] | 0 / 0 | 0 / 0 | 0 / 0 | 0 / 0 | 0.00 |
| zesty | philbot-trains-bitunix | 0.0000260 / 0.0847 | 0.0000190 / 0.0448 | 5.38e-7 / 0.00000163 | 2.69e-7 / 2.70e-7 | 0.85 |
| zesty | philbot-range-wave-readonly | 0.000336 / 0.0121 | 0.000237 / 0.0183 | 0.0000241 / 0.00000488 | 0.0000134 / 0.00000378 | 0.13 |
| zesty | philbot-personal-snapshots | 0.00000353 / 0.0024 | 0.00000418 / 0.0098 | 8.94e-9 / 1.69e-9 | 6.31e-9 / 2.78e-9 | 0.02 |
| zesty | philbot-personal-readonly | 0.000217 / 0.0155 | 0.000245 / 0.0196 | 0.00000377 / 0.00000227 | 0.00000323 / 0.00000190 | 0.16 |
| zesty | philbot-outsider-hl-validation | 0.0132 / 0.3294 | 0.0113 / 0.3218 | 0.000290 / 0.000118 | 0.000286 / 0.000111 | 3.56 |
| zesty | hybrid-hwr-qualify-node22-20261010 | 0.000302 / 0.0862 | 0.0046 / 0.0812 | 0.0000338 / 0.00000656 | 0.000809 / 0.0000957 | 0.87 |
| zesty | philbot-replay-r16-smoke | 0 / 0 | 7.05e-7 / 0.0147 | 0 / 0 | 7.84e-9 / 9.36e-10 | 0.00 |
| zesty | hybrid-r4-read-check | 0.1272 / 2.8710 | 0.3141 / 3.0559 | 0.0019 / 0.000410 | 0.0012 / 0.000277 | 31.25 |
| zesty | philbot-grid-range-v1 | 0 / 0 | 0.00000524 / 0.1354 | 0 / 0 | 0.00000673 / 1.65e-7 | 0.00 |
| zesty | philbot-control-shadow-read-proxy | 0.000142 / 0.0202 | 0.000103 / 0.0341 | 0.00000277 / 0.00000122 | 0.00000573 / 0.00000465 | 0.20 |
| zesty | philbot-bitunix-phoenix-shadow-v1 | 0.0033 / 0.0635 | 0.0101 / 0.0912 | 0.000525 / 0.000184 | 0.000608 / 0.0038 | 0.70 |
| zesty | philbot-bitunix-phoenix-dual-shadow | 0.0031 / 0.0666 | 0.0041 / 0.0939 | 0.000518 / 0.0000445 | 0.000506 / 0.0000443 | 0.73 |
| zesty | philbot-r20-shadow-probe | 0.000146 / 0.0198 | 0.000151 / 0.0193 | 0.0000256 / 0.00000425 | 0.0000254 / 0.00000422 | 0.20 |
| zesty | philbot-range-rejection-forward-lab | 0 / 0 | 1.08e-7 / 0.000214 | 0 / 0 | 0 / 0 | 0.00 |
| zesty | philbot-r1-oos-proxy | 0 / 0 | 2.58e-7 / 0.0053 | 0 / 0 | 5.34e-11 / 6.61e-11 | 0.00 |
| zesty | philbot-replay-r7-native | 0.0016 / 0.1355 | 0.0034 / 0.2286 | 0.0000714 / 0.000289 | 0.0000709 / 0.000261 | 1.39 |
| zesty | philbot-rafale2-swing-shadow | 0.000579 / 0.0629 | 0.0036 / 0.0638 | 0.000159 / 0.0000440 | 0.0036 / 0.0000770 | 0.64 |
| zesty | philbot-guardian | 0.0027 / 0.0979 | 0.0023 / 0.0846 | 0.0000406 / 0.0000157 | 0.0000358 / 0.0000141 | 1.03 |
| zesty | philbot-snapback-v10r1 | 0.0057 / 0.2126 | 0.0057 / 0.2050 | 0.0000135 / 0.0000114 | 0.0000136 / 0.0000114 | 2.24 |
| zesty | philbot-reversal-research | 0 / 0 | 0.0000650 / 0.4323 | 0 / 0 | 0.0000284 / 6.56e-7 | 0.00 |
| zesty | philbot-health | 0.0040 / 0.1242 | 0.0041 / 0.0942 | 0.000399 / 0.0000565 | 0.000467 / 0.0000533 | 1.32 |
| zesty | philbot-rafale2-hl | 0.000383 / 0.1046 | 0.000403 / 0.1079 | 0.0000310 / 0.0000575 | 0.0000331 / 0.0000572 | 1.05 |
| zesty | philbot-rafale2-blofin | 0.0036 / 0.1779 | 0.0031 / 0.1549 | 0.000423 / 0.0000525 | 0.000357 / 0.0000356 | 1.85 |
| zesty | venue-research-rafale2 | 0 / 0 | 0 / 0 | 0 / 0 | 0 / 0 | 0.00 |
| zesty | philbot-rafale2-bitunix | 0.000541 / 0.1024 | 0.000579 / 0.0959 | 0.0000131 / 0.0000425 | 0.0000139 / 0.0000415 | 1.04 |
| zesty | philbot-snapback | 0.000882 / 0.1399 | 0.000648 / 0.1617 | 0.00000560 / 0.00000563 | 0.00000665 / 0.00000565 | 1.42 |
| zesty | philbot-vortex | 0 / 0 | 0.00000143 / 0.0545 | 0 / 0 | 1.56e-10 / 8.00e-11 | 0.00 |
| zesty | faithful-passion | 0.00000350 / 0.0507 | 0.00000412 / 0.0310 | 1.40e-9 / 3.04e-9 | 1.38e-9 / 3.04e-9 | 0.51 |
| zesty | philbot-signer | 0.0755 / 0.2517 | 0.0988 / 0.2391 | 0.0000382 / 0.0000417 | 0.0000282 / 0.0000350 | 4.03 |
| dp60 | philbot-dp60-readonly | 0.000144 / 0.0385 | 0.000116 / 0.0339 | 0.00000137 / 0.00000153 | 9.61e-7 / 7.86e-7 | 0.39 |
| dp60 | rafale2-blofin-dp60 | 0.0059 / 0.1757 | 0.0108 / 0.1592 | 0.0000824 / 0.0000437 | 0.000413 / 0.000111 | 1.87 |
| recent40 | recent40-observer | 0.0117 / 0.2979 | 0.0076 / 0.2248 | 0.000403 / 0.000112 | 0.000369 / 0.000106 | 3.21 |
| r20 | philbot-r20-hl [compte dédié] | 0.0713 / 0.2577 | 0.0142 / 0.0498 | 0.000133 / 0.0000552 | 0.0000284 / 0.00000904 | 4.00 |
| r20 | r20-shadow | 0.0148 / 0.1714 | 0.0161 / 0.2146 | 0.000343 / 0.0000744 | 0.000307 / 0.0000818 | 2.01 |

## Historique des mesures, protections et audit de modification

**DÉTECTÉ** : coût continu HWR encore majeur; R20 en hausse relative de charge due à période de comparaison hétérogène; quelques proxys et qualifications dont l'intérêt doit être établi; risque de plafond courant non mesurable; historique Vault 404 SHADOW. **PROPOSÉ** : instrumentation sur clone, audit dépendances et profilers HWR/R20, correction réversible du bruit et des 404 en SHADOW après sauvegarde prouvée; revue strictement économique du prix de chaque ressource. **TESTÉ** : métriques Railway/états/logs/relecture code seuls; aucune suite d'intégration ou benchmark de correctif exécuté. **INSTALLÉ** : **aucun correctif technique**, aucune ressource, ordre, trade, stratégie, levier, sizing, risque, stop, capital, protection, Health/Guardian, volume ou limite budgétaire modifiés. **OBSERVÉ 24H APRÈS** : fenêtre complète POST correctif HWR observée, sans attribuer la différence au correctif de façon causale. Toute action susceptible d'altérer LIVE requiert sauvegarde/restauration, tests, rollback et accord si impact métier.

**Références** : Railway get_service_metrics 24/168/1h, describe_environment/service, environment_status, get_logs ; Gmail e-mails `1a18279cdac87c27` (28 oct), `1a16989c06f0de33` (reset 4 nov), reçu Railway `1a1049f13222ea5e`, reçu Claude `1a15439482a96ad7` ; prix https://docs.railway.com/pricing/plans ; GitHub https://github.com/chapsrl1999-lab/philbot-signer/issues/67 ; source opérationnelle https://github.com/chapsrl1999-lab/philbot-data/blob/main/operations/PHILBOT_OPERATING_STATE_V1.md.
