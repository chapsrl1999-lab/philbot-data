# Contrôle FinOps — 16 novembre 2026, 08:45 EST

## Périmètre et méthode
Quatre projets Railway, 28 services inventoriés : zesty-learning 22, philbot-rafale2-dp60 4, philbot-recent40-observer 1, philbot-r20-shadow 1. `environment_status` consulté pour les quatre projets, `list_services` pour chaque projet, `describe_service` pour HWR, BRIQUES, ALIGNEMENT; `get_service_metrics` pour les 28 services sur 24 h et 7 j (CPU_USAGE, MEMORY_USAGE_GB, NETWORK_RX_GB, NETWORK_TX_GB), 1 h ciblée pour HWR, BRIQUES, ALIGNEMENT, QUATRE et auxiliaires; journaux HWR, BRIQUES, ALIGNEMENT, REPLAY. Une requête R20 a initialement été limitée puis relue avec succès. Les valeurs NETWORK_RX_GB/TX_GB sont des moyennes de séries, non des volumes d'egress facturés agrégés; pas de coût réseau total inféré de ces moyennes.

Tarifs officiels Railway confirmés le 16/11 : CPU 20 USD/vCPU-mois, RAM 10 USD/Go-mois, egress 0,05 USD/Go, volumes 0,15 USD/Go-mois, facturation au prorata minute; https://docs.railway.com/pricing . Projection indicative à charge constante = somme des moyennes CPU*20 + RAM*10, **85,74 USD/mois** sur 24 h, contre 85,27 USD/mois au contrôle précédent (+0,47, +0,5 %); hors egress, volumes, abonnement, Agent, taxes et crédits. Ne pas interpréter comme facture ni coût effectivement encouru. La projection sur 7 j n'est pas présentée comme référence de régime stable pour les jobs créés/récemment modifiés.

## Principaux postes, moyennes 24 h
- HWR hybrid-r4-read-check : CPU 0,164629 vCPU, RAM 3,034971 Go; **33,64 USD/mois théoriques**. Sur 7 j : 0,134428 vCPU et 2,978749 Go, soit 32,48 USD/mois. Base avant 28 octobre : 0,758 vCPU et 3,507 Go, soit 50,23 USD/mois théoriques. Comparaison descriptive uniquement; échantillon mixte avant/après et évolution de charge ne prouvent aucun gain causal ou facturé.
- BRIQUES : CPU 0,026417 vCPU, RAM 1,340220 Go, **13,93 USD/mois théoriques** contre 11,89 USD la veille; sur 7 j 0,013399 vCPU / 0,479493 Go, soit 5,06 USD/mois, fenêtre non représentative de son régime actuel. Dernier cron 13:13–13:15Z : 1930 trades historiques recalculés (69 s), traitement total 138 s; **exécuteur REEL**, équité observée ~276,55 USD, 4 positions, 0 ouverture/fermeture sur le cycle. Ne jamais traiter comme shadow inoffensif. Cache/reprise incrémentale sur clone et parité stricte, sans modification LIVE avant validation.
- SIGNER : CPU 0,113830 / RAM 0,305833, projection 5,33 USD/mois.
- CASCADE REAL : CPU 0,011552 / RAM 0,427351, projection 4,50 USD/mois. Nom Railway shadow trompeur, LIVE.
- R20 : CPU 0,071407 / RAM 0,249991, projection 3,93 USD/mois; service ONLINE mais statut d'entrées métier distinct du déploiement.
- OUTSIDER validation : CPU 0,011887 / RAM 0,302904, projection 3,27 USD/mois.
- RECENT40 : CPU 0,003640 / RAM 0,313802, projection 3,21 USD/mois.
- REPLAY : CPU 0,002121 / RAM 0,559668, projection 5,64 USD/mois; anciens 429/400 visibles dans les journaux du 12/11, aucune nouvelle erreur de ce type établie dans le court échantillon courant.
- QUATRE et ALIGNEMENT : CPU et RAM **0 sur 24 h** selon métriques, zéro sur 1 h; aucune économie nouvelle à revendiquer pour leur arrêt/sommeil. PERSONAL snapshots zéro CPU/RAM sur 24h et 7j; cronFailed depuis 06/11. Shadow read proxy zéro sur 24h.
- Les moyennes de réseau de tous les services ont été lues; pas de hausse anormale démontrée sur les séries observées. Une valeur de mémoire `current` non nulle après un cron, à elle seule, ne démontre pas un processus encore facturé : recouper statut et consommation minute.

## Disponibilité et causes
- `environment_status` : zesty-learning 22 services, 1 problème (PERSONAL snapshots cronFailed), DP60 4 sans incident Railway, Recent40 1 ONLINE, R20 1 ONLINE; DP60 readonly conserve un patch staged non appliqué. HWR a un volume persistant, BRIQUES aucun.
- HWR : sur la dernière heure CPU moyen 0,731 vCPU et RAM 3,891 Go, au-dessus des moyennes 24 h, mais échantillon ponctuel ne prouvant pas une hausse durable. Logs 13:39Z : `INCOMPLETE_SIGNALS/CURRENT_HISTORY_GAP`, `ordersPossible=false` et partial silence MELANIA, `consecutiveFailures=0`; à 07:30 EST la garde avait vu READY, donc incident métier fluctuant, pas panne Railway permanente. **Ne pas réduire ses ressources ni ses données de marché** pour optimiser la facture; suivre la fiabilité séparément.
- BRIQUES : full replay historique horaire prouvé; optimisation proposée : snapshot incrémental et cache borné, comparaison exacte des positions/ordres/frais/équité et rollback, sans toucher au LIVE avant tests et accord si impact.
- ALIGNEMENT : dernier run 13:23Z, 5 s, 62 cryptos, 3 signaux; 0 CPU/RAM sur 24h, pas un poste significatif. QUATRE cronReady sans consommation 24h. Aucune suppression rentable identifiée.
- Aucun correctif technique FinOps testé ou installé; aucune économie observée 24 h après.

## Factures, limites et rentabilité
- Recherche Gmail Railway depuis le 07/11 : dernier avis d'usage **10,04 USD le 07/11 21:16Z**, pas de nouvel avis de hard stop ni montant courant vérifié; cycle annoncé jusqu'au 04/12, plafond actuel **INCONNU**. L'ancien plafond de 55 USD du 28/10 ne doit pas être réutilisé. Risque d'arrêt sous 24–48 h **non calculable**, ni confirmé ni exclu.
- Reçu Railway 71,91 USD payé 03/11, période précédente; séparé de la projection 85,74 USD/mois et de l'avis d'usage 10,04 USD.
- Reçu Claude Pro 32,19 CAD le 19/10 et autres reçus historiques ne constituent pas le total des coûts; ChatGPT, n8n, TradingView non consolidés. PnL net réalisé + flottant 30j de tous comptes réels et transferts non réconciliés : bénéfice net PhilBot global **non calculable**. Ne pas mélanger CAD/USD ni double compter les frais déjà intégrés au PnL.

## État des actions
- **DÉTECTÉ :** BRIQUES replay complet horaire, mémoire HWR poste principal, variation HWR 1h et blocage métier transitoire, absence de données fraîches de plafond.
- **PROPOSÉ :** benchmark clone BRIQUES avec reprise incrémentale, cache et rollback; comparer sorties exactes et mesurer 24 h après. Vérifier les métriques d'egress facturées via Railway Usage, plutôt que convertir des moyennes réseau en factures.
- **TESTÉ :** lectures et réconciliation des métriques, états, journaux, tarifs, Gmail. Aucun patch de code testé.
- **INSTALLÉ :** aucun correctif FinOps.
- **OBSERVÉ 24H APRÈS :** sans objet.
- **SÉCURITÉ :** aucun service LIVE, Health/Guardian, volume, ordre, stop, levier, sizing, stratégie, capital, limite budgétaire ni alerte modifié.
