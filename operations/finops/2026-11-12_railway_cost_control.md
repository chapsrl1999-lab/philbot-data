# PhilBot — contrôle FinOps du 12 novembre 2026

**Statut : DÉTECTÉ + PROPOSÉ. Aucun correctif FinOps de code installé.** Contrôle lecture seule effectué le 12/11/2026 vers 13:45–14:00 UTC dans les environnements production des quatre projets Railway : **25 services** (19 zesty-learning, 4 philbot-rafale2-dp60, 1 philbot-recent40-observer, 1 philbot-r20-shadow). Mesures CPU, RAM, RX et TX sur 1h, 24h et 168h; inventaires, statuts, journaux de déploiement et flux réseau inspectés.

## Tarifs Railway officiels et méthode

Source officielle consultée le 12/11 : https://docs.railway.com/pricing/plans

- CPU : **20 USD/vCPU-mois**; RAM : **10 USD/Go-mois**; egress : **0,05 USD/Go**; volume : **0,15 USD/Go-mois**. Les ressources sont facturées à l'usage réel, au prorata du temps (par seconde).
- Les projections ci-dessous sont **CPU + RAM seulement**, calculées à partir des moyennes des échantillons : moyenne CPU × 20 + moyenne RAM × 10, annualisées en équivalent 30 jours à charge constante. Elles excluent egress facturable, volumes, Agent, abonnement, crédits et taxes; ce ne sont ni des factures ni du coût déjà payé.
- Les moyennes RX/TX du connecteur sont des **moyennes d'échantillons**, pas des totaux de GB du cycle. Elles ne sont donc pas multipliées par 0,05 USD/Go pour inventer un coût egress. Les flux réseau échantillonnés n'ont montré aucun volume sortant anormal; ils ne sont pas exhaustifs.
- Échantillonnage : 1h à 30 s (~121 points), 24h à 300 s (~289 points), 7j à 900 s (~673 points).

## Résumé des projections CPU + RAM

- **24h : 79.95 USD/mois** à charge constante.
- **7j : 67.77 USD/mois** à charge constante.
- Écart 24h vs 7j : **+12.17 USD/mois (+18.0%)**. Les fenêtres se chevauchent et le régime QUATRE a changé récemment : ce n'est pas une mesure de facture incrémentale.
- Comparaison au rapport du 11/11 (77,77 USD/mois sur 24h) : **+2.18 USD/mois** sur le même périmètre de 25 services; différence de projection, non dépense réalisée.

### Répartition par projet

| Projet | Projection 24h | Projection 7j |
|---|---:|---:|
| zesty-learning | 68.38 USD/mois | 55.84 USD/mois |
| philbot-rafale2-dp60 | 4.20 USD/mois | 4.06 USD/mois |
| philbot-recent40-observer | 3.11 USD/mois | 3.50 USD/mois |
| philbot-r20-shadow | 4.27 USD/mois | 4.37 USD/mois |

### Principaux postes

| Service | Projection 24h | Projection 7j |
|---|---:|---:|
| hybrid-r4-read-check (zesty-learning) | 31.81 | 32.47 |
| philbot-quatre-ombre (zesty-learning) | 12.96 | 2.89 |
| philbot-signer (zesty-learning) | 5.50 | 4.51 |
| philbot-r20-hl (philbot-r20-shadow) | 4.27 | 4.37 |
| philbot-cascade-shadow (zesty-learning) | 3.87 | 2.36 |
| philbot-outsider-hl-validation (zesty-learning) | 3.47 | 3.36 |
| recent40-observer (philbot-recent40-observer) | 3.11 | 3.50 |
| philbot-replay-r7-native (zesty-learning) | 2.48 | 2.45 |
| philbot-rafale2-blofin (zesty-learning) | 1.99 | 1.83 |
| triple-blofin (philbot-rafale2-dp60) | 1.89 | 1.91 |

## Tableau détaillé — CPU/RAM et état

CPU/RAM sont des moyennes d'usage en vCPU et Go. Le coût projeté 24h/7j est CPU+RAM uniquement. Les deux seules lignes avec CPU **et** RAM moyens nuls sur la dernière heure sont PERSONAL snapshots et le proxy SHADOW.

| Projet | Service | État Railway / contexte | CPU 1h moy. | RAM 1h moy. (Go) | CPU 24h moy. | RAM 24h moy. (Go) | $/mois 24h | $/mois 7j |
|---|---|---|---:|---:|---:|---:|---:|---:|
| zesty-learning | hybrid-r4-read-check | online | 0.131191 | 2.954 | 0.127353 | 2.926 | 31.81 | 32.47 |
| zesty-learning | philbot-quatre-ombre | cronSucceeded; RAM non nulle après succès | 0.008070 | 2.034 | 0.018671 | 1.259 | 12.96 | 2.89 |
| zesty-learning | philbot-signer | online | 0.115123 | 0.317 | 0.112172 | 0.326 | 5.50 | 4.51 |
| philbot-r20-shadow | philbot-r20-hl | online | 0.069246 | 0.303 | 0.071931 | 0.283 | 4.27 | 4.37 |
| philbot-recent40-observer | recent40-observer | online | 0.004370 | 0.261 | 0.005032 | 0.300 | 3.11 | 3.50 |
| zesty-learning | philbot-cascade-control-readonly | online | 0.000234 | 0.006 | 0.000187 | 0.006 | 0.07 | 0.05 |
| zesty-learning | philbot-soldes-relay | online | 0.000059 | 0.053 | 0.000076 | 0.051 | 0.51 | 0.32 |
| zesty-learning | hybrid-r4-market-data | online | 0.000275 | 0.062 | 0.000255 | 0.063 | 0.63 | 0.55 |
| zesty-learning | philbot-cascade-shadow | online — REAL/LIVE Bitunix; ancien nom SHADOW | 0.013744 | 0.398 | 0.011460 | 0.365 | 3.87 | 2.36 |
| zesty-learning | philbot-outsider-ledger-readonly | online | 0.000145 | 0.009 | 0.000133 | 0.009 | 0.09 | 0.11 |
| zesty-learning | philbot-range-wave-readonly | online | 0.000165 | 0.011 | 0.000151 | 0.011 | 0.11 | 0.12 |
| zesty-learning | philbot-personal-snapshots | cronFailed depuis 06/11; zéro compute | 0.000000 | 0.000 | 0.000000 | 0.000 | 0.00 | 0.04 |
| zesty-learning | philbot-personal-readonly | online | 0.000247 | 0.012 | 0.000181 | 0.012 | 0.12 | 0.11 |
| zesty-learning | philbot-outsider-hl-validation | online; déploiement 12/11 13:02Z | 0.028684 | 0.282 | 0.013036 | 0.321 | 3.47 | 3.36 |
| zesty-learning | philbot-control-shadow-read-proxy | sleeping; zéro compute 1h | 0.000000 | 0.000 | 0.000015 | 0.038 | 0.38 | 0.34 |
| zesty-learning | philbot-rafale2-swing-shadow | online | 0.000541 | 0.104 | 0.000472 | 0.105 | 1.06 | 1.06 |
| zesty-learning | philbot-guardian | online; protection conservée | 0.002205 | 0.250 | 0.002118 | 0.096 | 1.01 | 0.92 |
| zesty-learning | philbot-health | online; 2 builds échoués puis corrigés | 0.002767 | 0.079 | 0.002559 | 0.077 | 0.82 | 0.96 |
| zesty-learning | philbot-rafale2-hl | online | 0.000639 | 0.136 | 0.000679 | 0.147 | 1.48 | 1.37 |
| zesty-learning | philbot-rafale2-blofin | online | 0.000651 | 0.216 | 0.000630 | 0.198 | 1.99 | 1.83 |
| zesty-learning | philbot-replay-r7-native | online; PUBLIC_HTTP_429 en rafales | 0.002240 | 0.266 | 0.003729 | 0.241 | 2.48 | 2.45 |
| philbot-rafale2-dp60 | philbot-suivi | online | 0.000229 | 0.090 | 0.004027 | 0.092 | 1.00 | 0.95 |
| philbot-rafale2-dp60 | triple-relay | online | 0.000167 | 0.118 | 0.000244 | 0.119 | 1.20 | 1.09 |
| philbot-rafale2-dp60 | triple-blofin | online | 0.000807 | 0.161 | 0.000906 | 0.188 | 1.89 | 1.91 |
| philbot-rafale2-dp60 | philbot-dp60-readonly | online; patch STAGED non appliqué | 0.000409 | 0.011 | 0.000362 | 0.010 | 0.11 | 0.11 |

## Réseau — moyennes d'échantillons en Go

RX = entrant; TX = sortant. Ces valeurs ne sont **pas** des totaux de transfert facturable. 24h échantillonné toutes les 5 min; 7j toutes les 15 min.

| Projet | Service | RX moy. 24h | TX moy. 24h | RX moy. 7j | TX moy. 7j |
|---|---|---:|---:|---:|---:|
| zesty-learning | hybrid-r4-read-check | 0.00554119 | 0.00127603 | 0.01668016 | 0.00388287 |
| zesty-learning | philbot-quatre-ombre | 0.00388652 | 0.00016557 | 0.00725567 | 0.00021940 |
| zesty-learning | philbot-signer | 0.00010039 | 0.00003086 | 0.00027678 | 0.00010014 |
| philbot-r20-shadow | philbot-r20-hl | 0.00071291 | 0.00034595 | 0.00248145 | 0.00111695 |
| philbot-recent40-observer | recent40-observer | 0.00047568 | 0.00018138 | 0.00576366 | 0.00147011 |
| zesty-learning | philbot-cascade-control-readonly | 0.00003686 | 0.00003402 | 0.00002317 | 0.00002006 |
| zesty-learning | philbot-soldes-relay | 0.00003868 | 0.00003043 | 0.00006238 | 0.00004967 |
| zesty-learning | hybrid-r4-market-data | 0.00016599 | 0.00003269 | 0.00042549 | 0.00008498 |
| zesty-learning | philbot-cascade-shadow | 0.00417814 | 0.00035716 | 0.00552307 | 0.00031620 |
| zesty-learning | philbot-outsider-ledger-readonly | 0.00000179 | 0.00000140 | 0.00000492 | 0.00000372 |
| zesty-learning | philbot-range-wave-readonly | 0.00000000 | 0.00000000 | 0.00000000 | 0.00000000 |
| zesty-learning | philbot-personal-snapshots | 0.00000000 | 0.00000000 | 0.00000001 | 0.00000001 |
| zesty-learning | philbot-personal-readonly | 0.00000924 | 0.00000571 | 0.00003253 | 0.00002059 |
| zesty-learning | philbot-outsider-hl-validation | 0.00182535 | 0.00061808 | 0.00452644 | 0.00179549 |
| zesty-learning | philbot-control-shadow-read-proxy | 0.00000031 | 0.00000016 | 0.00001040 | 0.00000286 |
| zesty-learning | philbot-rafale2-swing-shadow | 0.00012107 | 0.00030063 | 0.00180108 | 0.00078170 |
| zesty-learning | philbot-guardian | 0.00015138 | 0.00007643 | 0.00046859 | 0.00021574 |
| zesty-learning | philbot-health | 0.00108811 | 0.00019343 | 0.00334775 | 0.00058795 |
| zesty-learning | philbot-rafale2-hl | 0.00025216 | 0.00005741 | 0.00112564 | 0.00039363 |
| zesty-learning | philbot-rafale2-blofin | 0.00016787 | 0.00015369 | 0.00011965 | 0.00011033 |
| zesty-learning | philbot-replay-r7-native | 0.00145924 | 0.00319064 | 0.00304801 | 0.00682703 |
| philbot-rafale2-dp60 | philbot-suivi | 0.00020574 | 0.00009448 | 0.00040500 | 0.00023114 |
| philbot-rafale2-dp60 | triple-relay | 0.00030161 | 0.00079762 | 0.00059677 | 0.00151483 |
| philbot-rafale2-dp60 | triple-blofin | 0.00083747 | 0.00005102 | 0.00167843 | 0.00014724 |
| philbot-rafale2-dp60 | philbot-dp60-readonly | 0.00003601 | 0.00009552 | 0.00010529 | 0.00027623 |

## Diagnostic des anomalies et causes

### 1. QUATRE MOTEURS — hausse majeure confirmée sur le poste de recherche

- Service philbot-quatre-ombre, cron 5 * * * *, aucun volume monté, compte fictif/shadow, aucun ordre réel.
- Projection CPU+RAM 24h : **12.96 USD/mois**; fenêtre 7j : **2.89 USD/mois**. Écart **+10.08 USD/mois théoriques** (+348.9%). Le 7j inclut une partie de l'ancien cron et des nouveaux passages horaires; ce n'est pas une baseline homogène.
- Cause de recalcul démontrée dans le code déployé : chaque passage horaire recharge 343 séries, reconstruit l'univers de 281 cryptos sur ~4 693 heures depuis le 01/05/2026, recalcule les signaux et rejoue le compte fictif depuis le 05/11. Le cache de travail est sous /tmp/quatre_work; aucun volume n'est attaché, donc pas de cache inter-conteneur persistant. La cadence horaire est une demande utilisateur; **ne pas la réduire**.
- Logs du 12/11 : un passage de **366 s** à 11:13Z, puis **67 s** à 12:08Z et **72 s** à 13:09Z. Le dernier passage a publié l'état dans PhilBot Suivi. Les durées et relectures complètes expliquent une grande part de la charge, mais la part évitable n'est pas encore mesurée.
- **Signal supplémentaire à vérifier :** le cron est déclaré cronSucceeded après 13:09Z, CPU courant nul, mais la métrique 1h donne RAM moyenne **2,03 Go** et mémoire courante **2,46 Go** près de 47 minutes après la fin du dernier journal. Cela peut être une instance gardant sa RAM ou un échantillon Railway périmé; **ce n'est pas encore la preuve qu'un processus continue ou que la mémoire est facturée pendant toute l'attente**. Vérifier l'évolution de la mémoire et les unités par minute du workspace avant de corriger.
- Échec Railway notifié à 10:10Z : l'archive Binance du 11/11 était incomplète pour 12/62 séries minute (couverture 50/62), le direct ne prenait que le 12/11 et QUATRE a échoué à publier. Le déploiement suivant du 12/11 10:40Z (commit 470ab901e368a7f69d7a003379df6369640d77f4) reprend maintenant aussi la dernière journée d'archive, en retirant les doublons; test four/test_live_overlap.py annoncé dans le commit. Déploiement SUCCESS; exécutions 11:13, 12:08, 13:08Z réussies. **Correction de données déjà déployée, pas une optimisation FinOps ni une économie réalisée.** Calcul et compte fictif déclarés inchangés.
- **PROPOSÉ, non testé/installé par FinOps :** benchmarker sur clone isolé un snapshot incrémental/reprise du dernier état horaire, avec parité stricte des trades, entrées/sorties, frais, positions ouvertes, panier, horodatages et reprises après crash/gap sur au moins 7 clôtures horaires. Le stockage existant côté PhilBot Suivi peut être évalué avant d'envisager un volume; ne pas créer de nouveau service ni toucher à la fréquence, au moteur CASCADE LIVE, aux protections, au capital ou au récepteur Suivi.

### 2. HWR — premier poste, comparaison prudente

- hybrid-r4-read-check : **0,12735 vCPU / 2,926 Go** sur 24h = **31.81 USD/mois** à charge constante; 7j **0,13640 / 2,974 Go = 32.47 USD/mois**.
- Base pré-correctif du 28/10 : **0,758 vCPU / 3,507 Go = 50,23 USD/mois** théoriques CPU+RAM. La mesure actuelle est inférieure, mais on ne peut pas attribuer l'écart au seul correctif : autres déploiements et charge de marché ont changé. L'ancien échantillon de 24h mixte avant/après le correctif n'était pas une preuve; ce relevé du 12/11 est postérieur, mais ne prouve toujours pas une économie facturée ou causale.
- Volume hybrid-r4-public-candles préservé; aucune réduction de RAM/CPU ni suppression de données proposée sans profilage et preuve de neutralité métier.

### 3. Replay R7 — erreurs upstream, pas fuite egress démontrée

- Logs PUBLIC_HTTP_429 répétés en rafales à 12:30Z, 13:00Z et 13:30Z. La projection CPU+RAM reste **2.48 USD/mois**; RX/TX moyen 24h inférieur à la moyenne 7j. Les flux échantillonnés sont de petits échanges; aucune anomalie de trafic facturable établie.
- Cause probable à confirmer dans le client : appels/retries regroupés sur les frontières de demi-heure et limites upstream. **PROPOSÉ** : backoff exponentiel + jitter, déduplication et cache TTL sur clone, avec comparaison de données et rollback; ne pas masquer les erreurs ni modifier le flux LIVE.

### 4. Hausses relatives sur petites bases

- philbot-cascade-shadow : +54% CPU et +65% RAM vs 7j, projection **3,87 USD/mois** contre 2,36. Le nom est historique : branche de déploiement feat/quatre-reel-bitunix-20261111, service **REAL/LIVE Bitunix** selon l'état opérationnel récent. **Ne pas désactiver ni traiter comme job shadow.**
- philbot-soldes-relay : +51% CPU / +57% RAM, mais seulement **0,51 USD/mois** projetés.
- philbot-rafale2-blofin : CPU +240% vs 7j, mais coût projeté **1,99 USD/mois** (écart d'environ 0,16 USD); pas une fuite matérielle.
- triple-relay : CPU +31%, coût **1,20 USD/mois**; hausse faible en dollars.
- Le service philbot-outsider-hl-validation a reçu un déploiement le 12/11 13:02Z (ce n'est pas un nouveau service dans l'inventaire). Le commit e3aa100 ajoute un tick 11 s après les frontières de 15 min et des journaux de refus/stale; fraîcheur 90 s, risque et stratégie inchangés. Sa projection **3,47 USD/mois** et son volume de validation sont documentés; aucune redondance prouvée, ne pas couper.

### 5. Jobs terminés, protections et changements en attente

- philbot-personal-snapshots : cronFailed depuis le 06/11, erreurs PERSONAL_SNAPSHOT_HTTP_401; CPU et RAM **0 sur 1h et 24h**, presque nuls sur 7j. Aucune économie de calcul à revendiquer en l'arrêtant. Le code d'appel utilise le jeton PHILBOT_CONTROL_SITE_TOKEN; authentification à corriger seulement si ce composant est encore requis.
- philbot-control-shadow-read-proxy : deployment SLEEPING; CPU/RAM **0 sur 1h**. Aucune économie CPU/RAM additionnelle à prétendre en le supprimant.
- philbot-health : deux builds échoués le 11/11 car le test de maintenance lisait le B&C public et trouvait 2 positions au lieu d'une; correctif de test déployé à 19:04Z, état actuel ONLINE. Health et Guardian, volumes et alertes préservés.
- DP60 : un patch STAGED non appliqué sur philbot-dp60-readonly (1 changement ressource). FinOps ne l'a ni accepté ni rejeté.
- Aucun volume, service LIVE, Health/Guardian, calcul nécessaire, protection, alerte, stratégie, ordre, stop, sizing, risque, capital ou plafond modifié.

## Facturation réellement prouvée vs projections

- **Vraie facture payée : 71,91 USD le 03/11/2026**, reçu Railway #2308-0620, période ressource 03/10–03/11 : mémoire **54,66 USD**, réseau **9,21**, CPU **6,84**, disque **0,38**, Agent **0,82**. Plan Hobby 5 USD pour 03/11–03/12 compensé par crédit inclus de 5 USD; total payé 71,91 USD. Ce reçu est distinct de l'usage courant.
- **Dernier usage courant confirmé par e-mail : 10,04 USD au 07/11/2026 21:16Z.** L'alerte support du 05/11 donne un seuil souple de 5 USD, usage 5,08 USD et fin de cycle au 04/12. Aucune alerte usage/billing plus récente trouvée jusqu'au 12/11. Le plafond HARD courant n'est pas exposé dans les courriels lus; l'ancien 80 USD du 30/10 n'est pas réutilisé. Le reçu de plan indique 03/11–03/12, l'alerte support 04/12 : une journée d'écart de date est à réconcilier. Sans usage courant ni HARD limit, **pas de projection fiable d'arrêt dans les 24–48h** et aucune limite modifiée.
- Anthropic : reçu Claude Pro **CA$32,19 payé le 19/10**; reçu Claude Max **CA$142,75 payé le 01/11**, comprenant un crédit de temps Pro inutilisé de **CA$15,84**. Montants CAD, reçus séparés; aucun total fournisseurs global.
- Recherche Gmail récente : aucun reçu/facture OpenAI correspondant à un abonnement ChatGPT, aucun reçu n8n ou TradingView dans les 45 derniers jours. Cela ne prouve pas l'absence d'autres prélèvements ou factures ailleurs.
- Aucun PnL net réalisé + flottant 30j consolidé, neutralisé des transferts internes et des frais déjà inclus, disponible pour comparer au coût complet. **Rentabilité nette globale PhilBot non calculable.**

## Statuts d'action

- **DÉTECTÉ :** coût QUATRE en hausse majeure; full-replay horaire confirmé; mémoire non nulle après cronSucceeded à vérifier; 429 Replay; hausses relatives CASCADE REAL/Soldes/BloFin/Triple Relay; snapshots PERSONAL en échec mais inactif.
- **PROPOSÉ :** snapshot incrémental/parité sur clone QUATRE; backoff/cache Replay; vérification du cycle de vie mémoire cron et de l'usage par minute Railway.
- **TESTÉ :** lectures métriques, état, inventaire, journaux, source QUATRE, flux réseau, tarifs officiels et reçus Gmail; aucun correctif de code FinOps exécuté.
- **INSTALLÉ :** aucun correctif FinOps. Le correctif de complétude des bougies QUATRE (commit 470ab901) et le tick OUTSIDER (commit e3aa100) étaient déjà déployés par leurs travaux respectifs; ils ne sont pas des optimisations de coûts.
- **OBSERVÉ 24h après :** sans objet pour une optimisation FinOps, aucune optimisation installée.

## État de reprise opérationnelle

La révision courante de operations/PHILBOT_OPERATING_STATE_V1.md a été lue avant ce contrôle : **contenu vide (blob SHA 3f0a81c68cf94f84d1450d0037915f89b06c9e3b)**. Ce rapport initialise l'état opérationnel après relecture du SHA; ne pas se fier aux anciens messages qui affirmaient que le fichier avait été actualisé. Rapport vérifié après écriture; état opérationnel à relire après mise à jour.

Sources primaires : Railway API lecture seule (métriques, inventaire, statuts, journaux et flux), Gmail reçu Railway #2308-0620 / alertes 05 et 07/11 / reçus Anthropic #2205-7093-5830 et #2320-2365-0776, tarifs officiels Railway ci-dessus, GitHub chapsrl1999-lab/philbot-signer et chapsrl1999-lab/philbot-data.
