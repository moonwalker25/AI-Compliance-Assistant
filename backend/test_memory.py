from services.memory_service import (
    get_history,
    add_user_message,
    add_assistant_message,
    clear_history
)

session = "test-session"

print("========== Test 1 ==========")
print(get_history(session))

print("\n========== Test 2 ==========")
add_user_message(session, "Hello")
print(get_history(session))

print("\n========== Test 3 ==========")
add_assistant_message(session, "Hi! How can I help?")
print(get_history(session))

print("\n========== Test 4 ==========")
clear_history(session)
print(get_history(session))