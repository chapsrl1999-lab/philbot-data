# PhilBot — décision de recherche RANGE après Carver 26/27
Date : 2026-10-29 (Québec)
Statut : **AUDIT DES RÉSULTATS TERMINÉ ; nouvelles stratégies PROPOSÉES, PAS ENCORE TESTÉES**.
Périmètre : uniquement recherche hors ligne, aucun changement live, d'ordres, de sizing, de stop, d'univers ou de coûts Railway.

## Verdict
- Les chapitres 26/27 simplifiés ne possèdent pas d'avantage net démontré sur BTC en range juillet–septembre 2026. Le rapport et les chiffres testés sont dans `research/2026-10-29_carver_ch26_ch27_limits_lab_v1.md`.
- R20 est un témoin utile mais **n'a pas démontré une rentabilité de range en septembre 2026**. Les bons résultats d'octobre sont largement concentrés sur les SHORT.
- Ne pas déduire un système viable du PF de l'ancien SHADOW : cet ancien état avait fait l'objet d'une reconstruction potentiellement invalide (marks futurs, reprises sans volume).

## Faits indépendamment relus dans GitHub
Source : `chapsrl1999-lab/philbot-signer`, branche `prep/r20-hl-isolated-runtime-20261028` :
- `research/range_rejection_forward/audit/r20_replay_native_20260827_20261027_20261028.json`, blob SHA `e4b8d8e247b065f10cfdd6711bb931eedc3d604a`. Replay causal R20 sur Binance 15m proxy, 27 août–27 octobre 2026, compte neuf 1 000 USD, pas de funding ni slippage. 64 entrées, final 1 031,2789 USD (+3,1279%), PF global 1,044 ; ce chiffre comprend valorisation finale des 2 ouvertes.
- Décomposition par sens recalculée sur 64 lignes du journal : SHORT 50, +225,46 USD, PF dollars 1,51 ; LONG 14, −194,19 USD, PF dollars 0,285.
- Décomposition des LONG : M2 5 opérations, **0 gagnante**, −177,34 USD (5 stops), FDB 9 opérations, 3 gagnantes, −16,84 USD, PF 0,82. Sélection postérieure aux pertes, ne pas supprimer M2 de la stratégie live à partir de ce seul constat.
- Attribution comptable au **mois de SORTIE** des opérations, pas à la courbe MTM mensuelle : août 2 trades −64,32 USD ; septembre 37 trades −156,10 USD ; octobre 25 trades +251,70 USD. Les deux ouvertures valorisées à la borne finale sont comptées en octobre. Cette attribution N'EST PAS le rendement calendaire d'un nouveau compte à chaque mois.
- Concentration : quatre SHORT GALA, ALGO, FET et TAO du 21 octobre 2026 totalisent ~222,20 USD dans le replay Binance15m, alors que le PnL total des 64 opérations n'est que +31,28 USD. Retirer ces quatre trades fictivement n'est PAS un replay causal : admissibilité et allocations pourraient changer.
- `research/range_rejection_forward/R20_AUDIT_RECONSTRUCTION_2026-10-28.md`, blob `a2774ab33272b56252473bf6d53eb29ef957fb3d` : audit identifié des risques de reconstruction du SHADOW historique (marks contemporains utilisés lors de replays d'entrées passées, absence de volume, fallsbacks invalides). **Ne pas valider l'ancien PF4,35 du SHADOW sans réconciliation complète du registre**.
- `research/range_rejection_forward/r12_same_engine_result.json` blob `c2dd99d6465ff625c779eaf3779b056e04012b76` : *autre moteur et autre configuration*, présélectionnée sur 2025, M2 LONG positif en 2024 (22, PF dollars 1,63), 2025 (19, PF 2,97), 2026 jusqu'au 22 août (8, PF 6,41). Ce n'est **pas** une preuve de rendement pour M2 du R20 actuel ; cela interdit seulement de conclure d'une petite fenêtre récente que M2 ne peut jamais marcher.
- État Railway consulté : service `philbot-r20-hl` du projet dédié `philbot-r20-shadow`, source `prep/r20-hl-isolated-runtime-20261028`, commit `73a725d29c908a76b4d97333f2c96bfdb105360d`, dernier déploiement SUCCESS observé à 15:00:14 UTC 2026-10-29, volume /data. **Le statut SUCCESS ne démontre pas à lui seul readiness métier, ordres natifs ou rentabilité live**. Ne rien changer à ce service au cours de la recherche.

## Programme préenregistré avant nouveaux replays
**Témoin A :** R20 figé, décisions et entrées sur le même univers et données que les variantes. Journal complet, DD avec flottant, financement, frais, margin/positions, stops, mesures LONG/SHORT, régimes mensuels et concentration.

**Candidat B — Range-bornes :** identifier causalement le régime horizontal sur 4h (force de pente EMA et efficacité directionnelle, largeur/ATR); construire bornes haut/bas exclusivement depuis les barres terminées; exiger une excursion de prix et un retour confirmé en 15m/1h. Achat près de la borne basse, vente/short près de la haute. Sorties médiane du range puis extrême opposé, stop hors borne tampon ATR et timeout limité. Objectif : profiter des oscillations, pas de la cassure.

**Candidat C — False-breakout :** après une cassure de borne suivie d'une clôture à l'intérieur, entrer dans le sens du retour; invalider si la cassure reprend avec impulsion/volume. LONG et SHORT symétriques, sans double comptage des mêmes événements; TP et SL autonomes. Tous niveaux/indicateurs doivent être disponibles au moment de la décision.

**Ablation R20 LONG sans promotion live :** analyser M2 et FAILED_BREAKDOWN_FLIP séparément, tester couverture 2024/25/26 et plusieurs départs, y compris 2026 avant et après août. Une variante de sizing 0,5× M2 est un test de sensibilité, PAS une correction causale si elle ne rejoue pas admissions, marge et corrélations de portefeuille.

**Ordres limites (Carver) :** seulement une variante d'exécution après validation d'une source de rendement, comparer maker/taker et simulateur conservateur d'exécution; ne pas créditer chaque touche de prix comme exécution.

## Validation exigée
- Multiactifs : au moins l'univers R20 disponible point-in-time, éviter la sélection uniquement sur survivants actuels. Timeframes 15m/1h/4h et BTC/ETH contexte.
- Périodes : 2024 (développement), 2025 (validation chronologique), 2026 (évaluation avec biais de sélection déjà connu, explicitement non 'futur vierge'), plusieurs points de départ en compte neuf 1 000 USD, pas de position héritée, préchauffage causal indépendant.
- Métriques : rendement net par année/mois/semaine et hebdomadaire composé, PF **dollars par trade** et PF R, WR, expectancy, #trades, DD MTM, durée sous pic, worst week, frais+funding, long/short, périodes de régime, concentration, exécution, marge/liquidation.
- Tester grilles voisines de paramètres et coûts aggravés; reconstituer la chaîne signaux→admission→fills→stops→sorties ; comparer trades par ID et non seulement capital final. Pas d'autorisation LIVE sur la base d'un joli replay.
- Condition de rejet : aucun résultat net positif robuste sur plusieurs années/régimes et données de validation → piste non retenue, garder résultat négatif. Aucun plafond de rendement annuel artificiel, augmenter sizing seulement après avantage net et risque vérifié.

## État / action
- **Effectué aujourd'hui :** vérification du moteur R20 déployé (niveau source/déploiement) et audit indépendant des 64 lignes R20 août–octobre ; diagnostic M2/FDB et gains corrélés.
- **Non fait :** aucune exécution de backtest des nouveaux candidats B/C, ni replay complet natif R20 revalidé, ni comparaison de trades, ni validation effective des stops live. Étape suivante : implémenter moteur de test isolé et exécuter les candidats B/C contre le témoin A.
- Aucune tâche asynchrone créée par ce document.
