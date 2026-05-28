from datetime import datetime
from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class IVRStepIn(BaseModel):
    step_key: str
    prompt: str
    options_json: dict = {}
    fallback_key: str = ""
    transfer_target: str = ""
    final_outcome: str = ""


class ScenarioIn(BaseModel):
    name: str
    scenario_type: str
    description: str = ""
    is_active: bool = True
    steps: list[IVRStepIn]


class ScenarioOut(ScenarioIn):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class CallStart(BaseModel):
    scenario_id: int
    to_number: str
    from_number: str | None = None


class CallOut(BaseModel):
    id: int
    acs_call_connection_id: str
    scenario_id: int
    from_number: str
    to_number: str
    direction: str
    status: str
    current_step_key: str
    created_at: datetime

    class Config:
        from_attributes = True
