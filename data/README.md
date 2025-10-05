# IA Custom Chatbot data management

## Services
- `docker-compose.yml` démarre PostgreSQL avec l'image `pgvector/pgvector`. L'initialisation de la base exécute automatiquement `init.sql` grâce au montage dans `docker-entrypoint-initdb.d`.

### Démarrer / arrêter la stack
- Lancer en arrière-plan : `docker compose -f data/docker-compose.yml up -d`
- Arrêter : `docker compose -f data/docker-compose.yml down`
- Réinitialiser entièrement (conteneur + volume) : `docker compose -f data/docker-compose.yml down -v`

## Schéma
- `init.sql` crée l'extension `vector`, la table `topics` et l'index IVFFlat sur la colonne `embedding`. La colonne `url` est unique afin d'empêcher les doublons.
- La colonne `embedding VECTOR(768)` est calibrée pour le modèle `nomic-ai/nomic-embed-text-v2` (768 dimensions).

## Chargement des données
- `load_topics_with_embeddings.py` importe les sujets du fichier `topics.json` vers la table `topics` et génère les embeddings localement grâce à [sentence-transformers](https://www.sbert.net/).
  - Dépendances : `psycopg[binary]` (optionnellement `psycopg[pgvector]`), `sentence-transformers`, `einops`.
  - Utilise la variable d'environnement `DATABASE_URL` (par défaut `postgresql://admin:password@localhost:5432/jbot`).
  - Réinitialise la table `topics` (TRUNCATE + RESTART IDENTITY) avant l'insertion.
  - Modèle d'embedding configurable via `EMBEDDING_MODEL` (défaut `nomic-ai/nomic-embed-text-v2`). Vous pouvez fixer `EMBEDDING_EXPECTED_DIMENSIONS` pour forcer la taille attendue (sinon la première réponse fait foi, vérifiez qu'elle correspond à la définition de la colonne `embedding`).
  - `EMBEDDING_DEVICE` permet de choisir le périphérique (`cpu`, `cuda`, etc.).
  - `EMBEDDING_TRUST_REMOTE_CODE` (`false` par défaut) autorise le chargement de modèles nécessitant du code custom (par ex. certains modèles HF comme `nomic-bert-2048`).
  - Se base sur `data/topics.json`.
  - Remarque : `topics.json` regroupe des fiches issues du site *La Communauté de l'inclusion*, un forum destiné aux professionnels de l'insertion socio-professionnelle en France. Ce corpus métier, riche en vocabulaire spécialisé, est idéal pour illustrer des cas de recherche sémantique assistée par IA.

### Charger les données
- Installez les dépendances Python requises (`psycopg`, `sentence-transformers`, `einops`).
- Facultatif : `export DATABASE_URL="postgresql://admin:password@localhost:5432/jbot"`
- Facultatif : `export EMBEDDING_MODEL="nomic-ai/nomic-embed-text-v2"`
- Facultatif : `export EMBEDDING_DEVICE="cuda"` (si vous disposez d'un GPU)
- Facultatif : `export EMBEDDING_TRUST_REMOTE_CODE="true"` (pour les modèles nécessitant du code custom)
- Puis exécuter : `python data/load_topics_with_embeddings.py`
