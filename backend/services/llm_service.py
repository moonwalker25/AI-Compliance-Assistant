from groq import Groq
from config import GROQ_API_KEY


client = Groq(api_key=GROQ_API_KEY)

MODEL_NAME = "openai/gpt-oss-120b"


def ask_llm(system_prompt: str, user_prompt: str):

    try:

        response = client.chat.completions.create(
            model=MODEL_NAME,

            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ],

            temperature=0.2,
            max_completion_tokens=1024
        )

        return response.choices[0].message.content

    except Exception as e:

        print(f"Groq Error: {e}")

        return (
            "Sorry, I'm currently unable to generate a response. "
            "Please try again later."
        )