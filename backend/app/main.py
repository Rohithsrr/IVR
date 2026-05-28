from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router
from app.core.config import settings
from app.core.database import Base, engine, SessionLocal
from app.models.models import IVRScenario
from app.services.scenario_service import upsert_scenario
from app.schemas.schemas import ScenarioIn, IVRStepIn

app = FastAPI(title=settings.app_name)
app.add_middleware(CORSMiddleware, allow_origins=[o.strip() for o in settings.cors_origins.split(',')], allow_methods=["*"], allow_headers=["*"], allow_credentials=True)
app.include_router(router)
Base.metadata.create_all(bind=engine)


@app.on_event("startup")
def seed():
    db = SessionLocal()
    if db.query(IVRScenario).count() == 0:
        types = ["customer_support", "auth_verification", "notifications", "lead_qualification", "emergency_alert", "ai_receptionist"]
        for t in types:
            upsert_scenario(db, ScenarioIn(name=t.replace('_',' ').title(), scenario_type=t, description=f"Default {t}", steps=[IVRStepIn(step_key="greeting", prompt="Welcome. Press 1 for sales, 2 for support.", options_json={"1": "sales", "2": "support"}, fallback_key="fallback"), IVRStepIn(step_key="sales", prompt="Routing to sales.", final_outcome="sales_routed"), IVRStepIn(step_key="support", prompt="Routing to support.", final_outcome="support_routed"), IVRStepIn(step_key="fallback", prompt="Invalid entry. Goodbye.", final_outcome="invalid_input")]))
    db.close()


@app.get("/")
def root():
    return {"status": "ok", "name": settings.app_name}
