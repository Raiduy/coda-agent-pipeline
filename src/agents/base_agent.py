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
        output_schema: Type[BaseModel],
        query_intent: str
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
        self.query_intent = query_intent
        
        # Build the standard prompt template
        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", self.system_prompt),
            ("human", "Analyze the provided research paper context and extract the required features.\n\nContext:\n{context}")
        ])
        
        # Bind the schema to the LLM so it forces structured JSON output
        self.runnable = self.prompt_template | self.llm.with_structured_output(self.output_schema)

    def __call__(self, state: AgentState) -> Dict[str, Any]:
        """
        Dynamically fetches targeted RAG context from the state database,
        runs the execution chain, and appends the features to the global graph state.
        """
        # 1. Fetch the database instance from the shared graph state
        vector_store = state.get("vector_store")
        
        if vector_store is not None:
            print(f"🔍 [{self.__class__.__name__}] Querying Chroma DB with intent: '{self.query_intent}'")
            
            # 2. Invoke semantic vector search (retrieve the top 3 most relevant text chunks)
            retriever = vector_store.as_retriever(search_kwargs={"k": 10})
            retrieved_docs = retriever.invoke(self.query_intent)
            
            # Combine retrieved text snippets into a single context block
            paper_context = "\n\n".join([doc.page_content for doc in retrieved_docs])
        else:
            # Fallback if testing infrastructure passes a plain string directly
            print('\n*******ERROR, NO CONTEXT AVAILABLE********')
            paper_context = state.get("paper_context", "No context provided.")
        
        # 3. Invoke the chain with the targeted context
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
