# Hackathon Tasks API

Small FastAPI service used by the sibling `hackathon-client` repository.

## Run

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

The API runs at `http://localhost:8000` by default.

## Endpoints

- `GET /health`
- `GET /api/tasks`
- `GET /api/tasks/summary`
- `POST /api/tasks`
- `PATCH /api/tasks/{task_id}`
- `DELETE /api/tasks/{task_id}`
