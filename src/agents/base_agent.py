"""Base agent class for the AI Hedge Fund.

Provides a common interface and shared functionality for all trading agents
in the system, including state management, logging, and LLM integration.
"""

from abc import ABC, abstractmethod
from typing import Any

from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph

from src.state import AgentState
from src.utils.logging import setup_logger

logger = setup_logger(__name__)


class BaseAgent(ABC):
    """Abstract base class for all hedge fund agents.

    Each agent is responsible for a specific aspect of the trading pipeline,
    such as fundamental analysis, technical analysis, or risk management.
    """

    def __init__(self, name: str, model: Any, verbose: bool = False):
        """Initialize the base agent.

        Args:
            name: Human-readable name for this agent.
            model: The LLM model instance to use for inference.
            verbose: Whether to enable verbose logging output.
        """
        self.name = name
        self.model = model
        self.verbose = verbose
        self._graph: StateGraph | None = None

    @abstractmethod
    def analyze(self, state: AgentState) -> AgentState:
        """Perform analysis and update the agent state.

        Args:
            state: The current shared agent state.

        Returns:
            Updated agent state with this agent's analysis results.
        """
        pass

    def _invoke_llm(self, prompt: ChatPromptTemplate, **kwargs: Any) -> str:
        """Invoke the LLM with a formatted prompt.

        Args:
            prompt: The prompt template to use.
            **kwargs: Variables to format into the prompt.

        Returns:
            The LLM's text response.
        """
        chain = prompt | self.model
        response = chain.invoke(kwargs)

        if self.verbose:
            logger.debug(f"[{self.name}] LLM response: {response.content[:200]}...")

        return response.content

    def _add_message(self, state: AgentState, content: str) -> list:
        """Append a new human message to the state messages list.

        Args:
            state: The current agent state.
            content: The message content to add.

        Returns:
            Updated messages list.
        """
        messages = state.get("messages", [])
        messages.append(HumanMessage(content=content, name=self.name))
        return messages

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name!r})"
