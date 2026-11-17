# Contrôle FinOps PhilBot — 17 novembre 2026 (08:00 EST)

## Périmètre et méthode
Railway : zesty-learning 22 services, philbot-rafale2-dp60 4, philbot-recent40-observer 1, philbot-r20-shadow 1, total 28. Inventaires, environment_status, 28/28 mesures 24h CPU_USAGE, MEMORY_USAGE_GB, NETWORK_RX_GB, NETWORK_TX_GB. Mesures 7j complètes sur les huit principaux/pertinents, non exhaustives pour les 28; mesures 1h sur six services prioritaires. Les valeurs réseau sont des moyennes des échantillons de mesure, pas des volumes d'egress facturés : ne pas les multiplier sans valider la sémantique des échantillons. Tarifs officiels https://docs.railway.com/pricing : CPU 20 USD/vCPU-mois, RAM 10 USD/Go-mois, egress 0,05 USD/Go, volume 0,15 USD/Go-mois, prorata du temps. Projection CPU+RAM = somme(20*CPU moyen 24h + 10*RAM moyenne 24h) = **86,26 USD/mois**, vs **85,74** au 16/11 (+0,52; +0,6%). Projection à charge constante, ni usage constaté ni facture. Exclut réseau, volume, agent, crédit, taxes et fournisseurs tiers.

## Principaux postes
- HWR hybrid-r4-read-check : 24h CPU 0,202339 vCPU, RAM 3,060639 Go, projection **34,65 USD/mois**. 7j CPU 0,143018, RAM 2,985356, projection **32,71 USD/mois**. CPU 24h supérieur au 7j de **41,5 %**, mais écart monétaire 24h vs 7j ~1,94 USD/mois. Baseline pré-correctif 28/10 CPU 0,758, RAM 3,507, projection 50,23 USD/mois; l'échantillon historique mixte pré/post de 24h ne prouve aucun gain causal. Déploiement HWR SUCCESS du 17/11 08:43Z, code 9da6d454; comparer 24h *entièrement* post-déploiement avant attribution. Service LIVE, volume persistant : aucun changement.
- BRIQUES : CPU 0,028085, RAM 1,015578, **10,72 USD/mois** vs 13,93 hier. 7j CPU 0,017265, RAM 0,620234, **6,55 USD/mois** (mélange périodes avant démarrage/variations de charge). Cron SUCCESS, dernier 12:15:53Z; logs 12h : recalcul 1 930 trades en 72 s, exécution ~145 s, **REEL** équité 274,45 USD, trois positions réelles, 13 legs virtuels/6 cryptos; aucune ouverture/fermeture du cycle. CPU 1h moyenne 0,0272 et RAM 0,7102, dernière valeur CPU 0 mais RAM 0,8689 Go : **ne pas conclure que le job est terminé sans consommation facturable** ni que c'est une fuite. Comparer cycle de vie Railway/échantillons après arrêt; aucune action sur exécuteur réel.
- SIGNER : CPU 0,120361, RAM 0,308052, **5,49 USD/mois**; 7j 0,112176/0,310086, **5,34 USD/mois**.
- Replay R7 : 0,001648 / 0,559234, **5,63 USD/mois**; derniers logs retournés datés 12/11 et montrent 429/400, **pas preuve de répétition le 17/11**. Cache/backoff/jitter proposé, non testé/ni installé.
- CASCADE REAL Bitunix (service nommé shadow) : 0,011928 / 0,405898, **4,30 USD/mois**; 7j 0,011024 / 0,371762, **3,94 USD/mois**. Ne pas arrêter.
- R20 : 0,070225 / 0,271285, **4,12 USD/mois**; 7j 0,071664 / 0,270188, **4,14 USD/mois**. Railway online ne prouve pas exécution métier : garde externe signale EXECUTION_NOT_READY connu.
- RECENT40 : 0,003598 / 0,349225, **3,56 USD/mois**; 7j 0,004603 / 0,332045, **3,41 USD/mois**. Railway online; exécution de trading désactivée selon état de garde, ne pas assimiler à panne de déploiement.
- OUTSIDER validation : 0,012448 / 0,311174, **3,36 USD/mois**; 7j 0,012786 / 0,305941, **3,32 USD/mois**.
- QUATRE, PERSONAL snapshots, proxy SHADOW : CPU et RAM zéro sur 24h; zéro sur 1h pour ces services; aucune économie nouvelle à revendiquer. ALIGNEMENT et ROTATION ont un peu de RAM sur 24h mais CPU/RAM zéro sur la dernière heure pour ALIGNEMENT et ROTATION (ROTATION non mesuré directement 1h; pas de conclusion catégorique sur 1h).

## État et alertes
Environment_status : zesty-learning 22 services, 1 anomalie (PERSONAL snapshots cronFailed depuis 06/11); DP60 4/4 online, ancien patch reader staged; Recent40 1/1 online; R20 1/1 online, patch staged vide. BRIQUES cronSucceeded, HWR online. Aucun nouveau service depuis inventaire 16/11. Aucun trafic facturable anormal démontré à partir des échantillons réseau. Aucune hausse totale >25% ni +10 USD/mois. HWR CPU +41,5% vs moyenne 7j : **détecté**, diagnostic complémentaire requis; le déploiement du 17/11 rend l'attribution délicate.

## Facturation
Recherche Gmail des e-mails Railway postérieurs au 07/11 : dernier avis d'usage **10,04 USD le 07/11 21:16Z**; pas de nouvel avis de consommation, de hard cap ou d'arrêt. Reçu historique payé **71,91 USD le 03/11** (source du dossier antérieur, non nouvelle facture). Cycle annoncé jusqu'au 04/12, à reconfirmer; hard cap courant inconnu. Le précédent plafond 55 USD du 28/10 ne doit pas être réutilisé. **Risque d'arrêt 24–48h indéterminable**, ne pas déclarer absent. Claude Pro 32,19 CAD le 19/10, Claude Max 142,75 CAD le 01/11 : reçus historiques distincts, aucun total fournisseurs. PnL nets réalisés+flottants 30j non consolidés et transferts non neutralisés : rentabilité nette globale non calculable.

## Statut des actions
- DÉTECTÉ : HWR CPU 24h +41,5% vs 7j; BRIQUES mémoire encore échantillonnée après CPU nul; replay anciens 429; PERSONAL snapshots déjà inactif.
- PROPOSÉ : HWR comparer une fenêtre 24h entièrement post-commit et profiler charge en lecture seule; BRIQUES vérifier état cron/RAM post-exécution et benchmark cache incrémental sur clone avec parité exacte, sans toucher à REEL; Replay cache TTL/backoff sur clone.
- TESTÉ : collecte Railway 28/28 services 24h, 8 services 7j, six 1h, descriptions HWR/BRIQUES, journaux, statut, tarifs, Gmail; **aucun correctif de code testé**.
- INSTALLÉ : **aucun correctif FinOps**.
- OBSERVÉ 24h APRÈS : sans objet.
- Aucun bot LIVE, Guardian/Health, volume, protection, alerte, stratégie, ordre, stop, sizing, levier, capital ou plafond modifié.
