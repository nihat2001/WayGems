# Plan: Make AI Chat Knowledgeable About Baku

## Problem
AI can't answer queries like "library near Sahil metro" or understand Baku regions (Bayil, Sabail, Nasimi, etc.)

## Root causes
1. Random embeddings → vector search returns irrelevant results → LLM gets confused
2. Only 15 places in DB, no libraries or metro-adjacent spots
3. Prompts are generic, don't frame AI as Baku expert with local geography knowledge

## Changes (backend only, no UI)

### 1. `app/utils/prompts.py` — Add Baku Knowledge context
Inject a structured `BAKU_KNOWLEDGE` block with:

**METRO LINES** (Red + Green lines, all stations, key station notes)

**DISTRICTS (Rayons)** of Baku:
- Sabail (Səbail): Central-coastal district, includes Old City, Baku Boulevard, Government House, Port Baku, **Bayil neighborhood** (coastal area south of center, Bayil Castle ruins, BSU new campus)
- Nasimi (Nəsimi): Central district around 28 May metro, railway station, business hub
- Yasamal (Yasamal): Central-western residential area, local markets
- Nizami (Nizami): Central district, Nizami Street shopping area
- Narimanov (Nərimanov): Central, Gənclik metro area, Baku State University
- Khatai (Xətai): Eastern residential district
- Binagadi (Binəqədi): Northern residential
- Garadagh (Qaradağ): Southern industrial zone
- Khazar (Xəzər): Northern coast
- Sabunchu (Sabunçu): Northern district
- Surakhani (Suraxanı): Eastern district
- Neftchilar area: Southern industrial/oil region

**KEY LANDMARKS BY AREA** (with nearest metro and district)

Makes the AI understand queries like "library near Sahil" (National Library is in Sabail district, near Sahil metro) or "cafe in Bayil" (Bayil is a coastal neighborhood in Sabail district).

### 2. `app/seed/seed_data.py` — Expand places
Add ~15 more places spread across districts:
- National Library of Azerbaijan (Sabail, near Sahil metro)
- Azerbaijan Carpet Museum (Sabail, near Baku Boulevard)
- Baku Museum of Modern Art (Nasimi)
- Azerbaijan State Academic Opera and Ballet Theatre (Nasimi, near 28 May)
- Baku State University main campus (Narimanov, near Gənclik)
- More cafes, restaurants in different districts
- All use picsum.photos — no real images

### 3. `app/services/embedding_service.py` — Return None on fallback
Random embeddings silently pollute vector search. Change fallback from `_random_embedding` to returning `None` so upstream knows no real embedding is available.

### 4. `app/services/rag_service.py` — Handle None embedding
When `generate_embedding` returns `None`, skip vector search entirely and return empty results → triggers `_knowledge_response` with the enhanced Baku prompt.

## Files changed
- `app/utils/prompts.py` (rewrite all prompts with BAKU_KNOWLEDGE)
- `app/seed/seed_data.py` (add ~15 places to BAKU_PLACES)
- `app/services/embedding_service.py` (remove random fallback, return None)
- `app/services/rag_service.py` (add log message when skipping search)

## Not changed
- No frontend changes
- No PlacesPage changes
- No new UI elements
- No real image URLs needed

## How it works
Without Gemini API key: Vector search skipped → LLM answers from training + Baku context prompt → understands Bayil/Sabail/Nasimi naturally
With Gemini API key: Vector search works → precise DB matches + Baku context → even better
