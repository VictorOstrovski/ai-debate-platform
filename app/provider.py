from ollama import chat


def ask_model(prompt: str) -> str:

    try:

        response = chat(
            model="qwen2.5:1.5b",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            options={
                "temperature": 0.1
            }
        )

        return response.message.content

    except Exception as e:

        print("OLLAMA ERROR:", e)

        return f"MODEL ERROR: {str(e)}"