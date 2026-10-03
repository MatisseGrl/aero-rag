# aero-rag — instructions pour les agents

RAG sur la maintenance aéronautique (docs publics FAA, EASA, NASA NTRS). Il cite ses sources (document, page) et refuse de répondre quand le corpus n'a pas la réponse. Spec complète : `docs/cahier-des-charges.md`.

L'objectif n'est pas d'aller vite : Matisse (ING4 Data & IA) doit pouvoir tout expliquer en entretien et à un lab du MIT. Quand il y a un conflit entre aller vite et comprendre, on comprend.

## Langue et ton

- Matisse parle français, familier. Réponds en français, même registre, sans formalisme.
- Direct et honnête : si une idée est mauvaise, dis-le et explique pourquoi.
- Réponds à la question posée. Pas de conseil non demandé, pas de listes de ressources sans raison.
- Code, commentaires, messages de commit : en anglais.

## Périmètre

Le RAG seul. Pas d'agents, pas d'orchestrateur, pas de tool RUL, pas de Kubernetes. Si Matisse en parle, rappelle que le RAG passe d'abord.

## Stack

Python, FastAPI, pytest, ruff, httpx, uv, Docker, GitHub Actions, déploiement AWS (App Runner + ECR) plus tard.

## Structure

```
src/rag/        ingest, chunking, retriever, generator, pipeline
src/api/main.py GET /health, POST /ask
tests/
eval/
corpus/         SOURCES.md + documents
Dockerfile
.github/workflows/ci.yml
pyproject.toml
```

`pipeline.answer(question)` reste un module Python séparé de l'API.

## Commandes

À compléter au fur et à mesure que le projet existe (ne pas inventer de commande qui ne tourne pas encore) :

```bash
uv venv                      # créer le venv
uv run pytest                # tests
uv run ruff check .          # lint
```

## Règles de travail (non négociables)

1. **Tests d'abord.** Le test s'écrit avant le code et Matisse doit le voir échouer. Premier test : `GET /health`.
2. **Pas de CI/CD écrite par l'agent.** Matisse écrit le workflow. L'agent explique ce que fait chaque étape, relit le fichier et signale les erreurs, sans le rédiger à sa place. Pareil pour le Dockerfile quand son tour vient, sauf si Matisse demande autrement.
3. **Débogage à la main.** Quand un test casse, Matisse lit l'erreur et cherche. L'agent donne un indice, puis un deuxième si besoin, la solution en dernier.
4. **Human in the loop.** Avant de passer au bloc suivant, demander à Matisse d'expliquer ce que fait le code proposé.
5. **Relire comme un reviewer.** Sur chaque diff : oublis réels, secret dans le repo, test qui ne teste rien, `random_state` manquant, etc.
6. **Git propre.** Une branche par fonctionnalité, une PR même seul, merge seulement quand la CI est verte. Pas de commit direct sur `main`. L'agent ne commit et ne push que si Matisse le demande.
7. **Une seule tâche par session.** Ne pas proposer de passer à la suite.
8. **Aucun secret dans le repo.** `.env` dans `.gitignore`, `.env.example` commité. Clés via variables d'environnement ou AWS Secrets Manager.

## Décisions encore ouvertes

À trancher avec Matisse avant de coder la partie concernée, ne pas décider à sa place : LLM (API directe ou Bedrock), modèle d'embeddings (vérifier la taille de l'image Docker), index (FAISS ou Chroma), budget AWS/API, 5 premiers documents du corpus.
