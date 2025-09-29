# IA Custom Chatbot API

API FastAPI minimale servant une réponse simulée pour préparer l'intégration avec la webapp Next.js.

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
- `POST /api/v1/chat` : ajoute les messages fournis à une conversation et retourne une réponse simulée de l'assistant.

### Exemple de requête `/chat`

```json
{
  "conversation_id": null,
  "prompt": "Comment obtenir le rapport trimestriel ?"
}
```

La réponse contient l'`conversation_id` (généré si absent) et le message de l'assistant. Les conversations sont actuellement conservées en mémoire pour faciliter le passage à une persistance réelle.
