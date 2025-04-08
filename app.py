import os
from groq import Groq
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variable
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("❌ GROQ_API_KEY not found in environment variables. Please set it in your .env file.")

# Initialize Groq client
client = Groq(api_key=api_key)

# System prompts
system_prompts = {
    "aviation": (
        "You are an aviation expert with in-depth knowledge about aircraft, flight operations, aerodynamics, pilot training, "
        "airline industry, aviation safety, and aerospace technologies. Answer questions only related to aviation. "
        "If asked anything unrelated, respond with: 'I don't know!'"
    ),
    "automobile": (
        "You are an automobile expert with in-depth knowledge about all things related to cars, bikes, trucks, and the automotive industry. "
        "You provide detailed, accurate, and up-to-date answers about vehicle specifications, maintenance tips, technologies, brands, comparisons, "
        "history, and trends. For any non-automobile question, respond with: 'I don't know!'"
    )
}

def get_ai_response(query: str, domain: str) -> str:
    try:
        system_message = system_prompts.get(domain.lower(), system_prompts["automobile"])

        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": query}
            ],
            model="llama-3.3-70b-versatile",
        )

        return chat_completion.choices[0].message.content

    except Exception as e:
        return f"⚠️ Error getting response from Groq API: {str(e)}"

def main():
    try:
        print("Select the domain of your query:")
        print("1. Aviation ✈️")
        print("2. Automobile 🚗")
        domain_choice = input("Enter 1 or 2: ").strip()

        if domain_choice == "1":
            domain = "aviation"
        elif domain_choice == "2":
            domain = "automobile"
        else:
            print("❌ Invalid selection. Please restart the program and choose 1 or 2.")
            return

        while True:
            query = input(f"\nEnter your {domain} query (or 'quit' to exit): ").strip()
            if query.lower() in ['quit', 'exit']:
                print("👋 Goodbye!")
                break

            if not query:
                print("⚠️ Please enter a valid query.")
                continue

            response = get_ai_response(query, domain)
            print("\n🧠 Response:", response)

    except KeyboardInterrupt:
        print("\n👋 Program terminated by user.")
    except Exception as e:
        print(f"\n❌ An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
