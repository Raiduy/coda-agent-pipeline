from typing import Type, Dict, Any
import time
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.language_models import BaseChatModel
from pydantic import BaseModel
from src.graph.state import AgentState
from src.utils.logger import logger

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
        agent_name = self.__class__.__name__
        start_time = time.time()
        logger.info(f"🚀 Starting agent [{agent_name}]")
        
        # 1. Fetch the database instance from the shared graph state
        vector_store = state.get("vector_store")
        
        if vector_store is not None:
            logger.info(f"🔍 [{agent_name}] Querying Chroma DB with intent: '{self.query_intent}'")
            
            # 2. Invoke semantic vector search (retrieve the top 10 most relevant text chunks)
            db_start = time.time()
            retriever = vector_store.as_retriever(search_kwargs={"k": 10})
            retrieved_docs = retriever.invoke(self.query_intent)
            db_duration = time.time() - db_start
            
            logger.debug(f"⏱️  VectorDB retrieval for [{agent_name}] took {db_duration:.2f}s")
            
            # Combine retrieved text snippets into a single context block
            paper_context = "\n\n".join([doc.page_content for doc in retrieved_docs])
        else:
            logger.error(f"❌ [{agent_name}] NO CONTEXT AVAILABLE - No vector_store in state")
            paper_context = state.get("paper_context", "No context provided.")
        
        # 3. Invoke the chain with the targeted context
        llm_start = time.time()
        try:
            extracted_data = self.runnable.invoke({"context": paper_context})
        except Exception as e:
            logger.exception(f"💥 Error during LLM invocation for [{agent_name}]: {str(e)}")
            raise e
        llm_duration = time.time() - llm_start
        
        logger.debug(f"⏱️  LLM generation for [{agent_name}] took {llm_duration:.2f}s")
        
        total_duration = time.time() - start_time
        logger.info(f"✅ Agent [{agent_name}] completed in {total_duration:.2f}s")
        
        # 3. Return the payload to update LangGraph's State
        data_payload = extracted_data.model_dump() if isinstance(extracted_data, BaseModel) else extracted_data
        return {
            "extracted_features": [
                {
                    "agent_name": agent_name,
                    "data": data_payload
                }
            ]
        }
