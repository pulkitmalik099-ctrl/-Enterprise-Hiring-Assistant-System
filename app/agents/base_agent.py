from typing import Optional, Dict, Any
from abc import ABC, abstractmethod
from pydantic import BaseModel


class AgentResponse(BaseModel):
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class BaseAgent(ABC):
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    @abstractmethod
    async def execute(self, **kwargs) -> AgentResponse:
        pass

    async def validate_input(self, **kwargs) -> bool:
        return True

    async def process_output(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return data
