# Modular IVR Platform MVP (React + Vite + FastAPI + ACS)

## Folder Tree
```text
frontend/
backend/
  app/
    api/
    core/
    integrations/
    ivr/
    models/
    schemas/
    services/
    utils/
  uploads/
README.md
```

## Setup
1. Backend
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --port 8000
```

2. Frontend
```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

## Run
- Backend: `http://localhost:8000`
- Frontend: `http://localhost:5173`
- API docs: `http://localhost:8000/docs`

## Features Delivered
- Login/register, dashboard, scenarios CRUD, call initiation, call history, analytics summary.
- Six seeded IVR scenarios: customer support, auth verification, notifications, lead qualification, emergency alert, AI receptionist.
- IVR engine with greeting/menu branching, fallback, escalation path fields, final outcomes.
- ACS integration layer with mock adapter (local) and Azure adapter stubs (production wiring point).
- Call webhook processing for DTMF and disconnected/end events.

## Testing Each IVR Scenario
1. Open frontend and login.
2. Go to Scenarios and confirm seeded scenarios.
3. Go to Calls and start call using selected Scenario ID.
4. Simulate webhook:
```bash
curl -X POST http://localhost:8000/api/calls/webhook -H 'Content-Type: application/json' -d '{"callConnectionId":"<mock-call-id>","eventType":"DtmfReceived","tone":"1"}'
```
5. Fetch call details:
```bash
curl http://localhost:8000/api/calls/<call_id>
```
6. Verify final outcomes in dashboard analytics and call logs.

## Real Azure Credentials Needed
Set these in `backend/.env`:
- `ACS_CONNECTION_STRING`
- `ACS_SOURCE_PHONE_NUMBER`
- `ACS_CALLBACK_BASE_URL` (public HTTPS URL for ACS webhooks)
- `ACS_USE_MOCK=false`

Then replace SDK stubs in `app/integrations/acs_adapter.py` with actual `azure-communication-callautomation` client calls.
