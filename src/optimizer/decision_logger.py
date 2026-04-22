import json
import os
from datetime import datetime


class DecisionLogger:
    def __init__(self, log_dir="logs/decisions"):
        self.log_dir = log_dir
        os.makedirs(log_dir, exist_ok=True)

    def log(self, query, analysis, retrieval_info):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        data = {
            "timestamp": timestamp,
            "query": query,
            "analysis": analysis,
            "retrieval": retrieval_info
        }

        filename = os.path.join(
            self.log_dir,
            f"{timestamp}.json"
        )

        with open(filename, "w") as f:
            json.dump(data, f, indent=2)