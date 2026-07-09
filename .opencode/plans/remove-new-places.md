# Plan: Remove new places from PlacesPage

## Problem
15 new places were added to `seed_data.py` and they now appear as place cards on the main PlacesPage. The user doesn't want new places on the PlacesPage (only the AI should know about them via the prompt).

## Fix

### 1. `app/seed/seed_data.py`
Remove the 15 new place entries from `BAKU_PLACES`, restoring the list to the original 15 places only.

### 2. Rebuild & reseed
- `docker compose up -d --build app`
- Run seed to restore DB to original 15 places

## What stays
- The `BAKU_KNOWLEDGE` block in prompts (no UI impact, AI-only)
- The embedding/rag fixes (no UI impact)
- The AI chat history & persistence changes (no UI impact)
