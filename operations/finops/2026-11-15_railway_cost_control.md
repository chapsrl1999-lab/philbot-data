# Contrôle FinOps — 15 novembre 2026 (08:41–08:55 EST)

## Périmètre et preuves
Railway: 28 services inventoriés (zesty-learning 22, philbot-rafale2-dp60 4, philbot-recent40-observer 1, philbot-r20-shadow 1). `list_services`, `environment_status`, `get_service_metrics` 24h sur 28/28, 7j sur principaux services et autres échantillons, 1h sur HWR/BRIQUES/QUATRE/PERSONAL, `describe_service` et journaux sur HWR, BRIQUES, QUATRE, replay. Les mesures 7j ne sont pas exhaustives pour tous les services. Pas de modification Railway.

Tarifs officiels https://docs.railway.com/pricing : CPU 20 USD/vCPU-mois, RAM 10 USD/Go-mois, egress 0,05 USD/Go, stockage volume 0,15 USD/Go-mois; compute proratisé à la minute. Projections = 20×moyenne CPU + 10×moyenne RAM, à charge constante, hors réseau, volumes, Agent, crédits, taxes et abonnements. Ne pas les confondre avec coût constaté/facture.

## Coût et écarts
Projection CPU+RAM 24h sur 28 services = **85,27 USD/mois** (14/11 : 77,68 USD/mois hors QUATRE; écart +7,59 USD/mois, pas une dépense facturée). HWR **32,45** (CPU 0,13627 vCPU, RAM 2,97223 Go; 7j CPU 0,12917, RAM 2,96701), BRIQUES **11,89** (CPU 0,04449, RAM 1,10027; 7j CPU 0,00962, RAM 0,28412; 7j inclut avant lancement, ne prouve pas une hausse anormale de régime), SIGNER **5,30**, REPLAY **5,74**, CASCADE REAL **4,27**, R20 **4,08**, RECENT40 **3,69**, OUTSIDER validation **3,22** USD/mois. Le reste se répartit entre 20 autres services. La RAM de BRIQUES représente 11,00 USD/mois théoriques, CPU 0,89. Réseau RX/TX relevé pour 28/28; ce sont des moyennes de métriques, pas des volumes d'egress facturés; aucune anomalie d'egress établie.

HWR référence avant correctif 28/10 : CPU 0,758 et RAM 3,507, soit 50,23 USD/mois théoriques; actuellement 32,45. Écart théorique ≈−17,78 USD/mois, **aucune économie causale/facturée prouvée**. Un échantillon 24h mixte avant/après ne démontre pas un gain post-déploiement.

QUATRE : retiré le 13/11, cron modifié en exécution annuelle inerte; CPU et RAM zéro sur 24h et 1h; aucune nouvelle économie à revendiquer. PERSONAL snapshots : cronFailed depuis 06/11, CPU/RAM zéro sur 24h et 1h; pas de gain en le désactivant. BRIQUES : cronSucceeded mais la RAM moyenne sur la dernière heure 0,609 Go et métrique courante 1,235 Go alors que CPU courant 0; déterminer si métrique périmée ou mémoire encore facturable après fin du cron avant d'affirmer une fuite.

**Fait opérationnel important** : contrairement à son suffixe « ombre », BRIQUES exécute aussi un module **RÉEL** : journaux 15/11 13:17Z indiquent `[BRIQUES-EXEC] REEL`, équité ~273,75 USD, 4 positions réelles, zéro ouverture/fermeture au cycle. Le cron 13:10–13:17 a duré 425 s contre 235 s au cycle 11:10–11:14; univers horaire 214 s contre 27 s, 1 930 trades historiques rejoués. Le statut métier et les dépendances doivent être reconnus avant tout correctif FinOps; **ne pas suspendre ce service**. Différence de durée potentiellement liée aux téléchargements/historiques; cause non démontrée. Optimisation proposée seulement : cache de données immutable/récupération incrémentale, tests de parité stricte sur clone sans accès ordre, rollback documenté, aucun changement de cadence/stratégie.

HWR journaux : nombreux `NO_FRESH_BOUNDARY` entre clôtures, mais `ordersPossible=true` et `READY` après clôture; pas de preuve d'une boucle de calcul fautive. Replay : 429 historiques visibles dans les derniers logs consultés (12/11), pas preuve de 429 récents 15/11. Backoff/cache proposés non installés.

État Railway : Health, Guardian, HWR, CASCADE, R20, RECENT40, Triple online; DP60 readonly a un patch staged depuis 05/11, non appliqué; R20 a un patch staged sans changements; PERSONAL cronFailed. 22+4+1+1 services listés, 10/22 services zesty visibles dans le premier `environment_status` (limite 10). Aucun service coupé.

## Factures, limites et résultat économique
Gmail Railway recherché après 07/11 : dernier mail d'usage daté 07/11, **10,04 USD**; aucun nouveau mail de plafond/hard stop. Dernière facture Railway payée 03/11 : 71,91 USD (preuve historique); prochain reset signalé 04/12; **hard cap courant inconnu**, risque d'arrêt sous 24–48h non calculable, ne pas réutiliser les anciens plafonds 55/80 USD. Claude Pro 32,19 CAD payé 19/10, Claude Max 142,75 CAD 01/11 avec crédit 15,84 CAD : reçus historiques, pas total global. PnL nets 30j réels réalisés+flottants, flux dépôts/retraits et factures ChatGPT/n8n/TradingView incomplets; revenu net après abonnements non calculable. Aucune augmentation automatique des limites.

## Statut des actions
- DÉTECTÉ : BRIQUES 11,89 USD/mois projetés; durée cron variable, 1 930 trades recalculés; présence de module REEL; RAM résiduelle à vérifier; HWR principal poste.
- PROPOSÉ : cache/reprise incrémentale BRIQUES sur clone sans ordre, comparaison sortie bit à bit et 7 cycles, test rollback; évaluer métrique RAM après cron et logs HWR; pas de suppression sans dépendances prouvées.
- TESTÉ : relevés métriques/statuts/logs et tarifs, **aucun patch de code testé**.
- INSTALLÉ : aucun correctif FinOps.
- OBSERVÉ 24h après : sans objet.

Source d'état versionnée : operations/PHILBOT_OPERATING_STATE_V1.md; suivi FinOps : https://github.com/chapsrl1999-lab/philbot-signer/issues/67.
