# Contrôle FinOps PhilBot — 14 novembre 2026

## Sources et périmètre
Railway : 28 services inventoriés (zesty-learning 22, dp60 4, recent40 1, r20 1). Mesures CPU_USAGE, MEMORY_USAGE_GB, NETWORK_RX_GB, NETWORK_TX_GB sur 24h pour les 28 services, 1h et 7j pour les services prioritaires et plusieurs autres; **7j non exhaustif**, aucune projection globale 7j. environment_status par projet, describe_service HWR, QUATRE, BRIQUES et journaux ciblés. Le statut zesty retourne seulement 10/22 services par appel, donc les autres états individuels ne sont pas exhaustivement attestés. Réseau : moyennes d'échantillons, pas egress facturé cumulé.

Tarifs Railway officiels confirmés le 14/11 : CPU 20 USD/vCPU-mois, RAM 10 USD/Go-mois, egress 0,05 USD/Go, volume 0,15 USD/Go-mois, facturation compute au prorata du temps (https://docs.railway.com/pricing). Projections CPU+RAM = 20×CPU moyen + 10×RAM moyenne. Exclut egress, stockage, crédits, abonnement, taxes, Agent. Ni factures ni coûts constatés.

## Coûts et diagnostics
- **Total des 28 services sur moyennes 24h : 89,23 USD/mois théoriques**, dont 11,55 USD/mois historiques de QUATRE, déjà retiré le 13/11. **Hors QUATRE : 77,68 USD/mois** en projection illustrative; pas une économie réalisée ou facturée.
- **HWR** : 24h CPU 0,133274 vCPU, RAM 2,944826 Go, RX 0,00122458 Go et TX 0,00027937 Go en moyenne métrique => **32,11 USD/mois**. 7j CPU 0,126944 / RAM 2,963799 => 32,18 USD/mois. Base avant correctif 28 octobre : CPU 0,758, RAM 3,507, 50,23 USD/mois théoriques. Un échantillon mixte pré/post 24h n'est pas preuve de gain; aucun gain causal ou facturé attribué. Online, volume 1 Go.
- **QUATRE** : 24h CPU 0,000836 / RAM 1,153723 => 11,55 USD/mois historiques. **Dernière heure CPU=0 RAM=0**; service cronReady, commande de démarrage annonce explicitement le retrait du 13/11, planification 1er janvier. Pas de gain supplémentaire possible en arrêtant un calcul déjà arrêté; métriques historiques ne prédisent pas le futur.
- **BRIQUES** : nouveau cron horaire, 24h CPU 0,022850 / RAM 0,853292 => **8,99 USD/mois** théoriques. 7j CPU 0,003264 / RAM 0,121980, mélange période avant création. Logs 14/11 : recalcul de 1919 trades, 125–130 s/run, succès 13:16Z; présence de la ligne ORDRE_SEC OUVERTURE, donc ne pas conclure que le service est sans effet métier sur la seule étiquette ombre. Proposition réversible : benchmark cache/snapshot incrémental sur clone, sans changement des signaux, fréquence, exécution, capital ni protections; vérifier dépendances, parité et rollback avant déploiement.
- **SIGNER** : 24h CPU 0,111190 / RAM 0,303788 => 5,26 USD/mois; 7j CPU 0,102026 / RAM 0,292605 => 4,97; +5,9 % théoriques.
- **R20** : 24h 0,072648 / 0,269354 => 4,15 USD/mois; 7j 0,073252 / 0,281115 => 4,28; service online et volume persistant, accès métriques rétabli.
- **CASCADE REAL** (ancien nom shadow) : 24h 0,011836 / 0,384529 => 4,08 USD/mois; 7j 0,009949 / 0,288961 => 3,09; +32 % mais +0,99 USD/mois, pas une alerte de coût absolue.
- **Replay** : 24h 0,001900 / 0,366999 => 3,71 USD/mois; 7j 0,003770 / 0,260748 => 2,68; hausse +38 % (+1,03 USD/mois). Logs accessibles datés du 12/11 contiennent des PUBLIC_HTTP_429 et 400; aucune preuve de nouveaux 429 au 14/11. Cache TTL, backoff/jitter proposés sur clone, non testés.
- **RECENT40** : 24h 0,003596 / 0,311678 => 3,19 USD/mois; 7j 0,006728 / 0,327522 => 3,41. Online, volume.
- **OUTSIDER validation** : 24h 0,013789 / 0,293533 => 3,21 USD/mois; 7j 0,012603 / 0,311297 => 3,37. Online, volume.
- **ROTATION** : 1h CPU=RAM=0; 24h CPU 0,000026 / RAM 0,019369, projection 0,19 USD/mois. **ALIGNEMENT** : 1h et 24h CPU=RAM=0; 7j RAM 0,073765. **PERSONAL snapshots** : 24h CPU=RAM=0, cronFailed depuis 6/11. Ne pas revendiquer d'économie compute en les arrêtant. **BRIQUES** a CPU/RAM sur la dernière heure (cron horaire), ne pas le classer terminé définitivement.
- Les métriques RX/TX ont été relevées pour chaque service; aucune anomalie de trafic facturé démontrée. Pas de changement de service, volume ou stratégie.

## Facturation, budget et rentabilité
Gmail Railway revérifié le 14/11 : dernier avis d'usage **10,04 USD au 07/11 21:16Z**, aucun nouvel avis trouvé depuis. Message : https://mail.google.com/mail/u/?authuser=chapsrl1999%40gmail.com#all/1a1b7df31cecc612 . Dernière facture payée **71,91 USD le 03/11**, cycle précédent; distincte des projections. Fin de cycle annoncée 04/12, HARD limit actuel et usage actuel inconnus; impossible de démontrer ou d'exclure un arrêt sous 24–48h. Aucune augmentation de limite. Reçus historiques Claude Pro 32,19 CAD le 19/10 et Claude Max 142,75 CAD le 01/11 avec crédit 15,84 CAD, pas de total global. PnL réels nets 30j réalisés+flottants, dépôts/retraits, forex et factures autres fournisseurs non consolidés; revenu net global non calculable.

## Suivi des actions
**DÉTECTÉ** : BRIQUES nouveau poste de recherche à 8,99 USD/mois théoriques; QUATRE déjà retiré; hausses relatives CASCADE/Replay sous 10 USD/mois; PERSONAL snapshots en échec sans CPU/RAM.
**PROPOSÉ** : optimisation incrémentale BRIQUES sur clone et analyse des dépendances; cache/backoff Replay. Aucun arrêt de LIVE, Health/Guardian, protection ou volume.
**TESTÉ** : lectures et diagnostics seulement; aucun correctif de code testé.
**INSTALLÉ** : aucun correctif FinOps.
**OBSERVÉ 24H APRÈS** : sans objet.
Suivi : https://github.com/chapsrl1999-lab/philbot-signer/issues/67 .
