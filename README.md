# philbot-data

Donnees de chandelles (OHLC) multi-timeframes pour PhilBot.

Les archives ZIP sont publiees comme assets de release, pas dans le repo.
Voir l'onglet Releases : tag data-v1

Format : symbol,t,open,high,low,close (t = timestamp en ms UTC)
Contenu : un fichier csv.gz par actif + un manifest.json par ZIP
Source : export fetcher v1.1
