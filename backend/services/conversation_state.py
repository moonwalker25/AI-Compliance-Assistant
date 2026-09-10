conversation_states = {}


def get_state(session_id):

    return conversation_states.get(
        session_id,
        {}
    )


def update_state(session_id, state):

    conversation_states[session_id] = state


def clear_state(session_id):

    if session_id in conversation_states:
        del conversation_states[session_id]