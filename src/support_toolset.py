import json
import os
from typing import Any

class SupportToolset:
    def __init__(self):
        self.escalation_log = []

    async def query_knowledge_base(self, search_term: Any) -> str:
        # Print exactly what the AI sends us to the terminal!
        print(f"\n--- AI SEARCH INITIATED: {search_term} ---\n") 
        try:
            # 1. Force the search_term to be a string (fixes dictionary crashes)
            if isinstance(search_term, dict):
                search_term = json.dumps(search_term)
            search_term = str(search_term).lower()

            # 2. Bulletproof file loading
            kb_path = os.path.join(os.path.dirname(__file__), 'knowledge_base.json')
            with open(kb_path, 'r') as f:
                kb = json.load(f)

            # 3. Aggressive stop-word filter (added 'policy' so it doesn't match everything)
            filler_words = ["what", "is", "your", "the", "how", "do", "i", "my", "a", "an", "to", "for", "policy", "please"]
            terms = [w.strip("?") for w in search_term.split() if w.strip("?") not in filler_words]
            
            if not terms:
                terms = [search_term.strip("?")]

            results = []
            for category in kb.get("categories", []):
                for item in category.get("items", []):
                    text_to_search = (item.get("question", "") + " " + item.get("answer", "")).lower()
                    
                    if any(word in text_to_search for word in terms):
                        result_text = f"Policy: {item.get('question', 'N/A')}\nAnswer: {item.get('answer', 'See steps below.')}"
                        if "steps" in item:
                            result_text += "\nSteps: " + " -> ".join(item["steps"])
                        results.append(result_text)

            if results:
                return "Found in Knowledge Base:\n\n" + "\n\n---\n\n".join(results[:3])
            else:
                return f"No info found for '{search_term}'. Escalate or ask user."
                
        except Exception as e:
            # Print the EXACT error to your terminal so we aren't guessing
            print(f"\n--- CRITICAL PYTHON ERROR: {str(e)} ---\n")
            return f"Search failed: {str(e)}"

    async def escalate_to_human(self, reason: str, context_summary: str) -> str:
        try:
            ticket_id = f"TKT-{len(self.escalation_log) + 1000}"
            self.escalation_log.append({"ticket": ticket_id, "reason": reason, "context": context_summary})
            return f"ESCALATION SUCCESSFUL. Ticket ID: {ticket_id}. Tell the customer a Tier 2 specialist will contact them shortly."
        except Exception as e:
            return f"Escalation failed: {str(e)}"

    def get_tools(self) -> dict[str, Any]:
        return {
            'query_knowledge_base': self,
            'escalate_to_human': self,
        }