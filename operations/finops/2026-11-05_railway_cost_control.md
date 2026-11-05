# PhilBot — Contrôle FinOps du 5 novembre 2026 (vers 08 h, heure de Montréal)

**Périmètre réellement contrôlé : 30 services** Railway dans 4 projets : zesty-learning (22), philbot-rafale2-dp60 (5), philbot-recent40-observer (1), philbot-r20-shadow (2). Relevés directs `list_projects`, `list_services`, `get_service_metrics` **CPU_USAGE / MEMORY_USAGE_GB / NETWORK_RX_GB / NETWORK_TX_GB**, sur **1 h, 24 h et 168 h**; `describe_service` pour les 30, `environment_status` pour les 4 environnements, `get_logs` sur PERSONAL, HWR, R7/R9, RECENT40, signer et HWR-qualify. Certains appels métriques parallèles ont temporairement échoué, puis ont été **retentés séquentiellement jusqu'à obtenir 30/30 mesures par fenêtre**. Mesures sur fenêtres glissantes prises à quelques minutes d'intervalle : les projections ne sont pas une facture ni une mesure d'usage global du compte.

## Synthèse chiffrée

- **Projections CPU+RAM à charge constante** à partir des moyennes des 24 h : **72.62 USD/mois**; à partir des 7 jours : **69.62 USD/mois**. Comparaison au contrôle 4 nov : **71,95 USD/mois** pour 29 services (échantillons et inventaire évolutifs). Aucune économie facturée/causale revendiquée.
- Par projet (projection 24 h CPU+RAM seulement) : zesty-learning 56.98 USD/mois (22 services) ; philbot-rafale2-dp60 5.46 USD/mois (5 services) ; philbot-recent40-observer 3.54 USD/mois (1 services) ; philbot-r20-shadow 6.64 USD/mois (2 services).
- Poste principal : **HWR `hybrid-r4-read-check`**, CPU moyen **0.123264 vCPU**, RAM **2.9312 Go**, soit **31.78 USD/mois** théoriques sur 24 h. 7j : **31.28 USD/mois**. Référence *avant correctif du 28 octobre* : **0,758 vCPU / 3,507 Go = 50,23 USD/mois** théoriques. L'écart décrit une baisse mesurée sous des conditions différentes, **pas une économie vérifiée ni une causalité établie**. Une ancienne fenêtre de 24 h mêlant l'avant et l'après ne prouve rien; la fenêtre actuelle après le 28 oct traverse le déploiement du 2 nov, et les charges de marché changent.
- Top autres postes : `philbot-r20-hl` 4.23 USD/mois ; `philbot-signer` 3.95 USD/mois ; `recent40-observer` 3.54 USD/mois ; `philbot-outsider-hl-validation` 3.40 USD/mois ; `r20-shadow` 2.41 USD/mois ; `philbot-replay-r7-native` 2.22 USD/mois ; `philbot-snapback-v10r1` 2.20 USD/mois.
- Hausses mathématiques **>25 %** (24 h / 7j) : `triple-blofin` +59.1 % (1.95 USD/mois) ; `philbot-bandecycle-shadow` +137.8 % (1.70 USD/mois) ; `philbot-rafale2-swing-shadow` +33.5 % (1.09 USD/mois) ; `triple-relay` +61.3 % (1.05 USD/mois) ; `philbot-suivi` +72.8 % (0.61 USD/mois) ; `philbot-outsider-ledger-readonly` +599.6 % (0.15 USD/mois). Essentiellement **fenêtres de mise en service / redéploiement / services petits** ; pas d'attribution automatique à une fuite. Aucune nouvelle dérive >10 USD/mois démontrée hors gros poste HWR déjà suivi.
- **Réseau** : RX et TX moyens par échantillon Railway (tableau complet). Un échantillon moyen **n'est pas** une facture d'egress; public vs interne et fréquence effective doivent être réconciliés. Aucun spike d'egress payé confirmé par les flux/logs ciblés.
- **Dernière 1h CPU=RAM=0** : `philbot-control-shadow-read-proxy` SLEEPING ; `philbot-personal-snapshots` CRASHED/cronFailed (`HTTP_401`, cron 15 min) ; `philbot-signer` SUCCESS avec métriques 1h nulles **mais activité métier ingress et HTTP 200 dans les logs : ne pas assimiler à un job terminé/à arrêter**. Aucun job de recherche terminé encore présent et facturant du calcul prouvé; les anciens jobs supprimés n'achètent plus de compute, **aucune économie nouvelle ne peut être réclamée**. Le qualificatif HWR consomme encore ~0.86 USD/mois à charge constante, nécessité/dépendances non validées.

## Actions, diagnostics, gardes-fous

**DÉTECTÉ, non corrigé** : PERSONAL cron `*/15 * * * *` revient `PERSONAL_SNAPSHOT_HTTP_401`, dernier à 13:04:36Z / 08:04 EST, notifications Railway répétées. Cause observée : rejet d'authentification, pas une boucle mémoire prouvée; coûts CPU+RAM faibles. Incident #82 préexistant ; valider credentials/droits sans les exposer, puis au moins deux snapshots persistés/retraits lisibles. Ne pas couper l'alerte ni prétendre que la collecte fonctionne.

**DÉTECTÉ, non corrigé** : `philbot-replay-r7-native` logs `[REPLAY-R9] PUBLIC_HTTP_429` en rafales environ toutes les 30 minutes (11:30Z /12:00Z /12:30Z /13:01Z), tandis que ses requêtes proxy peuvent renvoyer 200. Cause plausible : quotas upstream, redondance d'appels, absence de cache. **PROPOSÉ, non testé, non installé** : profiler un lot et les statuts en lecture seule, puis cache/déduplication et backoff plafonné sur clone sans impact calcul de marché ni ordre; rollback documenté avant tout changement. Coût CPU+RAM modeste ~2.22 USD/mois, ne pas annoncer de gain avant facture.

**SURVEILLANCE sans mutation** : HWR réussit ses clôtures récentes (dernier `PREPARED_RUNTIME ok=true` 13:00:51Z) avec boucles `COLLECTOR` ~1/min et `NO_FRESH_BOUNDARY` entre bougies. Besoin d'un profilage isolé des 113 séries, cache, relectures historiques, fréquence de polling et allocation RAM avant de modifier le LIVE. Cinq changements HWR STAGED non appliqués. RECENT40 online, RAM 24h 0.337 Go vs 7j 0.339 Go; pas de dérive >25 %. Deux nouveaux auxiliaires `philbot-outsider-ledger-readonly` et `philbot-personal-readonly` apparaissent dans l'inventaire, faible coût; dépendances réelles à contrôler avant tout retrait.

**Sécurité** : aucune modification sur Railway, GitHub moteurs, bots LIVE, Health/Guardian, volumes, stratégie, capital, stops, alertes ou limites. Actions FinOps : **détecté**, **proposé**, **testé=non**, **installé=non**, **observé 24h après installation=non applicable**. Aucun service supplémentaire de monitoring créé, aucune suppression/redémarrage.

## Tarifs, facturation, risque de plafonnement, bilan projet

Tarifs publics officiels Railway, consultés le 5 nov : **20 USD/vCPU-mois**, **10 USD/Go RAM-mois**, egress **0,05 USD/Go sortant**, volumes **0,15 USD/Go-mois**, ressources calcul facturées au prorata d'utilisation. Documentation : https://docs.railway.com/pricing/plans et https://docs.railway.com/pricing . **Ne pas facturer RX comme egress sortant ni déduire facture d'une projection.**

**Facture acquittée** : reçu Railway #2308-0620 **71,91 USD payés le 3 novembre**, usage 3 oct–3 nov : mémoire 54,66, CPU 6,84, réseau 9,21, disque 0,38, Railway Agent 0,82 ; Hobby 5 USD et crédit -5 USD se neutralisent, éviter double compte. Source Gmail message `1a1a443a7f09c53c`. **Usage courant constaté mais non temps réel** : nouveau mail Railway daté du **5 novembre 00:16:28Z** : **2,56 USD** utilisés « this month » (Gmail `1a1a9106e986def4`), et non 60,08 USD du cycle précédent; cycle indiqué par reçu **3 nov–3 déc**. Le **plafond actuel** n'est pas accessible, le précédent 80 USD du 30 oct est historique. Ni coupure sous 24–48 h ni possibilité de l'exclure garanties sans consulter la limite effective; **aucune modification du plafond**.

Anthropic : reçu Claude Pro **32,19 CAD TTC le 19 oct** (référence antérieure vérifiée) ; Claude Max **142,75 CAD TTC payés le 1er nov**, avec **15,84 CAD** crédit Pro non consommé, reçu Gmail `1a1998a443efd800` (ne pas compter les deux comme un mois plein). Autres fournisseurs ChatGPT, n8n, TradingView : factures consolidées et périodicité vérifiées **non disponibles** dans cette lecture; recherches Gmail ciblées négatives pour reçus. Les PnL **nets réalisés + flottants des vrais comptes** sur 30 jours, apurement dépôts/retraits et conversion FX ne sont pas certifiés; **aucune rentabilité nette globale annoncée**. Les frais de marché ne doivent pas être soustraits une deuxième fois d'un PnL déjà net. Les coûts d'impôts et FX restent séparés.

## Tableau des 30 services — moyennes, non factures

Les valeurs RX/TX sont des **moyennes de NETWORK_RX_GB / NETWORK_TX_GB par point Railway**, pas des volumes mensuels facturables. Les 1h zéro/météo doivent être interprétées avec état et logs, non comme critères de suppression.

| Projet | Service | CPU 24h (vCPU) | RAM 24h (Go) | RX/TX 24h (Go/échantillon) | CPU 7j | RAM 7j | RX/TX 7j (Go/échantillon) | CPU/RAM 1h | État dernier déploiement | Projection 24h USD/mois |
|---|---|---:|---:|---|---:|---:|---|---|---|---:|
| zesty-learning | `philbot-outsider-ledger-readonly` | 0.000097 | 0.0147 | 0.0000003 / 0.0000002 | 0.000014 | 0.0021 | 0.0000000 / 0.0000000 | 0.00015 / 0.0204 | SUCCESS | 0.15 |
| zesty-learning | `philbot-bandecycle-shadow` | 0.000065 | 0.1694 | 0.0000006 / 0.0000011 | 0.000049 | 0.0712 | 0.0000069 / 0.0000003 | 0.00007 / 0.1814 | SUCCESS | 1.70 |
| zesty-learning | `philbot-trains-bitunix` | 0.000032 | 0.0825 | 0.0000008 / 0.0000046 | 0.000040 | 0.0853 | 0.0000010 / 0.0000076 | 0.00001 / 0.0784 | SUCCESS | 0.83 |
| zesty-learning | `philbot-range-wave-readonly` | 0.000157 | 0.0119 | 0.0000002 / 0.0000001 | 0.000276 | 0.0132 | 0.0000163 / 0.0000032 | 0.00014 / 0.0117 | SUCCESS | 0.12 |
| zesty-learning | `philbot-personal-snapshots` | 0.000002 | 0.0255 | 0.0000000 / 0.0000000 | 0.000003 | 0.0257 | 0.0000000 / 0.0000000 | 0.00000 / 0.0000 | CRASHED / cronFailed | 0.25 |
| zesty-learning | `philbot-personal-readonly` | 0.000197 | 0.0125 | 0.0000026 / 0.0000015 | 0.000198 | 0.0143 | 0.0000029 / 0.0000017 | 0.00015 / 0.0099 | SUCCESS | 0.13 |
| zesty-learning | `philbot-outsider-hl-validation` | 0.011497 | 0.3166 | 0.0002499 / 0.0001192 | 0.011891 | 0.3304 | 0.0003038 / 0.0001181 | 0.01085 / 0.3281 | SUCCESS | 3.40 |
| zesty-learning | `hybrid-hwr-qualify-node22-20261010` | 0.000369 | 0.0852 | 0.0000333 / 0.0000066 | 0.000315 | 0.0853 | 0.0000334 / 0.0000066 | 0.00041 / 0.0839 | SUCCESS | 0.86 |
| zesty-learning | `hybrid-r4-read-check` | 0.123264 | 2.9312 | 0.0012249 / 0.0002789 | 0.120958 | 2.8863 | 0.0012198 / 0.0002823 | 0.11346 / 2.9438 | SUCCESS / 5 STAGED | 31.78 |
| zesty-learning | `philbot-control-shadow-read-proxy` | 0.000124 | 0.0260 | 0.0000054 / 0.0000019 | 0.000193 | 0.0212 | 0.0000092 / 0.0000028 | 0.00000 / 0.0000 | SLEEPING | 0.26 |
| zesty-learning | `philbot-bitunix-phoenix-shadow-v1` | 0.003975 | 0.0597 | 0.0005298 / 0.0007247 | 0.003622 | 0.0608 | 0.0005271 / 0.0004566 | 0.00390 / 0.0614 | SUCCESS | 0.68 |
| zesty-learning | `philbot-replay-r7-native` | 0.002247 | 0.2176 | 0.0001610 / 0.0008189 | 0.003425 | 0.1871 | 0.0001512 / 0.0006422 | 0.00252 / 0.2224 | SUCCESS | 2.22 |
| zesty-learning | `philbot-rafale2-swing-shadow` | 0.000909 | 0.1074 | 0.0006654 / 0.0000488 | 0.000732 | 0.0804 | 0.0004285 / 0.0000501 | 0.00032 / 0.1058 | SUCCESS | 1.09 |
| zesty-learning | `philbot-guardian` | 0.002643 | 0.0800 | 0.0000366 / 0.0000137 | 0.002682 | 0.0937 | 0.0000392 / 0.0000153 | 0.00244 / 0.0773 | SUCCESS | 0.85 |
| zesty-learning | `philbot-snapback-v10r1` | 0.005661 | 0.2088 | 0.0000128 / 0.0000108 | 0.005707 | 0.2155 | 0.0000135 / 0.0000113 | 0.00546 / 0.2241 | SUCCESS | 2.20 |
| zesty-learning | `philbot-health` | 0.003055 | 0.0863 | 0.0002933 / 0.0000462 | 0.003608 | 0.0926 | 0.0003606 / 0.0000538 | 0.00268 / 0.0944 | SUCCESS | 0.92 |
| zesty-learning | `philbot-rafale2-hl` | 0.000723 | 0.1315 | 0.0004928 / 0.0000069 | 0.000608 | 0.1329 | 0.0003204 / 0.0000216 | 0.00074 / 0.1223 | SUCCESS | 1.33 |
| zesty-learning | `philbot-rafale2-blofin` | 0.000131 | 0.1637 | 0.0000049 / 0.0000042 | 0.002420 | 0.1649 | 0.0002816 / 0.0000396 | 0.00010 / 0.1868 | SUCCESS | 1.64 |
| zesty-learning | `philbot-rafale2-bitunix` | 0.000294 | 0.1061 | 0.0000089 / 0.0000254 | 0.000445 | 0.1067 | 0.0000122 / 0.0000487 | 0.00018 / 0.1076 | SUCCESS | 1.07 |
| zesty-learning | `philbot-snapback` | 0.000420 | 0.1347 | 0.0000015 / 0.0000010 | 0.000708 | 0.1385 | 0.0000047 / 0.0000040 | 0.00011 / 0.1302 | SUCCESS | 1.36 |
| zesty-learning | `faithful-passion` | 0.000003 | 0.0196 | 0.0000000 / 0.0000000 | 0.000003 | 0.0377 | 0.0000000 / 0.0000000 | 0.00000 / 0.0191 | SUCCESS | 0.20 |
| zesty-learning | `philbot-signer` | 0.071300 | 0.2525 | 0.0000249 / 0.0000167 | 0.074547 | 0.2374 | 0.0000365 / 0.0000332 | 0.00000 / 0.0000 | SUCCESS (métriques 1h nulles) | 3.95 |
| philbot-rafale2-dp60 | `philbot-suivi` | 0.003633 | 0.0533 | 0.0000060 / 0.0000361 | 0.002009 | 0.0310 | 0.0001231 / 0.0000086 | 0.00043 / 0.0499 | SUCCESS | 0.61 |
| philbot-rafale2-dp60 | `triple-relay` | 0.000209 | 0.1046 | 0.0000492 / 0.0001272 | 0.000194 | 0.0647 | 0.0000512 / 0.0001357 | 0.00025 / 0.1052 | SUCCESS | 1.05 |
| philbot-rafale2-dp60 | `triple-blofin` | 0.000850 | 0.1929 | 0.0001428 / 0.0000112 | 0.000575 | 0.1211 | 0.0001426 / 0.0000069 | 0.00093 / 0.2023 | SUCCESS | 1.95 |
| philbot-rafale2-dp60 | `philbot-dp60-readonly` | 0.000292 | 0.0152 | 0.0000062 / 0.0000163 | 0.000201 | 0.0259 | 0.0000040 / 0.0000099 | 0.00036 / 0.0102 | SUCCESS / 1 STAGED | 0.16 |
| philbot-rafale2-dp60 | `rafale2-blofin-dp60` | 0.002886 | 0.1640 | 0.0000445 / 0.0000163 | 0.004564 | 0.1689 | 0.0001171 / 0.0000468 | 0.00274 / 0.1574 | SUCCESS | 1.70 |
| philbot-recent40-observer | `recent40-observer` | 0.008740 | 0.3370 | 0.0003843 / 0.0001081 | 0.008150 | 0.3388 | 0.0002962 / 0.0000868 | 0.00819 / 0.4008 | SUCCESS | 3.54 |
| philbot-r20-shadow | `philbot-r20-hl` | 0.072680 | 0.2772 | 0.0002332 / 0.0000962 | 0.072531 | 0.2727 | 0.0002061 / 0.0000810 | 0.07085 / 0.2913 | SUCCESS | 4.23 |
| philbot-r20-shadow | `r20-shadow` | 0.016224 | 0.2090 | 0.0003658 / 0.0000818 | 0.015487 | 0.1833 | 0.0003591 / 0.0000780 | 0.01829 / 0.1950 | SUCCESS | 2.41 |

### Sources et recoupements
- Railway get_service_metrics et describe_service : 30/30 x 3 fenêtres, environnement status (4); journaux PERSONAL 401, HWR PREPARED_RUNTIME, REPLAY 429, RECENT40, signer.
- Gmail reçus et budget identifiés ci-dessus. État opérationnel courant lu sur GitHub blob `93e86bd1335caafa08d18e900dc8ad7b77936ace`, avant écriture; revérifier avant mutation.
- Issue FinOps de suivi : https://github.com/chapsrl1999-lab/philbot-signer/issues/67 .
