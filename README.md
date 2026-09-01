# Recipe Finder API

A small REST API built with FastAPI for storing recipes and searching through
them by ingredient. Built this mainly to get more comfortable with FastAPI +
SQLAlchemy and to have something with real CRUD + tests + docs, instead of
another script that just runs once and prints stuff.

## What it does

- Create, read, update, and delete recipes
- Search recipes by ingredient (`GET /recipes/?ingredient=eggs`)
- Auto-generated interactive docs at `/docs` (this is genuinely one of my
  favorite things about FastAPI, you get this for free)
- Basic input validation — no negative prep times, no zero servings, etc.

## Tech

- FastAPI
- SQLAlchemy (SQLite for now, would swap this out for Postgres if this ever
  needed to run for real)
- Pydantic for request/response validation
- Pytest + httpx for tests

## Setup

```bash
git clone <your-repo-url>
cd recipe-api
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Running it

```bash
uvicorn app.main:app --reload
```

Then open `http://localhost:8000/docs` to try it out interactively, or hit
the endpoints directly:

```bash
curl -X POST http://localhost:8000/recipes/ \
  -H "Content-Type: application/json" \
  -d '{"title": "Pancakes", "ingredients": ["flour","eggs","milk"], "instructions": "Mix and fry.", "prep_minutes": 15, "servings": 2}'

curl "http://localhost:8000/recipes/?ingredient=eggs"
```

## Endpoints

| Method | Path            | Description                    |
|--------|-----------------|--------------------------------|
| POST   | /recipes/       | Create a recipe                |
| GET    | /recipes/       | List recipes (optional `?ingredient=`) |
| GET    | /recipes/{id}   | Get one recipe                 |
| PATCH  | /recipes/{id}   | Update one or more fields       |
| DELETE | /recipes/{id}   | Delete a recipe                |

## Tests

```bash
pytest tests/ -v
```

Tests run against a separate `test.db` (via a dependency override on
`get_db`), so they don't touch whatever's in your dev database, and the
tables get wiped between each test so nothing leaks across them.

## Things I'd add if I kept working on this

- Auth (right now anyone can hit any endpoint, fine for a portfolio project,
  not fine for anything real)
- Pagination metadata in the list response (total count, next page, etc.) —
  right now it's just `skip`/`limit` with no way to know how many are left
- Ingredients are stored as a comma-separated string under the hood, which
  works but a proper `ingredients` table with a many-to-many relationship
  would be the "correct" way to do this if the search needs to get smarter
  (e.g. matching partial words, plurals, etc.)

## License

MIT
