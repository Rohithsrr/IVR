from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.models import Call, CallEvent, CallResult, IVRScenario
from app.schemas.schemas import CallStart, ScenarioIn, Token, UserCreate, UserLogin
from app.services.auth_service import login_user, register_user
from app.services.call_service import handle_webhook, start_call
from app.services.scenario_service import list_scenarios, upsert_scenario

router = APIRouter(prefix="/api")


@router.post("/auth/register")
def register(payload: UserCreate, db: Session = Depends(get_db)):
    try:
        user = register_user(db, payload)
        return {"id": user.id, "email": user.email}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/auth/login", response_model=Token)
def login(payload: UserLogin, db: Session = Depends(get_db)):
    try:
        token = login_user(db, payload.email, payload.password)
        return {"access_token": token}
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))


@router.get("/scenarios")
def get_scenarios(db: Session = Depends(get_db)):
    return list_scenarios(db)


@router.post("/scenarios")
def create_scenario(payload: ScenarioIn, db: Session = Depends(get_db)):
    return upsert_scenario(db, payload)


@router.put("/scenarios/{scenario_id}")
def update_scenario(scenario_id: int, payload: ScenarioIn, db: Session = Depends(get_db)):
    return upsert_scenario(db, payload, scenario_id)


@router.delete("/scenarios/{scenario_id}")
def delete_scenario(scenario_id: int, db: Session = Depends(get_db)):
    s = db.query(IVRScenario).filter(IVRScenario.id == scenario_id).first()
    if not s:
        raise HTTPException(404, "Scenario not found")
    db.delete(s)
    db.commit()
    return {"deleted": True}


@router.post("/calls/start")
async def start(payload: CallStart, db: Session = Depends(get_db)):
    return await start_call(db, payload.scenario_id, payload.to_number, payload.from_number)


@router.post("/calls/incoming")
def incoming(payload: dict):
    return {"message": "Inbound call received", "payload": payload}


@router.post("/calls/webhook")
def webhook(payload: dict, db: Session = Depends(get_db)):
    return handle_webhook(db, payload)


@router.get("/calls")
def get_calls(db: Session = Depends(get_db)):
    return db.query(Call).all()


@router.get("/calls/{call_id}")
def get_call(call_id: int, db: Session = Depends(get_db)):
    c = db.query(Call).filter(Call.id == call_id).first()
    if not c:
        raise HTTPException(404, "Call not found")
    events = db.query(CallEvent).filter(CallEvent.call_id == call_id).all()
    result = db.query(CallResult).filter(CallResult.call_id == call_id).first()
    return {"call": c, "events": events, "result": result}


@router.get("/analytics/summary")
def analytics(db: Session = Depends(get_db)):
    total = db.query(Call).count()
    completed = db.query(Call).filter(Call.status == "completed").count()
    ended = db.query(Call).filter(Call.status == "ended").count()
    return {"total_calls": total, "completed_calls": completed, "ended_calls": ended, "completion_rate": (completed / total * 100) if total else 0}
