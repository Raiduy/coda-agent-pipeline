from typing import Type, Dict, Any
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.language_models import BaseChatModel
from pydantic import BaseModel
from src.graph.state import AgentState

class BaseAgent:
    def __init__(
        self, 
        llm: BaseChatModel, 
        system_prompt: str, 
        output_schema: Type[BaseModel]
    ):
        """
        Args:
            llm: The LangChain ChatModel instance (e.g., ChatOpenAI, ChatAnthropic).
            system_prompt: The specific instructions for this agent.
            output_schema: The Pydantic class this agent MUST respond with.
        """
        self.llm = llm
        self.system_prompt = system_prompt
        self.output_schema = output_schema
        
        # Build the standard prompt template
        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", self.system_prompt),
            ("human", "Analyze the provided research paper context and extract the required features.\n\nContext:\n{context}")
        ])
        
        # Bind the schema to the LLM so it forces structured JSON output
        self.runnable = self.prompt_template | self.llm.with_structured_output(self.output_schema)

    def __call__(self, state: AgentState) -> Dict[str, Any]:
        """
        This makes the class callable as a standard LangGraph node function.
        It reads from the global state, processes data, and returns the update.
        """
        # 1. Fetch the RAG context from the state (simulated here)
        # In a full setup, you'd pull state["vector_store_id"] and query it here
        paper_context = state.get("paper_context", "No context provided.")
        
        # 2. Invoke the chain
        extracted_data = self.runnable.invoke({"context": paper_context})
        
        # 3. Return the payload to update LangGraph's State
        # Because 'extracted_features' uses operator.add in our state, 
        # this dict will be cleanly appended to the list automatically!
        return {
            "extracted_features": [
                {
                    "agent_name": self.__class__.__name__,
                    "data": extracted_data.model_dump()
                }
            ]
        }
