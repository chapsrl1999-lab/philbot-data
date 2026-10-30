# PhilBot — test unique du moteur autonome bayésien de régimes, AVANT résultats
30 octobre 2026. Recherche hors ligne. Aucun changement à Swing, Sélectif, DUO, R20 ni aucun autre bot. R20 **totalement exclu**, même comme témoin.

## Pourquoi cette hypothèse
Le lot104 du laboratoire PhilBot proposait un moteur BOCPD (Bayesian Online Change Point Detection, Adams/MacKay) sur les régimes de la distribution des rendements. Son code d'origine (lot104/bocpd.py, preuve original du 29 octobre) a démontré une récurrence bayésienne mathématiquement exacte sur données **synthétiques** mais **n'a jamais produit de compte ni de PNL de crypto**. C'est une famille distincte de STC/AlgoAlpha, funding, paire/écart et simple reversal; l'intérêt n'est PAS démontré. Étude en lecture seule.

## Hypothèse pré-gelée
La probabilité bayésienne d'un rendement natif 4h supérieur à 40 points de base, compte tenu du **régime observé jusqu'à t**, permet-elle de sélectionner LONG, SHORT ou FLAT après une barre d'attente entière, en améliorant le rendement net pendant BTC sans forte tendance ? Si non, **rejeter cette formulation sans optimiser**.

## Univers, horloge, données
8 marchés Binance USD-M : BTC ETH SOL XRP ADA DOGE AVAX LINK, sans retrait après résultats. 4h construit causalement par regroupement des 4 bougies natives 1h. Historique août–décembre 2023 pour warm-up/échelle, 2024 pour sélectionner une fois le hazard selon **score prédictif** (aucun PNL), 2025 pour validation gelée, janvier–septembre 2026 pour test pseudo-OOS (déjà connu par le projet; PAS prospectif vierge). Archive officielle Binance USD-M 1h, ZIP et SHA256 vérifiés dans les travaux du 29 octobre. Rapport trous/alias et exclusion si manquants, pas d'imputation.
4h x[t]=log(close4h/open4h) / std des rendements 2023 tous actifs; échelle figée au 31 décembre 2023. Prior NIG mu0=0,kappa1,alpha2,beta1 sur x standardisé. Hazard constant 1/24,1/72,1/168 natifs : sélectionner sur 2024 le meilleur score **log predictive likelihood** cumulé (pas performance financière); un hazard commun à l'univers, départage préférence 168. Ensuite bloquer cette valeur pour 2025 et 2026. État postérieur calculé de manière causale.
Cible : depuis la clôture de t, attendre la bougie t+1 en entier, entrer à **open t+2**, sortir à **open t+3** (1 bougie tenue), aucune utilisation des prix t+1 dans la décision. Prédiction du rendement t+2 par mélange Student-t avec survie du régime sur 2 transitions ; P(x[t+2]>log(1.004)/scale)>=0.60 LONG, ou P(x[t+2]<-log(1.004)/scale)>=0.60 SHORT, sinon aucune entrée. Si les deux dépassent 0.60, aucun trade.
Frais+slippage hypothétiques **0.20% par aller-retour** ; stress **0.40%**. Buffer de 0.20% supplémentaire inclus dans le hurdle 40bp (ne pas le déduire deux fois des PNL). Funding réel non inclus; marge/venue/lot non certifiés.
Le coût par signal est calculé sans levier (rendement directionnel de notionnel), puis simulation de compte virtuel neuf 1000 USD, exposition **25% equity notionnel par entrée**, 4 positions maximum, aucune nouvelle entrée avant la sortie, classement stable alphabétique, PNL flottant à chaque clôture4h, zéro positions héritées, liquidation théorique à fin de période. Stress double friction et sensibilité notionnel ×2 déclarés séparément, pas sélectionnés.
Régime latéral causal : variation BTC sur 14 jours passés <= 5% à l'instant de décision. Témoin directionnel d'impulsion: signal LONG si x[t]>0 ou SHORT si x[t]<0, même attente et détention, mais uniquement aux timestamps où le BOCPD déclenche ; témoin complémentaire random same event calendar with mirrored sides (inverse). **Ces témoins ne prouvent pas la génération d'un alpha s'ils sont également perdants.**

## Décision prédéfinie
Retenir la famille pour étude de portefeuille exact uniquement si :
- en compte neuf 2025 et 2026 les résultats nets restent POSITIFS après 0.20% coûts;
- le compte 2026 est positif pendant les régimes BTC latéraux (résultat d'événements avec timing causal);
- le profit ne provient pas d'une seule crypto, et le résultat reste positif en coût stress 0.40%;
- n>=100 trades/an pour les 8 actifs et valeur d'espérance moyenne par événement > 0 net.
Si l'un des critères échoue, **rejeter la formule figée**, ne pas inverser le signal ni retoucher le seuil/horizon / choisir un autre univers après coup.

## Limites
La recherche BOCPD sur flux d'ordres (Tsaknaki/Lillo/Mazzarisi, Quantitative Finance 2025) a trouvé du pouvoir prédictif sur NASDAQ, **pas prouvé de profits crypto**; le lot104 adapte son modèle aux retours OHLC, ce n'est pas une reproduction exacte des méthodes financières ou microstructure. Une amélioration du score de prédiction n'est pas un rendement net. Aucun compte réel, aucun service/trade/R20 modifié.