# Contrôle FinOps PhilBot — 20 novembre 2026 (08:33 EST)

## Méthode et couverture
Inventaire Railway actuel : zesty-learning 22 services, philbot-rafale2-dp60 4, philbot-recent40-observer 1, philbot-r20-shadow 1 : **28 services répertoriés**. Environnements vérifiés par environment_status (incluant services sains); journaux et describe_service ciblés HWR, BRIQUES, ROTATION, REPLAY. Métriques CPU_USAGE, MEMORY_USAGE_GB, NETWORK_RX_GB et NETWORK_TX_GB lues sur 24h et 168h pour **27 services**; 1h lue pour HWR, BRIQUES, REPLAY, ROTATION, ALIGNEMENT, PERSONAL snapshots et proxy shadow. QUATRE figure encore dans list_services, mais get_service_metrics répond « Service not found in environment » sur 1h, 24h et 168h : aucune consommation ne lui est imputée sans mesure. Échantillons réseau = débits/mesures moyennes de la fenêtre, **pas** volumes facturés cumulés; pas de projection egress à partir de ces moyennes.

## Chiffres (projections, non factures)
Sur les **27 services avec mesures 24h**, somme CPU moyen 0,426218 vCPU, RAM moyenne 7,572629 Go, soit **84,25 USD/mois CPU+RAM à charge constante** (20 USD/vCPU-mois et 10 USD/Go-mois). Comparaison indicative au 19/11 85,36 USD/mois : -1,11 USD/mois, périmètre et fenêtres non nécessairement identiques, aucune économie réalisée revendiquée. Tarifs officiels Railway confirmés le 20/11 : https://docs.railway.com/pricing : egress 0,05 USD/Go, volume 0,15 USD/Go-mois, calcul facturé au prorata du temps. Exclut egress, volume, abonnement, Agent, crédits et taxes. Ne pas confondre moyenne de RAM d'un cron avec une consommation permanente lorsque son exécution est terminée.

| Service | CPU moyen 24h | RAM moyenne 24h (Go) | Projection CPU+RAM USD/mois | CPU 7j | RAM 7j (Go) |
|---|---:|---:|---:|---:|---:|
| HWR hybrid-r4-read-check | 0,148765 | 3,041470 | 33,39 | 0,147508 | 3,004915 |
| BRIQUES (cron, exécuteur REEL) | 0,028746 | 0,909639 | 9,67 | 0,029215 | 1,028607 |
| SIGNER | 0,122356 | 0,314833 | 5,60 | 0,116442 | 0,310252 |
| REPLAY R7 | 0,002197 | 0,559586 | 5,64 | 0,003165 | 0,531146 |
| R20 | 0,071858 | 0,285116 | 4,29 | 0,072334 | 0,272823 |
| CASCADE REAL | 0,012705 | 0,397616 | 4,23 | 0,012037 | 0,405337 |
| Bande & Cycle (rafale2-blofin) | 0,008854 | 0,336937 | 3,55 | 0,001338 | 0,215561 |
| OUTSIDER validation | 0,014258 | 0,320620 | 3,49 | 0,012946 | 0,309428 |
| RECENT40 | 0,003457 | 0,290440 | 2,97 | 0,003604 | 0,313890 |
| ROTATION (cron en échec) | 0,00000144 | 0,007851 | 0,079 | 0,0000882 | 0,094281 |

HWR référence avant correctif du 28/10 : 0,758 vCPU / 3,507 Go, projection historique 50,23 USD/mois. Échantillon actuel inférieur, **aucune causalité ni économie facturée démontrée**. Un échantillon 24h mixte avant/après déploiement ne prouve pas de gain.

## Anomalies et état
- **ROTATION ombre : cronFailed** depuis exécution du 20/11 00:27Z; trace exacte `RuntimeError: BINANCE_UNREACHABLE /fapi/v1/exchangeInfo`, dans `rotation_ombre.py` lignes 37/43, lors de l'obtention des symboles. Service sans volume, cron 00:20 UTC, restartPolicy NEVER. 1h CPU=RAM=0; 24h CPU ~0, RAM moyenne 0,00785 Go. Ne pas revendiquer une économie en le stoppant. Correctif proposé : traitement résilient de l'indisponibilité Binance, cache daté validé et repli seulement si données suffisamment fraîches, tests de parité et échec explicite si données invalides. **Non testé / non installé**.
- **BRIQUES : cronSucceeded**, mais les logs confirment `[BRIQUES-EXEC] REEL` et équité réelle 641,61 USD au relevé 12Z, puis traitement de 1938 trades historiques en ~150s par cycle. Ne jamais assimiler le compte fictif de simulation interne à l'exécuteur réel; ne pas toucher au moteur sans accord explicite.
- HWR online et volume /data; Health et Guardian online. R20 online, Recent40 online, DP60 Triple online; patch staged du reader DP60 depuis 05/11 toujours non appliqué. Aucun patch activé.
- PERSONAL snapshots : cronFailed depuis 06/11 et CPU/RAM 0 sur 1h, 24h, 7j. Proxy shadow : CPU/RAM 0 sur 1h/24h. ALIGNEMENT : CPU/RAM 0 sur 1h, cronSucceeded. QUATRE sans métriques accessibles, ne pas lui attribuer zéro de manière certaine.
- OUTSIDER validation : 1 build FAILED 19/11 puis déploiement SUCCESS; actuellement online.
- Bande & Cycle : RAM 24h 0,33694 Go vs 7j 0,21556 Go (+56,3%), CPU 24h 0,00885 vs 0,00134 (+561%), écart de coût CPU+RAM ~1,36 USD/mois, inférieur à 10 USD/mois; un déploiement 19/11 est visible. À diagnostiquer par fenêtre post-déploiement, sans changement de stratégie.
- Aucun trafic facturable anormal prouvé par les métriques consultées; pas de somme réseau en Go sans intégration de débit et qualification du type de mesure.

## Facturation / rentabilité
Recherche Gmail Railway après 07/11 : dernier avis d'usage **10,04 USD daté 07/11**, aucun avis billing plus récent retrouvé au 20/11. Facture Railway payée 03/11 : 71,91 USD (preuve historique du fichier d'état, non relue ici). Ancien arrêt 28/10 à 55,08/55 USD, **plafond actuel inconnu**; reset précédemment annoncé au 04/12 mais non revérifié par avis récent. Risque d'arrêt sous 24–48h **indéterminable**; ne pas augmenter les limites. Aucun PnL consolidé 30j net réalisé+flottant avec neutralisation des transferts ni ensemble complet des factures fournisseurs : **aucun bénéfice net global calculable**. Reçu Claude Pro 32,19 CAD le 19/10 historique; pas d'extrapolation.

## Actions
DÉTECTÉ : ROTATION cronFailed (cause externe Binance), hausse relative Bande & Cycle faible en USD; BRIQUES historique recalculé avec exécuteur REEL. PROPOSÉ : cache/fallback sûr pour ROTATION; profilage B&C et optimisation BRIQUES isolée avec parité. TESTÉ : lecture états, métriques, journaux, tarifs, Gmail; aucun correctif de code testé. INSTALLÉ : aucun. OBSERVÉ 24h après : sans objet. Aucun service, volume, protection, ordre, stratégie, levier, stop, risque, capital ni limite budgétaire modifié.
