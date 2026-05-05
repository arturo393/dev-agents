"""Base agent interface for all development agents."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, Optional
import logging

@dataclass
class AgentMessage:
    """Standard message format for agent communication."""
    id: str = field(default_factory=lambda: __import__('uuid').uuid4().hex)
    timestamp: str = field(default_factory=lambda: __import__('datetime').datetime.now().isoformat())
    source: str = ""
    destination: str = ""
    type: str = "request"  # request, response, event
    payload: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

class BaseAgent(ABC):
    """Abstract base class for all agents."""
    
    def __init__(self, name: str, config: Optional[Dict] = None):
        self.name = name
        self.config = config or {}
        self.logger = logging.getLogger(f"agent.{name}")
        self._health_status = "healthy"
    
    @abstractmethod
    async def run(self, input_data: Any) -> Any:
        """Main execution method for the agent."""
        pass
    
    def health_check(self) -> Dict[str, Any]:
        """Return health status of the agent."""
        return {
            "agent": self.name,
            "status": self._health_status,
            "timestamp": datetime.datetime.now().isoformat()
        }
    
    def setup(self) -> None:
        """Setup method called before running."""
        self.logger.info(f"Agent {self.name} setup complete")
    
    def teardown(self) -> None:
        """Cleanup method called after running."""
        self.logger.info(f"Agent {self.name} teardown complete")
