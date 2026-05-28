import json
from sqlalchemy.orm import Session
from app.models.models import Call, CallEvent, CallResult, IVRStep


def get_step(db: Session, scenario_id: int, step_key: str) -> IVRStep | None:
    return db.query(IVRStep).filter(IVRStep.scenario_id == scenario_id, IVRStep.step_key == step_key).first()


def process_dtmf(db: Session, call: Call, tone: str) -> str:
    step = get_step(db, call.scenario_id, call.current_step_key)
    if not step:
        return "missing_step"
    options = json.loads(step.options_json or "{}")
    next_key = options.get(tone) or step.fallback_key
    if not next_key:
        return "fallback"
    next_step = get_step(db, call.scenario_id, next_key)
    if not next_step:
        return "invalid_branch"
    call.current_step_key = next_key
    if next_step.final_outcome:
        call.status = "completed"
        db.add(CallResult(call_id=call.id, outcome=next_step.final_outcome, notes=next_step.prompt))
    db.add(CallEvent(call_id=call.id, event_type="dtmf_processed", payload=json.dumps({"tone": tone, "next": next_key})))
    db.commit()
    return next_key
