# IA Custom Chatbot data management

## Services
- `docker-compose.yml` démarre PostgreSQL avec l'image `pgvector/pgvector`. L'initialisation de la base exécute automatiquement `init.sql` grâce au montage dans `docker-entrypoint-initdb.d`.

### Démarrer / arrêter la stack
- Lancer en arrière-plan : `docker compose -f data/docker-compose.yml up -d`
- Arrêter : `docker compose -f data/docker-compose.yml down`
- Réinitialiser entièrement (conteneur + volume) : `docker compose -f data/docker-compose.yml down -v`

## Schéma
- `init.sql` crée l'extension `vector`, la table `topics` et l'index IVFFlat sur la colonne `embedding`. La colonne `url` est unique afin d'empêcher les doublons.
- La colonne `embedding VECTOR(768)` est calibrée pour le modèle Ollama `nomic-embed-text` (API `/api/embeddings`).

## Chargement des données
- `load_topics_with_embeddings.py` importe les sujets du fichier `topics.json` vers la table `topics` et génère les embeddings via l'API embeddings d'Ollama.
  - Dépendance : `psycopg[binary]` (optionnellement `psycopg[pgvector]` pour un mapping natif des vecteurs).
  - Utilise la variable d'environnement `DATABASE_URL` (par défaut `postgresql://admin:password@localhost:5432/jbot`).
  - Réinitialise la table `topics` (TRUNCATE + RESTART IDENTITY) avant l'insertion.
  - Modèle d'embedding configurable avec `OLLAMA_EMBED_MODEL` (défaut `nomic-embed-text`). Vous pouvez fixer `EMBEDDING_DIM` pour forcer la taille attendue (sinon la première réponse fait foi, vérifiez qu'elle correspond à la définition de la colonne `embedding`).
  - Se base sur `data/topics.json`.

### Charger les données
- Vérifiez qu'Ollama est démarré et accessible (défaut `http://localhost:11434`).
- Facultatif : `export DATABASE_URL="postgresql://admin:password@localhost:5432/jbot"`
- Facultatif : `export OLLAMA_EMBED_MODEL="text-embedding-3-small"` (ou tout autre modèle disponible dans Ollama)
- Puis exécuter : `python data/load_topics_with_embeddings.py`
