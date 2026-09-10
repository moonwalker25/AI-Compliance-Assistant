# Dictionary to store conversation history for each session
# Format:
# {
#     "session_id": [
#         {"role": "user", "content": "..."},
#         {"role": "assistant", "content": "..."}
#     ]
# }

conversation_memory = {}


def get_history(session_id):
    """
    Returns the conversation history for the given session.
    If the session does not exist, create an empty history.
    """
    return conversation_memory.setdefault(session_id, [])


def add_user_message(session_id, message):
    """
    Adds a user message to the conversation history.
    """
    history = get_history(session_id)

    history.append({
        "role": "user",
        "content": message
    })


def add_assistant_message(session_id, message):
    """
    Adds the assistant's response to the conversation history.
    """
    history = get_history(session_id)

    history.append({
        "role": "assistant",
        "content": message
    })


def clear_history(session_id):
    """
    Deletes the conversation history for a session.
    """
    if session_id in conversation_memory:
        del conversation_memory[session_id]