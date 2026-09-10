from services.conversation_router import route_message


history = []

context = {}

messages = [
    "What healthcare regulations apply in India?",
    "What about Germany?",
    "What about Finance?",
    "Tell me a joke.",
    "I think Shops and Establishments Act should apply here."
]

for message in messages:

    result = route_message(
        message,
        history,
        context
    )

    print("\nUSER:", message)
    print("ROUTER:", result)