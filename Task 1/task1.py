from abc import ABC, abstractmethod 
from typing import List, Optional

class KnowledgeRetriever(ABC):
	"""Abstract base class."""
	
	@abstractmethod
	def retrieve(self, query: str) -> List[str]:
		"""Retrieve relevant knowledge based on the query."""

class VectorDatabaseRetriever(KnowledgeRetriever):
	"""Abstract of KnowledgeRetriever"""
	
	def retrieve(self, query: str) -> List[str]:
		print("Retrieving from Vector Database...")
		return ["answer1", "answer2"]

class SQLDatabaseRetriever(KnowledgeRetriever):
	"""Abstract of KnowledgeRetriever"""
	
	def retrieve(self, query: str) -> List[str]:
		print("Retrieving from SQL Database...")
		return ["answer3", "answer4"]

class QueryType():
	""" check the need of RAG"""

	def needs_rag(self, query: str) -> bool:
		
		keywords = ["info", "details", "id", "explain", "number"]
		if any(keyword in query.lower() for keyword in keywords):
			return True
		return False

class LLMservice():
	"""Abstract of LLMservice"""
	
	def generate_answer(self, query: str, context: Optional[List[str]] = None) -> str:
		if context:
			return f"Generated answer with context: {context}"
		return "Generated answer without context"	
	
class Response():
	"""Response to a customer query."""
	
	def __init__(self, answer: str, source: Optional[str] = None):
		self.answer = answer
		self.source = source

	def format(self):
		return f"This is your Answer: {self.answer}, Source: {self.source}"
	

class CustomerSupportAgent():
	"""Class representing a customer support agent."""
	
	def __init__(self, retriever: KnowledgeRetriever, query_type_checker: QueryType, llm_service: LLMservice):
		self.retriever = retriever
		self.query_type_checker = query_type_checker
		self.llm_service = llm_service
	
	def handle_query(self, query: str) -> Response:
		if self.query_type_checker.needs_rag(query):
			context = self.retriever.retrieve(query)
			answer = self.llm_service.generate_answer(query, context)
			source = type(self.retriever).__name__
		else:
			answer = self.llm_service.generate_answer(query)
			source = type(self.retriever).__name__
		return Response(answer, source)
		



if __name__ == "__main__":
	vector_retriever = VectorDatabaseRetriever()
	sql_retriever = SQLDatabaseRetriever()
	query_type_checker = QueryType()
	llm_service = LLMservice()
	print("This is a customer support agent module.")
	
	# vector-based RAG agent
	print("--- Vector-based RAG Agent ---")
	agent_vec = CustomerSupportAgent(vector_retriever, query_type_checker, llm_service)
	agent_vec_response = agent_vec.handle_query("explain my account id")
	print(agent_vec_response.format())

	# SQL-based RAG agent
	print("--- SQL-based RAG Agent ---")
	agent_sql = CustomerSupportAgent(sql_retriever, query_type_checker, llm_service)
	agent_sql_response = agent_sql.handle_query("what is the info today?")
	print(agent_sql_response.format())

	# Non-RAG agent
	print("--- Non-RAG Agent ---")
	agent_non_rag = CustomerSupportAgent(vector_retriever, query_type_checker, llm_service)
	agent_non_rag_response = agent_non_rag.handle_query("hello, how are you?")
	print(agent_non_rag_response.format())
