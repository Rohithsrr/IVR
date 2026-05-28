import json
from sqlalchemy.orm import Session
from app.models.models import IVRScenario, IVRStep
from app.schemas.schemas import ScenarioIn


def list_scenarios(db: Session):
    return db.query(IVRScenario).all()


def upsert_scenario(db: Session, data: ScenarioIn, scenario_id: int | None = None):
    scenario = db.query(IVRScenario).filter(IVRScenario.id == scenario_id).first() if scenario_id else IVRScenario()
    if not scenario:
        raise ValueError("Scenario not found")
    scenario.name, scenario.scenario_type, scenario.description, scenario.is_active = data.name, data.scenario_type, data.description, data.is_active
    db.add(scenario)
    db.flush()
    db.query(IVRStep).filter(IVRStep.scenario_id == scenario.id).delete()
    for step in data.steps:
        db.add(IVRStep(scenario_id=scenario.id, step_key=step.step_key, prompt=step.prompt, options_json=json.dumps(step.options_json), fallback_key=step.fallback_key, transfer_target=step.transfer_target, final_outcome=step.final_outcome))
    db.commit()
    db.refresh(scenario)
    return scenario
