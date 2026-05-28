import json
from sqlalchemy.orm import Session
from app.core.config import settings
from app.integrations.acs_adapter import AzureACSAdapter, MockACSAdapter
from app.ivr.engine import get_step, process_dtmf
from app.models.models import Call, CallEvent, CallResult

adapter = MockACSAdapter() if settings.acs_use_mock or not settings.acs_connection_string else AzureACSAdapter()


async def start_call(db: Session, scenario_id: int, to_number: str, from_number: str | None):
    source = from_number or settings.acs_source_phone_number
    cb = f"{settings.acs_callback_base_url}/api/calls/webhook"
    acs = await adapter.start_call(source, to_number, cb)
    call = Call(acs_call_connection_id=acs["callConnectionId"], scenario_id=scenario_id, from_number=source, to_number=to_number, direction="outbound", status="initiated", current_step_key="greeting")
    db.add(call)
    db.commit()
    db.refresh(call)
    step = get_step(db, scenario_id, "greeting")
    if step:
        await adapter.play_prompt(call.acs_call_connection_id, step.prompt)
        await adapter.collect_dtmf(call.acs_call_connection_id)
    return call


def handle_webhook(db: Session, payload: dict):
    call_id = payload.get("callConnectionId")
    event_type = payload.get("eventType", "unknown")
    call = db.query(Call).filter(Call.acs_call_connection_id == call_id).first()
    if not call:
        return {"message": "call not found"}
    db.add(CallEvent(call_id=call.id, event_type=event_type, payload=json.dumps(payload)))
    if event_type == "DtmfReceived":
        tone = payload.get("tone", "")
        process_dtmf(db, call, tone)
    elif event_type in ["CallDisconnected", "CallEnded"]:
        call.status = "ended"
        if not db.query(CallResult).filter(CallResult.call_id == call.id).first():
            db.add(CallResult(call_id=call.id, outcome="ended", notes="Call ended before final node"))
        db.commit()
    else:
        db.commit()
    return {"message": "processed"}
