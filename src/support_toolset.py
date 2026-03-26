import json
import os
from typing import Any
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss


class SupportToolset:

    def __init__(self):

        self.escalation_log = []

        # load embedding model once
        self.embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

        # load knowledge base
        kb_path = os.path.join(os.path.dirname(__file__), "knowledge_base.json")

        with open(kb_path, "r") as f:
            kb = json.load(f)

        # flatten items
        self.kb_items = []
        texts = []

        for category in kb.get("categories", []):

            category_name = category.get("name", "")

            for item in category.get("items", []):

                self.kb_items.append(item)

                combined_text = (
                    category_name + " " +
                    item.get("question", "") + " " +
                    item.get("answer", "")
                )

                texts.append(combined_text)

        # convert to embeddings
        embeddings = self.embedding_model.encode(texts)

        # create FAISS index
        self.index = faiss.IndexFlatL2(embeddings.shape[1])
        self.index.add(np.array(embeddings))


    async def query_knowledge_base(self, search_term: Any) -> str:

        print(f"\n--- AI SEMANTIC SEARCH: {search_term} ---\n")

        try:

            search_term = str(search_term)

            # embed query
            query_embedding = self.embedding_model.encode([search_term])

            # search top 3 matches
            D, I = self.index.search(np.array(query_embedding), k=3)

            results = []

            for idx in I[0]:

                item = self.kb_items[idx]

                result_text = (
                    f"Policy: {item.get('question','N/A')}\n"
                    f"Answer: {item.get('answer','N/A')}"
                )

                if "steps" in item:

                    result_text += "\nSteps:\n- " + "\n- ".join(item["steps"])

                results.append(result_text)

            if results:

                return "Found in Knowledge Base:\n\n" + "\n\n---\n\n".join(results)

            else:

                return "No relevant information found. Consider escalation."

        except Exception as e:

            print(f"\n--- SEARCH ERROR: {str(e)} ---\n")

            return "Knowledge search failed."


    async def escalate_to_human(self, reason: str, context_summary: str) -> str:

        try:

            ticket_id = f"TKT-{len(self.escalation_log)+1000}"

            ticket = {

                "ticket_id": ticket_id,

                "reason": reason,

                "summary": context_summary

            }

            self.escalation_log.append(ticket)

            return (

                f"I am escalating this issue to a human specialist.\n"
                f"Ticket ID: {ticket_id}\n"
                f"Our support team will contact the customer shortly."
            )

        except Exception as e:

            return f"Escalation failed: {str(e)}"


    def get_tools(self) -> dict[str, Any]:

        return {

            "query_knowledge_base": self,

            "escalate_to_human": self

        }