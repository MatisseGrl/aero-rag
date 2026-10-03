# Cahier des charges — aero-rag

RAG déployé sur la maintenance aéronautique : il répond à partir de documents publics, cite ses sources et refuse de répondre quand le corpus ne contient pas la réponse.

Dernière mise à jour : 3 octobre 2026.

## 1. Objectif

Montrer qu'un système RAG peut être livré en mode production-ready : tests, CI/CD, conteneur, déploiement cloud, évaluation chiffrée. Le but n'est pas d'aller vite, c'est de pouvoir tout expliquer sans aide.

Fil rouge : un système peut donner une réponse qui a l'air propre et qui est fausse, sans qu'on s'en rende compte. L'évaluation (questions sans réponse, abstention) doit donc être réelle et chiffrée.

## 2. Périmètre

- Dans le périmètre : le RAG seul (ingestion, découpage, embeddings, index, retrieval, génération, API, évaluation, CI/CD, déploiement).
- Hors périmètre pour l'instant : orchestrateur, agents, tool RUL de C-MAPSS, Kubernetes.
- Le RAG est un module Python séparé de l'API (`pipeline.answer(question)`), pour pouvoir le brancher plus tard comme tool sans le réécrire.

## 3. Corpus

- 20 à 40 documents publics : FAA, EASA, NASA NTRS.
- PDF à texte natif, en anglais.
- Liste dans `corpus/SOURCES.md` (titre, éditeur, URL, date de téléchargement).
- À trancher : les 5 premiers documents à tester pour l'extraction du texte.

## 4. Pipeline

1. Extraction du texte (par page, pour pouvoir citer la page).
2. Découpage en passages.
3. Embeddings.
4. Index stocké en fichiers.
5. Retriever (top-k).
6. Générateur (LLM, réponse avec citations).

## 5. API (FastAPI)

| Route | Rôle | Réponse |
|---|---|---|
| `GET /health` | Santé du service (health check du déploiement) | `{"status": "ok"}` |
| `POST /ask` | Pose une question au RAG | `answer`, `answered`, `sources` (document, page, extrait) |

## 6. Abstention

Le système refuse de répondre quand le corpus n'a pas la réponse :

- un seuil de similarité sur le retrieval ;
- une consigne dans le prompt ;
- réglage sur 3 questions hors corpus.

## 7. Évaluation

10 questions :

- 7 avec réponse (document et page attendus) ;
- 3 sans réponse dans le corpus.

Mesures : Hit@k, réponse correcte, abstention.

## 8. Qualité et CI/CD

- Tests d'abord (pytest) : le test s'écrit avant le code et on le voit échouer. Premier test : `GET /health`.
- Lint : ruff.
- GitHub Actions : ruff, pytest, build Docker. Seul le Hit@k tourne en CI, car il n'a pas besoin de clé API.
- Git : une branche par fonctionnalité, une PR même seul, merge uniquement quand la CI est verte.

## 9. Déploiement

- Image Docker poussée dans ECR.
- Service AWS App Runner, `/health` en health check.
- Google Cloud Run seulement s'il reste du temps.
- Secrets : variables d'environnement ou AWS Secrets Manager. Jamais dans le repo (`.env` dans `.gitignore`, `.env.example` commité).

## 10. Structure du repo

```
aero-rag/
├── src/
│   ├── rag/          # ingest, chunking, retriever, generator, pipeline
│   └── api/main.py
├── tests/
├── eval/
├── corpus/           # SOURCES.md + documents
├── docs/
├── Dockerfile
├── .github/workflows/ci.yml
├── pyproject.toml
├── AGENTS.md
├── CLAUDE.md
└── README.md
```

## 11. Choix ouverts (à trancher avant de coder la partie concernée)

| Sujet | Options | Remarque |
|---|---|---|
| LLM | API directe ou Bedrock | API directe plus simple pour commencer ; Bedrock colle à AWS, pas de clé à gérer, accès au modèle à activer |
| Embeddings | Modèle local léger | Gratuit, mais alourdit l'image Docker : vérifier la taille avant de choisir |
| Index | FAISS ou Chroma | |
| Budget | Plafond de dépense AWS et API | À fixer avant le premier déploiement |

## 12. Plan de travail (≈ 15 h)

| # | Étape | Durée |
|---|---|---|
| 1 | Repo, `/health`, premier test, Dockerfile, CI | 3 h |
| 2 | Ingestion et découpage, avec tests | 2 h |
| 3 | Embeddings, index, retrieval, Hit@k | 2 h |
| 4 | Génération avec citations et abstention | 2 h |
| 5 | Route `/ask` et tests de l'API | 1,5 h |
| 6 | Évaluation des 10 questions, chiffres | 1,5 h |
| 7 | Déploiement AWS | 2 h |
| 8 | README, schéma d'architecture, déploiement automatique sur `main` | 1,5 h |

Si le temps manque : on coupe Google Cloud Run et le déploiement automatique. On ne coupe jamais les tests ni la CI.

## 13. Critère de réussite : ce que je dois pouvoir expliquer sans aide

- pourquoi ce découpage et cette valeur de k ;
- ce que fait l'abstention et comment elle a été réglée ;
- ce que fait chaque étape de la CI ;
- un bug trouvé et corrigé à la main ;
- un cas où le RAG s'est trompé avec une réponse qui avait l'air correcte.
