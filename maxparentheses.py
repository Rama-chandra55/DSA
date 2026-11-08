def simple_ai_mode():
    # Hardcoded knowledge base
    responses = {
        "hello": "Hello! Welcome to simple AI Mode. How can I help you today?",
        "what is ai mode": "AI Mode is a conversational search feature that answers complex questions directly.",
        "weather": "I am hardcoded, so I cannot check live weather, but it is always sunny in the terminal!",
        "bye": "Goodbye! Closing AI Mode."
    }

    print("Simple AI Mode started. Type 'bye' to exit.\n")

    while True:
        user_input = input("You: ").strip().lower()

        if user_input in responses:
            print("AI Mode:", responses[user_input], "\n")
            if user_input == "bye":
                break
        else:
            print("AI Mode: Sorry, I only understand hardcoded phrases like 'hello' or 'what is ai mode'.\n")

if __name__ == "__main__":
    simple_ai_mode()
