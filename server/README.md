# IA Custom Chatbot API

API FastAPI s'appuyant sur un modèle Ollama local pour répondre à la webapp Next.js.

## Démarrage

```bash
cd server
python -m venv .venv
source .venv/bin/activate  # ou .venv\Scripts\activate sous Windows
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Endpoints

- `GET /healthcheck` : vérification simple du service.
- `POST /api/v1/chat` : ajoute les messages fournis à une conversation et retourne la réponse générée par Ollama.

### Exemple de requête `/chat`

```json
{
  "conversation_id": null,
  "prompt": "Comment obtenir le rapport trimestriel ?"
}
```

La réponse contient l'`conversation_id` (généré si absent) et le message de l'assistant. Les conversations sont actuellement conservées en mémoire pour faciliter le passage à une persistance réelle.

## Ollama

- Le service contacte `http://localhost:11434` par défaut avec le modèle `gpt-oss:20b`.
- Variables d'environnement disponibles :
  - `OLLAMA_BASE_URL`
  - `OLLAMA_MODEL`
  - `OLLAMA_TIMEOUT_SECONDS`
- Assurez-vous que le serveur Ollama est lancé avant `uvicorn`, par exemple :

```bash
ollama run gpt-oss:20b --keepalive
```
