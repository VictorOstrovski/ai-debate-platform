from ollama import chat


def ask_model(
    prompt: str,
    model: str = "qwen2.5:1.5b"
) -> str:

    try:

        response = chat(
            model=model,
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