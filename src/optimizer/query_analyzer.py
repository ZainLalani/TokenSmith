import re


class QueryAnalyzer:
    def __init__(self):
        self.math_terms = {
            "calculate", "solve", "compute", "find", "derive"
        }

        self.concept_terms = {
            "explain", "describe", "why", "how"
        }

        self.definition_terms = {
            "what is", "define", "meaning of"
        }

    def analyze(self, query: str) -> dict:
        q = query.lower()

        result = {
            "query": query,
            "length": len(q.split()),
            "type": "general",
            "difficulty": "medium",
            "use_hyde": False,
            "top_k": 5
        }

        # computational
        if any(word in q for word in self.math_terms):
            result["type"] = "computational"
            result["top_k"] = 3
            result["difficulty"] = "hard"

        # conceptual
        elif any(word in q for word in self.concept_terms):
            result["type"] = "conceptual"
            result["top_k"] = 7
            result["use_hyde"] = True

        # definition
        elif any(term in q for term in self.definition_terms):
            result["type"] = "definition"
            result["top_k"] = 4
            result["difficulty"] = "easy"

        # broad / long query
        if result["length"] > 12:
            result["top_k"] += 2
            result["use_hyde"] = True

        return result