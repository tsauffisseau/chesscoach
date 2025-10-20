# ChessCoach — PGN Analyzer (Stockfish + Streamlit)

Analyse tes parties d'échecs à partir de fichiers **PGN** avec **Stockfish** et une interface **Streamlit** simple.
Le but : identifier les coups clés, les erreurs (blunders), et générer un tableau d’analyse lisible avec des graphes.

![Demo](docs/demo.gif) <!-- Remplace par ton GIF/capture -->

## ✨ Fonctionnalités
- Import d’un fichier **.pgn**
- Analyse par **Stockfish** (profondeur configurable)
- Scores et **meilleures lignes** suggérées
- Détection d’erreurs (blunder, mistake, inaccuracy)
- Export des résultats (CSV/Parquet)
- UI Streamlit prête à l’emploi

## 🚀 Démarrage rapide

### 1) Cloner le repo
```bash
git clone https://github.com/<ton-user>/<ton-repo>.git
cd <ton-repo>



# Option conda
conda env create -f environment.yml
conda activate chesscoach


# Option pip
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
python -m pip install -r requirements.txt


# Télécharger Stockfish

Télécharge le binaire Stockfish pour ton OS (ou utilise celui déjà installé).
Fournis le chemin via l’UI ou une variable d’environnement :

# Exemple :
export ENGINE_PATH="/chemin/vers/stockfish"
# Windows (PowerShell) :
# $env:ENGINE_PATH="C:\path\to\stockfish.exe"


# Lancer l'app

streamlit run ui/streamlit_app.py



# Architecture
.
├── src/chesscoach/
│   ├── analysis.py        # analyse PGN + moteur
│   ├── engine.py          # gestion Stockfish (open/close, depth, options)
│   ├── parsing.py         # utilitaires PGN
│   └── viz.py             # plots/figures
├── ui/
│   └── streamlit_app.py   # interface utilisateur
├── tests/                 # tests unitaires (pytest)
├── data/                  # (optionnel) échantillons .pgn
├── docs/                  # captures, GIFs, schémas
├── environment.yml
├── requirements.txt
└── README.md





# Configuration
Paramètres importants (exemples) :

ENGINE_PATH : chemin vers Stockfish

ANALYSIS_DEPTH : profondeur d’analyse (par défaut 12–18)

MULTIPV : nombre de meilleures lignes (1–3)

Tu peux les passer via :

Variables d’environnement

Fichier .streamlit/secrets.toml (ne pas versionner)

Widgets Streamlit (sidebar)



# Tests

pytest -q 



# Road Map
 Export PDF du rapport d’analyse

 Détection automatique des moments critiques

 Mode “coach” interactif coup-par-coup

 Hébergement Streamlit Cloud


#Contributions
Les contributions sont bienvenues !
Ouvre une issue / PR avec une description claire (repro steps, captures…).


# Remerciements

python-chess

Stockfish

Communauté open source ♟️