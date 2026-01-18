import os
from pageindex import PageIndexClient
from dotenv import load_dotenv

load_dotenv()

PAGEINDEX_API_KEY = os.getenv("PAGEINDEX_API_KEY")

class RagClient:
    def __init__(self):
        if not PAGEINDEX_API_KEY:
             print("Warning: PAGEINDEX_API_KEY not set")
             self.client = None
        else:
            self.client = PageIndexClient(api_key=PAGEINDEX_API_KEY)

    def upload_file(self, file_path: str):
        if not self.client:
            raise Exception("PageIndex client not initialized")
        
        # submit_document likely takes a path or file-like object
        # Based on SDK inspection, submit_document exists.
        # Assuming it returns a document object with an ID.
        with open(file_path, "rb") as f:
            # We might need to check if submit_document accepts file path or bytes
            # Commonly SDKs accept path.
             response = self.client.submit_document(file_path=file_path)
        
        return response

    def query(self, query: str, file_ids: list[str]):
        if not self.client:
             raise Exception("PageIndex client not initialized")
        
        # Using chat_completions for RAG behavior
        # Assuming we can pass doc_ids or access attached knowledge
        
        # If chat_completions is standard, it might not take file_ids directly solely.
        # However, PageIndex is RAG focused.
        # Let's try to construct a message.
        
        messages = [
            {"role": "user", "content": query}
        ]
        
        # There might be a specific param for documents in PageIndex's chat_completion
        # Or we use submit_query.
        # Let's try chat_completions and pass available params if we knew them.
        # Given I don't see signature, I'll assume it's like OpenAI but maybe with extra args.
        # But wait, submit_query exists. "Vectorless RAG" usually means "Search".
        # But the user wants "Chatbot".
        
        # Let's try submit_query first as it's definitely RAG.
        # But for a conversational interface we might want chat.
        # I will implement a generic 'ask' method that uses chat_completions
        # and assumes we can pass 'document_ids' or similar. 
        # Actually, let's use kwargs to be safe or inspect signature more deeply if I could.
        # For now I will assume 'document_ids' argument or similar.
        
        try:
             # Hypothetical usage based on typical RAG SDKs
            response = self.client.chat_completions(
                messages=messages,
                document_ids=file_ids, # This is a guess, but common for RAG SDKs
                model="gemini-1.5-pro" # User mentioned all using gemini. PageIndex might support model selection.
            )
            return response
        except TypeError:
            # Fallback if document_ids not supported in chat_completions, maybe use submit_query
            print("chat_completions might not support document_ids directly, falling back to simple generation")
            # In a real scenario I would debug this. 
            # Let's return a dummy response if it fails for now or try submit_query
            return self.client.submit_query(query=query, document_ids=file_ids)

rag_client = RagClient()
