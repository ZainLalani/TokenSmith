class AdaptiveOptimizer:
    def __init__(self):
        pass

    def optimize(self, query, cfg):
        query_length = len(query.split())

        # Simple heuristic rules
        if query_length <= 5:
            return {
                "top_k": 3,
                "use_hyde": False,
                "query": query
            }
        elif query_length <= 12:
            return {
                "top_k": 5,
                "use_hyde": False,
                "query": query
            }
        else:
            return {
                "top_k": 8,
                "use_hyde": True,
                "query": query
            }