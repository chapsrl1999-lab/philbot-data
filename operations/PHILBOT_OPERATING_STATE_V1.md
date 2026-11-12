# PHILBOT_OPERATING_STATE_V1

Version d'état opérationnel initialisée le 12 novembre 2026 après lecture de la révision courante (blob vide, SHA 3f0a81c68cf94f84d1450d0037915f89b06c9e3b). Les anciennes affirmations de mise à jour ne sont pas retenues comme preuve : ce fichier était vide au début du contrôle du 12/11.

## Contrôle FinOps courant — 12 novembre 2026

- Source de détail : operations/finops/2026-11-12_railway_cost_control.md
- Périmètre Railway : zesty-learning (19 services), philbot-rafale2-dp60 (4), philbot-recent40-observer (1), philbot-r20-shadow (1), soit 25 services.
- Projection indicative CPU+RAM à charge constante : 79,95 USD/mois sur les moyennes 24h; 67,77 USD/mois sur les moyennes 7j. Ces chiffres ne sont pas une facture, excluent egress/volumes/Agent/abonnement/crédits/taxes et sont calculés aux tarifs officiels Railway 20 USD/vCPU-mois, 10 USD/Go-mois, 0,05 USD/Go egress.
- Principaux postes 24h : HWR 31,81 USD/mois théoriques; QUATRE 12,96; SIGNER 5,50; R20 4,27; CASCADE REAL 3,87; Outsider HL validation 3,47; RECENT40 3,11; Replay R7 2,48.
- QUATRE MOTEURS : cron horaire demandé, compte fictif sans ordre réel. Rejoue l'historique complet à chaque heure; 343 séries, univers 281 cryptos sur ~4 693 heures depuis 01/05/2026, cache temporaire /tmp/quatre_work, aucun volume attaché. Projection 24h 12,96 USD/mois vs 7j 2,89, hausse indicative +10,08 USD/mois; le 7j mélange anciens et nouveaux régimes. Logs 12/11 : run 366 s, puis 67 s et 72 s. Le dernier run a réussi à 13:09Z. Mémoire 1h moyenne 2,03 Go et courante 2,46 Go alors que CPU courant nul après le succès : suspicion de RAM retenue ou métrique périmée, pas preuve d'un processus actif ni d'une facturation post-job. Vérifier avant correction.
- QUATRE échec notifié 12/11 10:10Z : couverture minute Binance 50/62, archive incomplète. Correctif de complétude déjà déployé au commit 470ab901e368a7f69d7a003379df6369640d77f4; dernier cron réussi. Ce n'est pas un correctif FinOps ni une économie.
- HWR hybrid-r4-read-check : 24h 0,12735 vCPU / 2,926 Go, projection 31,81 USD/mois; 7j 0,13640 / 2,974, 32,47 USD/mois. Base avant correctif 28/10 : 0,758 vCPU / 3,507 Go, 50,23 USD/mois théoriques. Valeurs actuelles inférieures mais aucun gain causal ou facturé attribué au correctif; l'ancien échantillon 24h mixte pré/post ne prouvait rien.
- Replay R7 : erreurs upstream PUBLIC_HTTP_429 en rafales à 12:30, 13:00 et 13:30Z; backoff/jitter/cache TTL proposé sur clone, non installé.
- Deux services CPU=RAM=0 sur 1h : PERSONAL snapshots (cronFailed depuis 06/11, HTTP401) et control-shadow-read-proxy (sleeping). Aucun gain de compute à revendiquer en les supprimant.
- CASCADE service philbot-cascade-shadow est REAL/LIVE Bitunix malgré son ancien nom SHADOW; ne pas désactiver. Health et Guardian en ligne; deux builds Health échoués le 11/11 corrigés par déploiement réussi à 19:04Z. DP60 garde un patch staged non appliqué.
- Aucun volume, bot LIVE, Health/Guardian, calcul de marché, protection, alerte, stratégie, levier, sizing, ordre, stop, risque, capital ou plafond budgétaire modifié. Aucun nouveau service créé par FinOps.

## Facturation et autres fournisseurs

- Reçu Railway #2308-0620 : 71,91 USD payés le 03/11/2026 pour usage 03/10–03/11; mémoire 54,66, réseau 9,21, CPU 6,84, disque 0,38, Agent 0,82; Hobby 5 USD compensé par crédit inclus de 5 USD.
- Dernier usage courant confirmé par courriel : 10,04 USD au 07/11/2026 21:16Z. Alerte support 05/11 : soft limit 5 USD, usage 5,08 USD, cycle indiqué finissant le 04/12. Aucun avis plus récent trouvé au 12/11. HARD limit courant inconnu; ancien 80 USD du 30/10 non réutilisé; arrêt sous 24–48h non projetable.
- Anthropic : Claude Pro 32,19 CAD payé le 19/10; Claude Max 142,75 CAD payé le 01/11 avec crédit Pro inutilisé 15,84 CAD. Reçus distincts; aucun total fournisseurs global.
- Recherche Gmail récente : aucun reçu OpenAI, n8n ou TradingView trouvé dans les 45 derniers jours. Ce n'est pas une preuve d'absence de facturation.
- PnL nets réalisés + flottants 30j des comptes réels non consolidés et transferts internes non réconciliés : rentabilité nette globale PhilBot non calculable.

## État des actions

- DÉTECTÉ : QUATRE consommation élevée/full replay; mémoire possiblement conservée après cron; 429 Replay; hausses relatives mineures sur CASCADE REAL/Soldes/BloFin/Triple Relay.
- PROPOSÉ : benchmark snapshot incrémental QUATRE sur clone avec parité stricte; backoff/cache Replay sur clone; confirmer cycle de vie mémoire cron et usage par minute.
- TESTÉ : mesures, statuts, inventaire, journaux, source QUATRE, flux réseau, tarifs officiels et reçus Gmail consultés en lecture seule. Aucun correctif FinOps de code testé.
- INSTALLÉ : aucun correctif FinOps. Correctif de complétude des bougies QUATRE et tick OUTSIDER déployés par les travaux respectifs, non attribués à FinOps.
- OBSERVÉ 24h après : sans objet, aucun correctif FinOps installé.

Dernière vérification : 12 novembre 2026. Source de vérité détaillée : operations/finops/2026-11-12_railway_cost_control.md. Issue de suivi : https://github.com/chapsrl1999-lab/philbot-signer/issues/67.
