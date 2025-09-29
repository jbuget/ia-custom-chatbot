# IA Custom Chatbot – Guide Agents

Bienvenue ! Ce document résume l'état du projet afin que les agents IA puissent intervenir rapidement et de manière cohérente.

## Aperçu du projet
- **Frontend** : webapp Next.js (App Router) avec Tailwind et composant de chat.
- **Backend** : FastAPI interfaçant un modèle Ollama (`gpt-oss:20b`) via `/api/v1/chat`.
- Objectif : assistant conversationnel métier, connecté aux documents internes (future roadmap).

## Structure principale
```
/
├── web/                 # Frontend Next.js
│   ├── src/app/         # Pages App Router
│   ├── src/components/  # Composants UI (ChatInput, ChatConversation, ...)
│   └── src/lib/         # Utilitaires (requestChatResponse, etc.)
└── server/              # Backend FastAPI
    ├── app/main.py      # Entrée principale, routes API (v1)
    └── app/services/    # Services métier (Ollama, etc.)
```

## Flux actuel
1. La webapp envoie un prompt utilisateur via `requestChatResponse` (`web/src/lib/chat.ts`).
2. Le backend (`POST /api/v1/chat`) stocke la conversation en mémoire et interroge Ollama pour générer la réponse (Markdown).
3. Le frontend affiche la conversation (messages côté client) avec rendu Markdown.

## Commandes utiles
### Frontend
```bash
cd web
npm run dev      # Lancer Next.js
npm run lint     # Vérifier linting
```

### Backend
```bash
cd server
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Variables d'environnement
- Frontend : `NEXT_PUBLIC_API_BASE_URL` (voir `web/.env.example`).
- Backend : `OLLAMA_BASE_URL`, `OLLAMA_MODEL`, `OLLAMA_TIMEOUT_SECONDS`.

## Services externes
- **Ollama** : défaut `http://localhost:11434`, modèle `gpt-oss:20b`.
- Lancer le serveur avant `uvicorn` (`ollama run gpt-oss-20b --keepalive`).

## Conventions
- **Git** : commits conventionnels (type `feat:`, `refactor:`, etc.).
- **TypeScript/JS** : ESLint activé, préférez les `async/await`. Composants React majoritairement client-side.
- **Python** : Pydantic v2, FastAPI, privilégier la séparation service/logique.
- **CSS** : Tailwind en priorité.

## Roadmap (priorités futures)
1. Authentification et scoping utilisateur (conversation par user).
2. Persistance des conversations (DB/Postgres).
3. Intégration sources métiers (Notion, GDrive, etc.).
4. Passage à de vraies réponses IA côté backend.

## Bonnes pratiques / Rappels
- Préserver le design chat (brosse, bulles arrondies, bouton iconique).
- Appels API versionnés (`/api/v1`).
- Gérer les erreurs réseau côté front (messages d'erreur user-friendly).
- Documenter les nouveaux endpoints / modules (README + doc inline si besoin).

Bon travail !
