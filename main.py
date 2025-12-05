from src.chatbot_math import MathChatbot


def main():
    """
    Initializes the MathChatbot and starts the interactive command-line loop.
    """
    try:
        # Instantiating the chatbot triggers the loading of the NLU model and Solver Engine.
        chatbot = MathChatbot()
    except RuntimeError as e:
        # Catches the specific error we built into the initialization process
        print(f"\nFATAL STARTUP ERROR: {e}")
        return

    # Simple interactive loop
    while True:
        # Displays the prompt to the user
        user_input = input("\nMath Query (or 'quit'): ")

        if user_input.lower() == 'quit':
            print("Exiting chatbot. Goodbye.")
            break

        print("\nThinking...")
        # Passes the query to the Orchestrator (MathChatbot.ask)
        answer = chatbot.ask(user_input)

        # Display the final answer
        print("\n**AI Solution**:")
        print(answer)
        print("-" * 50)


if __name__ == "__main__":
    main()