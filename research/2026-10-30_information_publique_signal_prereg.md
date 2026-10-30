# PhilBot — Audit externe prospectif d'une source d'alpha informationnelle
30 octobre 2026 — **PROTOCOLE avant regroupement BTC, recherche uniquement**, R20 entièrement exclu, aucun bot live modifié.

Source: Sun/Wang/Zhang, Agentic AI Nowcasting and Cryptocurrency Return Predictability, SSRN 7231679 (2026). Scores 9300 crypto-signal-date du 29 avril au 30 juillet 2026, portefeuille publié sur GitHub auteur Moonooo24/agentic-ai-crypto-nowcasting. Les auteurs déclarent un scoring prospectif à 00:00 UTC. **Le public n'a pas les prompts, logs horodatés ni registres d'ordres, donc prospective et rentabilité réelle NON indépendamment certifiées.**

Hypothèse: un classement basé sur les informations publiques peut fournir un avantage LONG/SHORT indépendant des moteurs STC/AA dans les périodes BTC peu directionnelles.

Règles figées:
- Même 93 jours, même fichier public execution_portfolio_daily.csv, filtre strict delay_minutes=15 et portfolio=perpetual_long_short_after_funding_net_25bps. Valeurs déjà après funding estimé et coûts de 25 points de base **par jambe** selon la méthode des auteurs. Stress utiliser ligne net_50bps, sans autres adaptations.
- Pour un compte **1000 USD, gross1x et net0**, investir moitié notionnel sur LONG top10 et moitié notionnel SHORT bottom10; rendement journalier du compte = **0.5 × rendement long-short publié** (qui représente 100% LONG et 100% SHORT séparément; brut2x). Compte neuf, composition quotidienne, aucune position héritée, pas de cashflow. Ce calcul ne garantit pas qu'un vrai compte de 1000 puisse exécuter 20 ordres.
- Régime BTC connu à 00:00 UTC : BTCUSDT Binance USD-M 1h, abs(close de la dernière bougie terminée la veille 23h / close au même horaire 14 jours auparavant - 1)<=5%. Calculer ensuite résultats des jours classés plat et non plat, et stratégie cash les jours non plats. Aucun futur pour classifier.
- Test par mois fixé : 29 avril–31 mai, juin, 1–30 juillet, plus première moitié 46 jours / seconde 47 jours. n, rendement moyen, PF des retours quotidiens de panier, WR, capital final, DD en marques quotidiennes, pire jour et pire semaine. Vérifier corrélation au BTC quotidien.
- Période unique déjà publiée; pas de véritable historique 2024/2025 ni de prospectif vierge. Stop intrajournalier, slippage natif, marché disponible et financement revérifié manquent.

Gate prédéfini pour classer « piste à explorer prospectivement, NON bot live » : compte brut1x positif, sous-ensemble BTC plat moyenne nette positive et PF quotidien >=1.5 sous 25bp ET 50bp, et les trois mois calendaires nets positifs sous25bp. Échec = **pas de qualification de troisième moteur**; pas d'ajustement de seuils.

Sources: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7231679 , https://github.com/Moonooo24/agentic-ai-crypto-nowcasting . Source indépendante BTC déjà certifiée PhilBot archive publique 1h SHA256.
