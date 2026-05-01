import os
import json
from config import get_user_dir

class ChatMemory:
    """
    Manages short-term conversation history for each user.
    Enables follow-up questions (e.g., 'What about his salary?').
    """
    def __init__(self, max_history=5):
        self.max_history = max_history
        self.memory_dir = os.path.join(get_user_dir(), "history")
        os.makedirs(self.memory_dir, exist_ok=True)

    def _get_history_path(self, user_id: str) -> str:
        return os.path.join(self.memory_dir, f"{user_id}.json")

    def get_context(self, user_id: str) -> str:
        """Retrieve recent conversation as a formatted string."""
        path = self._get_history_path(user_id)
        if not os.path.exists(path):
            return ""
        
        with open(path, "r") as f:
            history = json.load(f)
        
        context = "\nConversation History:\n"
        for msg in history[-self.max_history:]:
            context += f"{msg['role'].capitalize()}: {msg['content']}\n"
        return context

    def add_message(self, user_id: str, role: str, content: str):
        """Add a new message to the history and persist it."""
        path = self._get_history_path(user_id)
        history = []
        if os.path.exists(path):
            with open(path, "r") as f:
                history = json.load(f)
        
        history.append({"role": role, "content": content})
        
        # Keep only the last N messages
        if len(history) > self.max_history * 2:
            history = history[-(self.max_history * 2):]
            
        with open(path, "w") as f:
            json.dump(history, f)

    def clear(self, user_id: str):
        path = self._get_history_path(user_id)
        if os.path.exists(path):
            os.remove(path)

# Singleton instance
chat_memory = ChatMemory()
