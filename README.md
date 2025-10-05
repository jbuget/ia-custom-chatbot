# IA Custom Chatbot

Plateforme en cours de développement pour un assistant conversationnel métier.

## Architecture
- **web/** : frontend Next.js (App Router) avec une interface de chat.
- **server/** : backend FastAPI exposant des endpoints versionnés (`/api/v1`), connecté à Ollama pour le chat et à sentence-transformers pour les embeddings.

## Prérequis rapides
- Node.js 20+
- Python 3.10+

## Démarrage Frontend
```bash
cd web
npm install
npm run dev
```

## Démarrage Backend
```bash
cd server
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

> ℹ️ Assurez-vous que votre serveur Ollama (modèle `gpt-oss:20b` par défaut) tourne sur `http://localhost:11434` ou ajustez `OLLAMA_BASE_URL`.
> Installez également les dépendances Python qui incluent `sentence-transformers` pour la génération d'embeddings locale (`pip install -r requirements.txt`).

## Variables d'environnement

**Frontend:**
- `NEXT_PUBLIC_API_BASE_URL` (web) : URL de base de l'API (défaut `http://localhost:8000`).

**Backend:**
- copier `server/.env.example` vers `server/.env` pour configurer Ollama et CORS (`OLLAMA_BASE_URL`, `OLLAMA_MODEL`, etc.).

## Documentation
- `AGENTS_GUIDE.md` : brief pour les agents IA et nouveaux contributeurs.
- `server/README.md` : détails spécifiques à l'API.
- `web/README.md` : notes propres au frontend.

## Roadmap (extraits)
1. Authentification utilisateur & persistance des conversations.
2. Intégration de sources documentaires internes (Notion, Google Drive, etc.).
3. Passage d'une réponse simulée à une véritable génération IA.
