# PhilBot — recherche RANGE autonome : LABO EDGE-FIRST V1
Créé le 29 octobre 2026 — protocole de recherche, **pas un résultat de backtest**.
Statut : **PROTOCOLE ÉCRIT ET FIGÉ, DONNÉES NON ENCORE ANALYSÉES SUR CE PROTOCOLE**.
Périmètre : recherche indépendante pour identifier une source de rendement en marchés latéraux. Aucun bot live (ou shadow) n'est dans ce laboratoire, ni comme comparateur, ni comme cible de modification. Pas de déploiement, de changement d'ordres, d'API ou de budget Railway.

## Pourquoi on change
Les répétitions stratégie → filtre → optimisation → replay spectaculaire → mauvaise généralisation n'ont pas démontré de rendement robuste. Les essais Carver 26/27 rappellent qu'améliorer l'exécution par ordres limites n'est pas synonyme de créer un avantage de trading. Il faut mesurer **les comportements conditionnels réels du prix avant de choisir entrées, stops et capital**.

## Question falsifiable initiale
Quand le prix d'une crypto a fait une excursion exagérée loin d'un équilibre défini uniquement avec les barres passées, la probabilité et le gain espéré d'un retour vers cet équilibre, moins les frais/funding/slippage, sont-ils supérieurs à (a) poursuivre le mouvement, (b) ne pas négocier, et (c) entrer à des moments comparables aléatoires, dans la même période et le même actif ?

Ne pas supposer a priori que toute oscillation observée en fin de période était détectable comme range au début du mouvement.

## Données à acquérir et à auditer AVANT tout calcul de performance
- Historique OHLCV 15m (et 1h/4h agrégés causalement), perpétuels USDT pertinents pour la plateforme visée, pour 2024, 2025, 2026 ; univers point-in-time documenté, avec actifs alors disponibles et retraits, sans simple survivorship top100 actuel.
- Vérifier continuité, fuseau UTC, bougies clôturées, doublons, évolution des contrats, frais, funding lorsque disponible et différences de source ; hash des sources. Pas d'invention de périodes non couvertes.
- Contexte BTC/ETH et marché global calculé seulement avec données antérieures ou contemporaines effectivement clôturées.
- Aucun accès à l'historique complet n'est présumé ; décrire exactement la couverture acquise avant chaque calcul.

## Étape 1 : cartographie des événements, SANS construire de bot
Pour chaque actif et instant causal, mesurer à une cadence 1h et 4h :
1. Ecart signé du prix à plusieurs équilibres préspécifiés (EMA passée, centre de range roulant), normalisé par ATR/volatilité ; classes d'excès (notamment <1 ATR, 1–1.5, 1.5–2, >2). Paramètres testés en petit nombre pour limiter le biais de sélection.
2. Régime avant l'événement : efficacité directionnelle (déplacement net / somme des déplacements), pente normalisée, largeur/volatilité et synchronisation BTC/ETH. Le mot « range » ne peut être appliqué après avoir observé le futur.
3. Événements en sens LONG et SHORT séparément : simple excursion; excursion + ralentissement/rejet; fausse cassure/réintégration d'une borne causale. Définir les règles d'observation avant de regarder les rendements.
4. Échantillons de contrôle : timestamps aléatoires appariés par actif, période, volatilité et tendance; mouvement de continuation au lieu de retour; hypothèse nulle de coûts.
5. Résultats par horizon 4/12/24/48 heures : rendement brut et net d'un aller-retour proxy, MFE/MAE, probabilité de toucher +1R avant -1R et +2R avant -1R avec stop-first si OHLC ambigu, temps de retour, fréquence, séquence des résultats et corrélation entre actifs.
6. Incertitude et faux positifs : unités indépendantes regroupées par jours/semaines/épisodes de marché (pas 100 altcoins synchronisés considérés indépendants), intervalles de confiance par rééchantillonnage temporel, comptage de toutes les hypothèses examinées.

## Étape 2 : qualification d'un avantage
- Refuser les « gros PF » obtenus uniquement par un actif, quatre trades corrélés, une année, un paramètre isolé ou des coûts optimistes.
- Exiger une prime nette utile contre les contrôles, un nombre d'événements suffisant, une cohérence sur plusieurs actifs, régimes et réglages voisins et une résistance aux frais/funding/slippage aggravés.
- Ne pas limiter les ambitions de rendement annuel en fonction de chiffres de livres. La probabilité conditionnelle et l'espérance **précèdent** le sizing et le levier.

## Étape 3 : construire UNIQUEMENT si le signal survit
- Implémenter alors un moteur d'entrée/sortie complet avec validation ordre limite (franchissement ≠ exécution certaine), stops, latence, funding, maximum d'exposition, corrélation, marge et liquidation.
- Rejouer sur capital neuf 1000 USD au jour demandé, préchauffage causal indépendant, aucune position héritée, clôturé/flottant distincts.
- Mesurer rendement net, PF dollars et R, #trades, WR/espérance, DD MTM et temps sous sommet, pires semaines, répartition LONG/SHORT, frais/funding, marge et coûts dégradés.
- Validation chronologique : 2024 découverte, 2025 choix limité/validation, 2026 confirmation **contaminée par nos travaux antérieurs** et donc non « vierge » ; puis une période véritablement prospective après gel des règles. Éviter l'optimisation rétrospective cachée.

## Premier livrable avant un autre HTML de bot
Une **CARTE D'AVANTAGE STATISTIQUE** classée par famille d'événements avec : univers/période/couverture réelle, nombre d'événements indépendants, condition d'entrée causale, probabilités de retour vs continuation, gain net sous coûts, MFE/MAE, intervalle d'incertitude, contrôles et résultats par 2024/25/26. Expliquer aussi les résultats négatifs et les lacunes. Aucune courbe de trading « gagnante » n'est annoncée tant que cette carte ne montre pas un avantage plausible.

## Livrables / statut au moment de l'écriture
- Protocole préenregistré : OUI.
- Historique 60–100 actifs 2024–2026 rassemblé et vérifié pour ce protocole : NON.
- Carte statistique mesurée : NON.
- Candidats de trading testés selon ce protocole : NON.
- Déploiement live / changement de risque : AUCUN.
- Prochaine action technique : localiser et vérifier le vrai cache de chandelles et l'univers historique point-in-time, puis effectuer la carte d'événements sans réutiliser de labels futurs dans les signaux.
