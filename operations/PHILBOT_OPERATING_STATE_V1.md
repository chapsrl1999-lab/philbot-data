# PHILBOT — ÉTAT D'EXPLOITATION VERSIONNÉ V1
Dernière constitution : 2026-10-29 (America/Toronto) · niveau : partiel, preuves vérifiées ci-dessous seulement

## Objectif et source de vérité
Ce fichier décrit les faits CHANGEANTS du projet, indépendamment de AGENTS.md (règles permanentes), de la mémoire de conversation et des résultats de replay. L'agent de maintenance DOIT le lire, réconcilier avec les preuves Railway/GitHub/Health/Control réellement courantes, puis le mettre à jour avec commit confirmé. Ne jamais déduire « service rentable » ou « peut ouvrir des ordres » de Railway SUCCESS.

## Automatisations en fonctionnement (confirmées le 29 octobre)
- Garde externe PhilBot, HORAIRE, strictement lecture seule : `6a92119ca7c88191b4a579829192fee3`.
- Maintenance autonome PhilBot, TOUTES LES 4 H dès 08:00 (Québec) : `6ae32b80a2848191af3800dcb3d9bac5`. Créée et activée; **aucune intervention future n'est garantie**, exiger preuves à chaque exécution.
- Contrôle des coûts PhilBot, QUOTIDIEN dès 08:30 : `6ae32c79fc40819189066ba255c1b43f`. Créée et activée; monitoring, pas autorisation de changer le budget.
- Poursuivre la recherche PhilBot, HORAIRE : `6ade71abbff8819194aa2cb2da181f54`, obligations architecture du jeudi et forward du dimanche incorporées; tâches dédiées correspondantes désactivées seulement **après** mise à jour confirmée.
- Autres tâches ponctuelles, revues et renouvellements : distinctes. Ne pas désactiver implicitement.

## État et incidents par composant (photographies horodatées)
| Bot / composant | Source/version réellement vérifiée | État à la date du contrôle | Anomalie ou point ouvert |
|---|---|---|---|
| OUTSIDER / Hyperliquid | déploiement `e56e81ca772434d60f8b4cc06993616c665254a2` · vérifié 29 oct 2026 env. 06:31-06:47 Québec | `OUTSIDER_LIVE_READY`, `blockers=[]`; PhilBot Health 6 positions / 6 protections; incidents={} sur plusieurs cycles à 06:45-06:47 | Le défaut `TACTICAL_OPPOSES_CORE` auparavant déclenchait un halt global. Correction de traitement des refus CORE/TACTICAL validée 165/165 tests. Continuer à examiner le **matching individuel** des stops/owners, pas seulement 6/6. |
| RECENT40 / Hyperliquid | déploiement `cd3de0065a9625c9208f94fe3fd1906ee5708266` vérifié 29 oct matin | service Railway ONLINE mais métier `EXECUTION_NOT_READY`; PhilBot Health 4 positions / 4 protections; 4187 POST /candles HTTP 4xx/0 acceptés sur 24h (relevé ~06:30 Québec) | `FEED_CONFLICT_REQUIRES_REVIEW` FIL 30m, 27 oct 00:00Z, clôture et mèche différentes vs historique Binance USD-M. Garde intacte. Issue [#63](https://github.com/chapsrl1999-lab/philbot-signer/issues/63). **Interdit de lever verrou et réécrire historique sans preuve.** |
| PHILBOT HEALTH | déploiement `351a516df9b407e1c33f9679d667b76045a0a44d` vérifié 29 oct 06:44-06:47 Québec | en ligne, 11/11 sources au dernier point, 89/89 positions/protections recensées; RECENT40 encore critique; OUTSIDER sans incident | Correction 29 oct : code racine RECENT40 dans diagnostic, escalade après 30 minutes, rappels de gate espacés à 6h. Livré sans changer les règles ni les stops. Un webhook Telegram accepté sans message_id prouvé ne garantit pas la livraison. |
| TRAINS Bitunix 1H SHADOW | déploiement `89e78b8cf03b0e5b15d26b8e636ac854e5c82cf7`, 29 oct | mode SHADOW; endpoint `/trains/performance` et PnL horaire. Exemple seulement 28 oct à 21:43 : initial 605,74 USDT, equity 605,14, ROI -0,10%, PnL net -0,60, 5 trains. | Utilisateur exige une carte dans PhilBot Control. **Non installée/ni vérifiée dans le Site** ; issue [#66](https://github.com/chapsrl1999-lab/philbot-signer/issues/66). Ne pas afficher 0 ou 1000 sans registre. |
| PHOENIX dual SHADOW Bitunix | deux services `philbot-bitunix-phoenix-shadow-v1` et `philbot-bitunix-phoenix-dual-shadow` redéployés 28 oct | écrans à 1000 USD; aucun volume persistent sur les deux; un Vault HTTP 404 en restore et backup; l'autre Vault non configuré | Historique antérieur **non récupéré**; sauvegarder état actuel avant redéploiement, restauration externe, fail-closed sans état plutôt que reset silencieux. Issue [#65](https://github.com/chapsrl1999-lab/philbot-signer/issues/65). |
| HWR Hybrid BloFin | correction annoncée `3714ffa39ddb29e3157dbbf6524adbfc16fcf685` le 28 oct 16:46 Québec; contrôles de version après amendement à poursuivre | Railway service `hybrid-r4-read-check` online, volume présent, RAM ≈2,75 GB au contrôle; CPU moyen 0,115 vCPU sur dernière heure; échantillon 24h inclut l'AVANT correctif | Mesurer économies sur 24h APRÈS correctif avant de donner gain. Revue ponctuelle planifiée 29 oct 16:50 Québec. Anciens conflits historiques à examiner. |
| Autres bots live, R20, DP60, Swing, etc. | **NON CONTRÔLÉS DANS CE DOCUMENT** | inconnu ici, reprendre le vrai état via source et contrôles appropriés | Ne jamais généraliser les risques, états ou versions des bots ci-dessus. |

## Situation financière prouvée
- Gmail Railway, message daté **2026-10-28 12:26 UTC** : usage `55,08 USD`, hard limit **alors** `55 USD`, message « Deployments and Plugins Stopped ». Le plafond ACTUEL après relèvement par l'utilisateur reste **à confirmer**. Un incident équivalent est observé en septembre.
- Usage HWR Railway sur 24h relevé matin 29 oct : CPU moyen `0,332 vCPU`, RAM moyenne `2,846 Go`, période **mixte** avant/après le correctif du 28. Tarifs documentés Railway `20 USD / vCPU-mois` et `10 USD / GB-mois` (projection linéaire uniquement; ne pas confondre avec facture).
- Service `philbot-reversal-research` et `philbot-grid-range-v1` : métriques **0 CPU, 0 RAM sur la dernière heure** (jobs terminés, 0/1 réplique active malgré Railway status SUCCESS). Leur moyenne 24h comporte une exécution passée; ne pas prétendre économiser mensuellement en les arrêtant.
- Gmail Anthropic : CA$32,19 payé 19 octobre pour Claude Pro (19 oct-19 nov, taxes incluses), sans preuve des autres abonnements. N'en tirer aucun total mensuel non vérifié.
- Aucune limite Railway financière ne doit être modifiée automatiquement; anticiper 75 %, 85 %, 90 % et épuisement prévu en <48h. Cap des services Health/Guardian à protéger sans désactiver de garde.

## Dossiers opérationnels
- [#63](https://github.com/chapsrl1999-lab/philbot-signer/issues/63) — RECENT40 données FIL.
- [#64](https://github.com/chapsrl1999-lab/philbot-signer/issues/64) — programme global SRE (health, source, coût, arrêt, rollback).
- [#65](https://github.com/chapsrl1999-lab/philbot-signer/issues/65) — SHADOW sans volume, historique perdu, restauration.
- [#66](https://github.com/chapsrl1999-lab/philbot-signer/issues/66) — TRAINS dans PhilBot Control.

## Règles de mise à jour
1. Vérifier d'abord l'état effectif et identifier le bot/version/compte, pas le souvenir d'une conversation.
2. Inscrire le contrôle, la preuve, date UTC/Québec et les métriques avant/après; distinguer PROPOSÉ / TESTÉ / INSTALLÉ / VÉRIFIÉ.
3. Récupérer la révision actuelle de ce fichier, modifier sans écraser des contributions concurrentes et vérifier le commit. Une correction live exige tous les tests, rollback et deux cycles Health + lecture moteur.
4. Ne jamais déclarer un bot revenu à un capital fictif « profitable » ni masquer un fail-closed. Aucun ordre, stop, risque ou transfert modifié sans autorisation correspondante.
