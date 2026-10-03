# STATUS — aero-rag

Source de vérité sur l'avancement. À lire au début de chaque session, à mettre à jour à la fin.

Dernière mise à jour : 3 octobre 2026 (fin de la session 1).

## Étape en cours

Étape 1 du plan (repo, `/health`, premier test, Dockerfile, CI). Voir `docs/cahier-des-charges.md`, section 12.

## Fait

- [x] Repo cloné, `.gitignore` OK (`.env`, `.venv`)
- [x] Docs : cahier des charges, `AGENTS.md`, `CLAUDE.md`, `STATUS.md` (PR #1 mergée)
- [x] Venv `uv`, Python 3.12
- [x] `pyproject.toml` (fastapi, httpx ; dev : pytest, ruff) + `uv.lock`
- [x] Premier test `tests/test_health.py` vu échouer, puis `GET /health` dans `src/api/main.py` (PR #2 mergée)

## À faire ensuite

- [ ] Dockerfile (session à part)
- [ ] CI GitHub Actions : écrite par Matisse, relue par l'agent (session à part)

## Décisions

- Python 3.12 (pas 3.14) : meilleure compatibilité des libs d'embeddings/FAISS à venir.
- Repo hors OneDrive : `C:\Users\mgarl\Documents\aero-rag`.
- Boilerplate (routes triviales, config) : l'agent écrit vite. Cœur du RAG (découpage, retrieval, abstention, éval) : Matisse doit comprendre et expliquer chaque choix.

## Questions ouvertes

LLM (API directe ou Bedrock), embeddings (taille image Docker), index (FAISS ou Chroma), budget AWS/API, 5 premiers documents du corpus.

## Notes

- Warning pytest : `StarletteDeprecationWarning` sur `httpx` (suggère `httpx2`). Non bloquant, à regarder plus tard.
