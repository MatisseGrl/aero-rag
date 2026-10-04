# STATUS — aero-rag

Source de vérité sur l'avancement. À lire au début de chaque session, à mettre à jour à la fin.

Dernière mise à jour : 4 octobre 2026 (fin de la session 2).

## Étape en cours

Ingestion du corpus (extraction du texte des PDF, page par page). Branche `feat/ingest` : code et tests faits, PR pas encore ouverte/mergée. Voir `docs/cahier-des-charges.md`, section 12.

## Fait

- [x] Session 1 : repo, docs, venv `uv`, `pyproject.toml`, `GET /health` + premier test (PR #1 à #3 mergées)
- [x] 5 premiers documents du corpus choisis et téléchargés dans `corpus/` (3 EASA SIB, 1 FAA AC, 1 NASA NTRS), avec `corpus/SOURCES.md` (URL, date). Tous en texte natif.
- [x] `pypdf` ajouté
- [x] `src/rag/ingest.py` : `ingest_pdf(path)` renvoie une liste de `{document, page, text}`, pages numérotées à partir de 1
- [x] Tests `tests/test_ingest.py` (4 tests, vus échouer avant le code) + fixture `two_page_pdf` dans `tests/conftest.py` (PDF de test généré à la main)
- [x] Vérifié sur les 5 vrais PDF : 6, 2, 3, 13 et 48 pages, aucune page vide
- [x] Testé à la main : `start=0` casse `test_ingest_numbers_pages_from_one` (le test attrape bien le décalage de numérotation)

## À faire ensuite

- [ ] Ouvrir la PR de `feat/ingest` et la merger quand les tests passent (pas de CI pour l'instant)
- [ ] Dockerfile (session à part)
- [ ] CI GitHub Actions : écrite par Matisse, relue par l'agent (session à part)
- [ ] Étapes suivantes du RAG (découpage, embeddings, retrieval) : à planifier d'après le cahier des charges, pas encore commencées

## Décisions

- Python 3.12 (pas 3.14) : meilleure compatibilité des libs d'embeddings/FAISS à venir.
- Repo hors OneDrive : `C:\Users\mgarl\Documents\aero-rag`.
- Boilerplate (routes triviales, config) : l'agent écrit vite. Cœur du RAG (découpage, retrieval, abstention, éval) : Matisse doit comprendre et expliquer chaque choix.
- Extraction PDF : `pypdf` (léger, simple). Alternative à comparer si la qualité du texte pose problème : `pymupdf` (plus rapide et précis, plus lourd, licence AGPL).
- Numérotation des pages à partir de 1 dans `ingest_pdf`, pour que les citations correspondent à ce qu'on voit dans un lecteur PDF.
- Les PDF du corpus sont commités (1,5 Mo au total).

## Questions ouvertes

LLM (API directe ou Bedrock), embeddings (taille image Docker), index (FAISS ou Chroma), budget AWS/API.

À vérifier : licence de réutilisation des documents EASA.

## Notes

- Warning pytest : `StarletteDeprecationWarning` sur `httpx` (suggère `httpx2`). Non bloquant, à regarder plus tard.
- `pypdf` sort du texte avec beaucoup de `\n` et d'espaces en trop. À traiter au moment du découpage, pas dans `ingest_pdf`.
- `pypdf` affiche des messages "Ignoring wrong pointing object" sur certains PDF (FAA ou NASA). Sans effet sur l'extraction.
- `file` annonçait 2 pages pour `easa_sib_2008-37.pdf`, `pypdf` en compte 6. À recouper avec un lecteur PDF.
- Matisse débute en Python : expliquer le code avec des exemples concrets et peu de jargon. Une session d'explications peut remplacer l'écriture du code par lui quand il bloque.
