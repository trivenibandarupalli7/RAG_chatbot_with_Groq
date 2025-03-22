from app.groq_client import GroqClient
from app.utils import preprocess_pdf
from duckduckgo_search import DDGS  # Updated import
import json
import os

class RAGProcessor:
    def __init__(self):
        self.groq = GroqClient()
        self.search_api = os.getenv("SEARCH_API", "duckduckgo")

    def decompose_query(self, query: str) -> list:
        prompt = f"""Analyze this query and decompose it into sub-questions or information needs:
        Query: {query}
        Provide the decomposition as a JSON array of strings."""
        
        response = self.groq.chat(
            model="mixtral-8x7b-32768",
            messages=[{"role": "user", "content": prompt}]
        )
        return json.loads(response)

    def search_web(self, query: str) -> dict:
        # Updated DuckDuckGo Search syntax
        with DDGS() as ddgs:
            results = [r for r in ddgs.text(query, max_results=3)]
        return {"results": results}

    def search_vector_store(self, query: str, vector_store: dict) -> str:
        for filename, chunks in vector_store.items():
            for chunk in chunks:
                if query.lower() in chunk.lower():
                    return chunk
        return None

    def synthesize_results(self, query: str, results: list) -> str:
        prompt = f"""Synthesize this information into a coherent answer for the query: {query}
        Information: {json.dumps(results)}"""
        return self.groq.chat(
            model="mixtral-8x7b-32768",
            messages=[{"role": "user", "content": prompt}]
        )

    def process_query(self, query: str, vector_store: dict) -> str:
        decomposed = self.decompose_query(query)
        results = []
        for sub_q in decomposed:
            local_result = self.search_vector_store(sub_q, vector_store)
            if local_result:
                results.append(local_result)
            else:
                web_result = self.search_web(sub_q)
                if "results" in web_result:
                    results.append(web_result["results"][0]["body"])
                else:
                    results.append("No relevant information found.")
        return self.synthesize_results(query, results)

query_processor = RAGProcessor().process_query