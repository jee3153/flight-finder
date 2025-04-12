# ✈️ FastAPI Flight Finder

A deployable FastAPI backend that finds the cheapest flight route (with stops, cost filters, and more).

### 🚀 How to Run

```bash
uvicorn app.main:app --reload
```

Alternatively,
```bash
docker build -t fastapi-flight .
docker run -p 8000:8000 fastapi-flight
```

API Endpoints to try:
- GET /cheapest-flight?from=US&to=DE
- POST /add-flight
- GET /routes?from=UK
- GET /flights/from?from=US