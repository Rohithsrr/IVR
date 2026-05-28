import uuid
from typing import Any


class ACSAdapter:
    async def start_call(self, from_number: str, to_number: str, callback_url: str) -> dict[str, Any]:
        raise NotImplementedError

    async def play_prompt(self, call_connection_id: str, text: str) -> dict[str, Any]:
        raise NotImplementedError

    async def collect_dtmf(self, call_connection_id: str, max_tones: int = 1) -> dict[str, Any]:
        raise NotImplementedError


class MockACSAdapter(ACSAdapter):
    async def start_call(self, from_number: str, to_number: str, callback_url: str) -> dict[str, Any]:
        return {"callConnectionId": f"mock-{uuid.uuid4()}", "status": "connected"}

    async def play_prompt(self, call_connection_id: str, text: str) -> dict[str, Any]:
        return {"callConnectionId": call_connection_id, "played": text}

    async def collect_dtmf(self, call_connection_id: str, max_tones: int = 1) -> dict[str, Any]:
        return {"callConnectionId": call_connection_id, "maxTones": max_tones, "status": "listening"}


class AzureACSAdapter(ACSAdapter):
    async def start_call(self, from_number: str, to_number: str, callback_url: str) -> dict[str, Any]:
        # Add Azure Communication Services Call Automation SDK invocation here.
        return {"callConnectionId": f"azure-stub-{uuid.uuid4()}", "status": "started"}

    async def play_prompt(self, call_connection_id: str, text: str) -> dict[str, Any]:
        # Add SDK call to play text prompt in live ACS call.
        return {"callConnectionId": call_connection_id, "played": text}

    async def collect_dtmf(self, call_connection_id: str, max_tones: int = 1) -> dict[str, Any]:
        # Add SDK call to start continuous DTMF recognition.
        return {"callConnectionId": call_connection_id, "status": "listening"}
