# File: src/optimizer/adaptive_optimizer.py

import re
import time
from dataclasses import dataclass, asdict


@dataclass
class OptimizationDecision:
    query: str
    query_words: int
    query_chars: int
    complexity: str
    top_k: int
    use_hyde: bool
    num_candidates: int
    reason: str
    timestamp: float


class AdaptiveOptimizer:
    """
    Rule-based adaptive optimizer for TokenSmith.

    Goal:
    Dynamically tune retrieval parameters based on query complexity.

    Adjustable outputs:
      - top_k
      - use_hyde
      - num_candidates
    """

    def __init__(self):
        self.comparison_terms = {
            "compare", "difference", "versus", "vs",
            "better", "similar", "contrast"
        }

        self.reasoning_terms = {
            "why", "how", "explain", "analyze",
            "justify", "discuss", "evaluate"
        }

        self.multi_topic_terms = {
            "and", "or", "with", "between"
        }

    def optimize(self, query: str):
        words = query.split()
        query_words = len(words)
        query_chars = len(query)

        complexity = self._classify_complexity(query, query_words)

        if complexity == "simple":
            decision = OptimizationDecision(
                query=query,
                query_words=query_words,
                query_chars=query_chars,
                complexity="simple",
                top_k=3,
                use_hyde=False,
                num_candidates=8,
                reason="Short factual query; minimal retrieval sufficient.",
                timestamp=time.time()
            )

        elif complexity == "medium":
            decision = OptimizationDecision(
                query=query,
                query_words=query_words,
                query_chars=query_chars,
                complexity="medium",
                top_k=5,
                use_hyde=False,
                num_candidates=12,
                reason="Moderate query complexity; balanced retrieval.",
                timestamp=time.time()
            )

        else:
            decision = OptimizationDecision(
                query=query,
                query_words=query_words,
                query_chars=query_chars,
                complexity="complex",
                top_k=8,
                use_hyde=True,
                num_candidates=18,
                reason="Complex reasoning/comparison query; expanded retrieval.",
                timestamp=time.time()
            )

        return asdict(decision)

    def _classify_complexity(self, query: str, query_words: int):
        q = query.lower()

        comparison_hits = sum(1 for t in self.comparison_terms if t in q)
        reasoning_hits = sum(1 for t in self.reasoning_terms if t in q)
        multi_hits = sum(1 for t in self.multi_topic_terms if t in q)

        score = 0

        # Length-based signal
        if query_words <= 5:
            score += 0
        elif query_words <= 12:
            score += 1
        else:
            score += 2

        # Semantic signals
        score += comparison_hits
        score += reasoning_hits
        score += multi_hits

        if score <= 1:
            return "simple"
        elif score <= 3:
            return "medium"
        return "complex"