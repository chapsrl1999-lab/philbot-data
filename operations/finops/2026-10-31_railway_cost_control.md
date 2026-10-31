# PhilBot — contrôle FinOps du 31 octobre 2026 (2026-10-31T12:33:04.623Z)
**État : DÉTECTÉ, DIAGNOSTIC PARTIEL. Aucune optimisation technique TESTÉE ou INSTALLÉE pendant ce contrôle.** Audit lecture seule Railway 4 projets, 36 services (31 zesty-learning, 2 philbot-rafale2-dp60, 1 philbot-recent40-observer, 2 philbot-r20-shadow), \get_service_metrics\ pour **24h et 168h** (1441/10081 échantillons par mesure), \describe_environment\ et \environment_status\ de chaque projet, \describe_service\ pour les postes majeurs, journaux; 1h de CPU/RAM/réseau des jobs de recherche. Métrologie d'infrastructure ≠ readiness métier; état opérationnel consulté au début de passe, notamment incident #75 RAFALE2-HL concurrent, donc **aucune action sur ce service**.

## Alerte financière fraîche : limite Railway désormais 80 USD
Gmail **30 oct 2026, 16:12:07 UTC** courriel authentifié Railway Support «Resource Usage Alert», id `1a18d953fea0ab31`: usage du cycle **60,08 USD**, plafond déclaré **80,00 USD**, soit **75,1 %**, solde **19,92 USD**, réinitialisation déclarée **4 novembre 2026**. C'est une **alerte de consommation**, PAS une facture réglée; mesure courriel datée et non un compteur temps réel. Le 28 oct 12:26:22Z, un ancien seuil 55 USD avait été atteint avec 55,08 USD de consommation et les déploiements arrêtés (id `1a18279cdac87c27`); ce seuil est désormais obsolète. Entre les deux messages, +5,00 USD sur environ 51h46, soit ~**2,32 USD/jour** historiques mêlant arrêt/redémarrage et agents éventuels; **ne pas l'extrapoler comme prévision fiable**. Pour atteindre 80 USD en 48h à partir du montant déclaré 30 oct, il faudrait ~9,96 USD/jour; risque d'arrêt sous 24–48h **non prouvable sans usage temps réel, coût agent et changement de charge**, et n'est pas à écarter. Vérifier le tableau Railway à la source avant de conclure. **Aucune hausse automatique de plafond.**

Tarifs Railway officiels vérifiés 31 octobre: **CPU 20 USD/vCPU-mois, RAM 10 USD/Go-mois, egress 0,05 USD/Go, stockage volume 0,15 USD/Go-mois**; calcul au prorata de consommation et du temps, modèle des conteneurs, lien https://docs.railway.com/pricing/plans . Les VMs/agents ont des prix différents et ne sont PAS inclus dans ces estimations.

**Projections CPU+RAM à charge moyenne constante**: toutes ressources sondées **67.01 USD/mois** (moyennes 24h), **78.10 USD/mois** (moyennes 7j). Veille: 66,68 / 76,15; variation globale +0.33 USD/mois théorique, **pas une hausse facturée prouvée**. Ces projections ne sont ni usage mensuel constaté, ni facture, ni économie: excluent réseau egress total, volumes, VM/agents, abonnements/crédits, taxes et autres projets non inclus. `NETWORK_RX_GB`/`NETWORK_TX_GB` ci-dessous = **moyennes d'échantillons de télémétrie**, pas sommes de Go transférés; impossible d'en déduire la facture d'egress ici.

## Causes et priorités (aucune mutation)
1. **HWR** `hybrid-r4-read-check` (ID `79ebd36d-3960-4535-adf8-16f9e1265b94`), **0,120204 vCPU / 2,887116 Go** sur 24h → **31.28 USD/mois** équivalent, soit **46,7 %** des projections totales. 7j 0,274441 / 3,007531 → **35.56 USD/mois**. Avant correctif 28 oct: **0,758 vCPU / 3,507 Go, soit 50,23 USD/mois**; fenêtre actuelle du 31 oct 24h est intégralement postérieure au déploiement SHA `28eea2b5f053eaca966f62656944fb3c39ba6a79` du 28 oct 21:39Z, contrairement au 29 oct mixte. Baisse **DESCRIPTIVE** CPU ~84,1 %, RAM ~17,7 % contre référence; **pas de causalité démontrée, ni de facture économisée**. Logs frais 31 oct 11:39–12:27Z sur 181 entrées : ~53 `MARKET_STREAM_SILENT`, ~44 `NO_FRESH_BOUNDARY`, ~12 `CURRENT_HISTORY_GAP`, collector ~46, EPICUSDT en reconnexion répétée. `ordersPossible=true` souvent mais quelques faux; **cache/boucles/reconnexions seulement hypothèses**, pas preuve de panne ou coût causal. Profilage sur clone sans altérer cadence ni protection LIVE; benchmark comparable et rollback avec état /data avant changement.
2. **R20-HL dédié** `r20/philbot-r20-hl`: **4,08 USD/mois** théoriques 24h vs **1,37 USD/mois** 7j (+198 % relatifs), **redémarrage effectif 29 oct 15:00Z**; comparaison 7j mêlée d'inactivité, pas une fuite prouvée ni un service inutile. Volume /data à préserver et protections sans modification. Ancienne sonde `zesty/philbot-r20-hl` est exactement à zéro CPU/RAM 24h/7j: ne représente aucune économie future immédiate.
3. **RECENT40** `recent40-observer`: 24h **0,007038 vCPU / 0,345835 Go**, **3,60 USD/mois** théoriques; 7j **0,006877 / 0,237205**, **2,51 USD/mois**, +43,4 % relatif (principalement RAM), et 1h **0,005106 / 0,362924**; 30 oct RAM 24h 0,2979. Redéploiement 29 oct 15:54Z, le 7j contient arrêt budget du 28. **Hausse >25 % détectée dans une comparaison à charges non homogènes**, aucune boucle ou fuite mémoire démontrée; proposer inspection allocations/cache/historiques du flux 63 actifs sur clone, vérifier stabilité 24h/48h; pas modifier service critique.
4. **TRAINS** 24h ~0,94 USD/mois vs 7j ~0,58 (+61 %) après déploiement 29 oct, sans signal de consommation anormale; protéger moteur SHADOW. `hybrid-hwr-qualify-node22-20261010` consomme réellement **0,85 USD/mois** en RAM, 1h 0,000243 vCPU / 0,085178 Go alors que derniers logs 28 oct s'arrêtent sur `HYBRID_MARKET_QUALIFY_RESULT PASSED`; **vérification de dépendances et démonstration de l'absence de consommateurs requises** avant éventuel arrêt, ne pas prétendre économies déjà obtenues.
5. **Recherche terminée** : `philbot-reversal-research`, `philbot-grid-range-v1`, `philbot-audit-positions-telegram-20261029`, `philbot-replay-r16-smoke`, `philbot-range-rejection-forward-lab`, `venue-research-rafale2` = **0 CPU, 0 RAM, 0 réseau, min/max 0 sur 60–61 échantillons de la dernière heure** et moyenne 24h zéro. Leur RAM parfois positive sur 7j correspond à une activité PASSÉE (jusqu'à 0,655 Go pour reversal); **aucune économie CPU/RAM présente en les arrêtant**. `personal-snapshots` est CRON et ne doit pas être considéré job terminé sur seule moyenne zéro.
6. **Phoenix SHADOW V1/dual** 24h ~1,44 USD/mois ensemble CPU+RAM, pas de volumes; logs V1 historiques du 28 oct montrent 25 sauvegardes Vault HTTP 404, sans journaux postérieurs dans cette vue. L'absence de logs frais n'est **pas** la preuve de guérison; backup/restauration et dépendances à vérifier avant toute retouche. Backoff fail-closed possible sur clone seulement, issue #65; priorité de fiabilité, pas économie massive. Egress actuel moyen TX Phoenix V1 bien plus bas que sur 7j, pas de pic de débit durable prouvé.
7. **Autres coûts structurants** `philbot-signer` 4,28, OUTSIDER 3,55, SNAPBACK V10 2,36, R20-shadow 2,05 USD/mois théoriques. Toute réduction des services liés aux ordres, signaux, stops, guardian, health, volumes, alertes/Trade est **interdite sans rollback testé et accord explicite si impact métier**.

## Inventaire exhaustif — get_service_metrics
Unités: chaque case CPU/RAM = moyennes vCPU / Go sur fenêtre; RX/TX = **moyennes métriques réseau en GB** (ni débit cumulé ni facture). Dernière colonne coût CPU+RAM *projeté si moyenne 24h se répétait tout le mois*. État SUCCESS/SLEEPING = état Railway du déploiement, **PAS santé métier ni preuve de charge facturée**. Les observations horaires ne sont pas automatiquement extrapolables quand job terminé.

| Projet | Service | Déploiement | CPU/RAM 24h | CPU/RAM 7j | RX/TX 24h | RX/TX 7j | USD/mois théor. 24h |
|---|---|---|---|---|---|---|---:|
| zesty | philbot-r20-shadow-probe | SUCCESS | 0.00014 / 0.01797 | 0.00015 / 0.01914 | 2.55e-5 / 4.26e-6 | 2.54e-5 / 4.23e-6 | 0.18 |
| zesty | philbot-grid-range-v1 | SUCCESS | 0 / 0 | 5.24e-6 / 0.20518 | 0 / 0 | 6.73e-6 / 1.65e-7 | 0.00 |
| zesty | philbot-bitunix-phoenix-shadow-v1 | SUCCESS | 0.00345 / 0.06314 | 0.00874 / 0.08619 | 0.00053 / 0.00027 | 0.00059 / 0.00311 | 0.70 |
| zesty | philbot-personal-readonly | SUCCESS | 0.00021 / 0.01326 | 0.00022 / 0.01714 | 4.09e-6 / 2.42e-6 | 3.40e-6 / 2.04e-6 | 0.14 |
| zesty | philbot-bitunix-phoenix-dual-shadow | SUCCESS | 0.00312 / 0.06750 | 0.00385 / 0.08771 | 0.00052 / 4.51e-5 | 0.00051 / 4.43e-5 | 0.74 |
| zesty | philbot-replay-r16-smoke | SLEEPING | 0 / 0 | 7.05e-7 / 0.02224 | 0 / 0 | 7.84e-9 / 9.36e-10 | 0.00 |
| zesty | philbot-vortex | SLEEPING | 0 / 0 | 7.52e-7 / 0.00923 | 0 / 0 | 5.33e-11 / 5.57e-11 | 0.00 |
| zesty | philbot-reversal-research | SUCCESS | 0 / 0 | 6.50e-5 / 0.65490 | 0 / 0 | 2.84e-5 / 6.56e-7 | 0.00 |
| zesty | philbot-rafale2-blofin | SUCCESS | 0.00369 / 0.17063 | 0.00358 / 0.16605 | 0.00044 / 5.52e-5 | 0.00042 / 4.29e-5 | 1.78 |
| zesty | philbot-range-wave-readonly | SUCCESS | 0.00034 / 0.01377 | 0.00028 / 0.01989 | 2.69e-5 / 5.04e-6 | 1.73e-5 / 4.49e-6 | 0.14 |
| zesty | philbot-rafale2-swing-shadow | SUCCESS | 0.00061 / 0.06493 | 0.00302 / 0.06362 | 0.00025 / 4.95e-5 | 0.00292 / 7.23e-5 | 0.66 |
| zesty | philbot-control-shadow-read-proxy | SLEEPING | 0.00019 / 0.02008 | 0.00012 / 0.03199 | 8.44e-6 / 2.43e-6 | 6.53e-6 / 4.61e-6 | 0.20 |
| zesty | faithful-passion | SUCCESS | 3.01e-6 / 0.03877 | 3.97e-6 / 0.03351 | 1.40e-9 / 3.04e-9 | 1.38e-9 / 3.04e-9 | 0.39 |
| zesty | philbot-range-rejection-forward-lab | SLEEPING | 0 / 0 | 1.08e-7 / 0.00032 | 0 / 0 | 0 / 0 | 0.00 |
| zesty | philbot-replay-r7-native | SUCCESS | 0.00177 / 0.13337 | 0.00339 / 0.21166 | 8.48e-5 / 0.00033 | 7.61e-5 / 0.00028 | 1.37 |
| zesty | venue-research-rafale2 | SUCCESS | 0 / 0 | 0 / 0 | 0 / 0 | 0 / 0 | 0.00 |
| zesty | philbot-snapback-v10r1 | SUCCESS | 0.00559 / 0.22451 | 0.00570 / 0.20805 | 1.34e-5 / 1.14e-5 | 1.35e-5 / 1.14e-5 | 2.36 |
| zesty | philbot-outsider-hl-validation | SUCCESS | 0.01115 / 0.33261 | 0.01160 / 0.32442 | 0.00031 / 0.00012 | 0.00030 / 0.00011 | 3.55 |
| zesty | philbot-rafale2-hl | SUCCESS | 0.00038 / 0.11785 | 0.00040 / 0.10897 | 6.10e-5 / 5.43e-5 | 3.77e-5 / 5.70e-5 | 1.19 |
| zesty | philbot-r1-oos-proxy | SLEEPING | 0 / 0 | 2.58e-7 / 0.00803 | 0 / 0 | 5.34e-11 / 6.61e-11 | 0.00 |
| zesty | philbot-audit-positions-telegram-20261029 | SUCCESS | 0 / 0 | 0 / 0 | 0 / 0 | 0 / 0 | 0.00 |
| zesty | philbot-trains-bitunix | SUCCESS | 4.00e-5 / 0.09381 | 2.48e-5 / 0.05823 | 1.04e-6 / 6.61e-6 | 4.19e-7 / 1.22e-6 | 0.94 |
| zesty | hybrid-r4-read-check | SUCCESS | 0.12020 / 2.88712 | 0.27444 / 3.00753 | 0.00121 / 0.00029 | 0.00117 / 0.00028 | 31.28 |
| zesty | philbot-guardian | SUCCESS | 0.00268 / 0.09224 | 0.00239 / 0.08554 | 4.18e-5 / 1.93e-5 | 3.67e-5 / 1.51e-5 | 0.98 |
| zesty | philbot-snapback | SUCCESS | 0.00088 / 0.14114 | 0.00069 / 0.15788 | 5.80e-6 / 5.51e-6 | 6.61e-6 / 5.63e-6 | 1.43 |
| zesty | philbot-rafale2-bitunix | SUCCESS | 0.00045 / 0.10712 | 0.00054 / 0.09610 | 1.16e-5 / 5.35e-5 | 1.29e-5 / 4.33e-5 | 1.08 |
| zesty | philbot-personal-snapshots | SUCCESS | 0 / 0 | 4.11e-6 / 0.00924 | 2.93e-9 / 0 | 6.42e-9 / 2.64e-9 | 0.00 |
| zesty | philbot-r20-hl | SUCCESS | 0 / 0 | 0 / 0 | 0 / 0 | 0 / 0 | 0.00 |
| zesty | philbot-health | SUCCESS | 0.00394 / 0.07952 | 0.00403 / 0.09387 | 0.00042 / 5.45e-5 | 0.00046 / 5.37e-5 | 0.87 |
| zesty | philbot-signer | SUCCESS | 0.08568 / 0.25662 | 0.09643 / 0.24251 | 3.97e-5 / 5.02e-5 | 2.96e-5 / 3.75e-5 | 4.28 |
| zesty | hybrid-hwr-qualify-node22-20261010 | SUCCESS | 0.00027 / 0.08511 | 0.00464 / 0.08396 | 3.37e-5 / 6.58e-6 | 0.00081 / 9.57e-5 | 0.86 |
| dp60 | rafale2-blofin-dp60 | SUCCESS | 0.00555 / 0.16735 | 0.01008 / 0.16080 | 7.89e-5 / 4.32e-5 | 0.00038 / 0.00010 | 1.78 |
| dp60 | philbot-dp60-readonly | SUCCESS | 0.00015 / 0.03811 | 0.00014 / 0.03942 | 1.43e-6 / 1.59e-6 | 1.17e-6 / 1.01e-6 | 0.38 |
| recent40 | recent40-observer | SUCCESS | 0.00704 / 0.34584 | 0.00688 / 0.23720 | 0.00024 / 7.40e-5 | 0.00036 / 0.00010 | 3.60 |
| r20 | philbot-r20-hl | SUCCESS | 0.07132 / 0.26570 | 0.02449 / 0.08794 | 0.00014 / 5.97e-5 | 4.92e-5 / 1.76e-5 | 4.08 |
| r20 | r20-shadow | SUCCESS | 0.01690 / 0.17123 | 0.01630 / 0.20661 | 0.00036 / 7.46e-5 | 0.00032 / 8.08e-5 | 2.05 |

## Factures réelles et économie nette 30 jours
**Preuves Gmail** : Railway reçu **28,40 USD payé 03/04 octobre** (période ancienne sept–oct, id `1a1049f13222ea5e`), Claude Pro **32,19 CAD taxes incluses payé 19 octobre** (id `1a15439482a96ad7`), à ne jamais additionner entre devises ou assimilier à un mois complet. TradingView e-mail **15 oct «Upcoming subscription payment»** seulement, ne prouve aucun paiement; pas de reçu/facture complet 30j n8n, OpenAI/ChatGPT ou TradingView trouvé via recherche ciblée Gmail. Le budget Railway est une **consommation déclarée**, pas un reçu. PnL net réalisé+flottant par comptes réels et transferts/dépôts/retraits neutralisés **non consolidés**, donc **profit NET 30j après abonnements non calculable**; ne pas fabriquer de rentabilité, ne pas double compter les frais de marché ou conversions forex.

## Statuts et suite autorisée
**DÉTECTÉ** : 80 USD limite désormais, 60,08 USD usage historique; HWR principal coût, RECENT40 hausse mémoire relative >25 % vs fenêtre 7j hétérogène; qualification HWR toujours consommatrice 0,85 USD/mois, Phoenix archives 404. **PROPOSÉ** : profilage RECENT40/HWR sans risque sur clone, audit de dépendances qualification HWR + backup Phoenix, revue budget rapprochée; aucune coupure LIVE ni des protections.
**TESTÉ** : API Railway mesures 24h/7j et 1h ciblée, configs/états, journaux, lecture facture Gmail et tarifs officiels. Aucun test unitaire de patch ni bench de changement.
**INSTALLÉ** : uniquement document et issue FinOps; **AUCUN code/déploiement/ressource/stratégie/sizing/stop/protection/capital/limite budgétaire modifié.**
**OBSERVÉ 24h APRÈS** : HWR 24h sur version post-28 oct, résultat descriptif seulement; aucun correctif nouveau de cette passe à réévaluer.
Références: https://github.com/chapsrl1999-lab/philbot-signer/issues/67 ; https://github.com/chapsrl1999-lab/philbot-signer/issues/65 ; https://github.com/chapsrl1999-lab/philbot-signer/issues/75 ; https://docs.railway.com/pricing/plans .
