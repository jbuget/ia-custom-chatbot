# IA Custom Chatbot API

API FastAPI s'appuyant sur un modèle Ollama local pour le chat et sur sentence-transformers pour les embeddings.

## Démarrage

```bash
cd server
python -m venv .venv
source .venv/bin/activate  # ou .venv\Scripts\activate sous Windows
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Configuration

Les variables d'environnement sont chargées automatiquement depuis `server/.env` (voir `server/.env.example`).

```bash
cp .env.example .env
# Puis ajuster les valeurs si nécessaire
```

## Endpoints

- `GET /api/v1/healthcheck` : vérification simple du service.
- `POST /api/v1/chat` : ajoute les messages fournis à une conversation et retourne la réponse générée par Ollama.
- `POST /api/v1/ask` : interprète la question, effectue une recherche vectorielle dans PostgreSQL (pgvector) et répond en citant les documents pertinents.

### Exemple de requête `/chat`

```json
{
  "conversation_id": null,
  "prompt": "Comment obtenir le rapport trimestriel ?"
}
```

La réponse contient l'`conversation_id` (généré si absent) et le message de l'assistant. Les conversations sont actuellement conservées en mémoire pour faciliter le passage à une persistance réelle.

## Configuration des modèles

- Chat : le service contacte `http://localhost:11434` par défaut avec le modèle `gpt-oss:20b` (Ollama).
- Embeddings : calculés localement avec `sentence-transformers` (`nomic-ai/nomic-embed-text-v2` par défaut).

Variables d'environnement principales :

- `OLLAMA_BASE_URL`
- `OLLAMA_MODEL`
- `OLLAMA_TIMEOUT_SECONDS`
- `DATABASE_URL`
- `EMBEDDING_MODEL`
- `EMBEDDING_DEVICE`
- `EMBEDDING_TRUST_REMOTE_CODE`
- `EMBEDDING_EXPECTED_DIMENSIONS`
- `RETRIEVER_TOP_K`
- `RETRIEVER_CONTEXT_CHAR_LIMIT`
- `CORS_ALLOW_ORIGINS`
- `CORS_ALLOW_METHODS`
- `CORS_ALLOW_HEADERS`
- `CORS_ALLOW_CREDENTIALS`

Assurez-vous que :

```bash
ollama run gpt-oss:20b --keepalive  # pour le chat
pip install -r requirements.txt      # installe aussi sentence-transformers
```
